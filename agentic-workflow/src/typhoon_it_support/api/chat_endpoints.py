"""Chat-related API endpoints."""

import asyncio
import json
import uuid
from queue import Empty
from typing import AsyncGenerator, Dict

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from ..config import get_settings
from ..config.user_context import get_current_user
from ..events import EventEmitter, create_event_callbacks
from ..graph import create_workflow, create_workflow_with_events
from ..models import AgentState
from ..prompts import AGENT_SYSTEM_PROMPT
from .models import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])

# In-memory session storage (replace with Redis/DB in production)
sessions: Dict[str, list] = {}


@router.post("/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    """Handle chat messages with streaming response.

    Args:
        request: Chat request with user message.

    Returns:
        Streaming response with Server-Sent Events.
    """
    settings = get_settings()
    session_id = request.session_id or str(uuid.uuid4())

    # Initialize or retrieve session history
    if session_id not in sessions:
        sessions[session_id] = []

    async def generate() -> AsyncGenerator[str, None]:
        """Generate streaming response."""
        try:
            # Initialize LLM with streaming
            llm = ChatOpenAI(
                model=settings.typhoon_model,
                temperature=settings.temperature,
                max_tokens=settings.max_tokens,
                api_key=settings.typhoon_api_key,
                base_url=settings.typhoon_base_url,
                streaming=True,
            )

            # Prepare messages
            messages = [SystemMessage(content=AGENT_SYSTEM_PROMPT)]
            messages.append(HumanMessage(content=request.message))

            # Stream response
            full_response = ""
            async for chunk in llm.astream(messages):
                if chunk.content:
                    full_response += chunk.content
                    # Send each chunk as SSE
                    data = json.dumps(
                        {
                            "type": "token",
                            "content": chunk.content,
                            "session_id": session_id,
                        }
                    )
                    yield f"data: {data}\n\n"

            # Store complete message in session
            sessions[session_id].append(
                {
                    "user": request.message,
                    "assistant": full_response,
                }
            )

            # Send completion event
            final_data = json.dumps(
                {
                    "type": "done",
                    "session_id": session_id,
                    "full_response": full_response,
                }
            )
            yield f"data: {final_data}\n\n"

        except Exception as e:
            error_data = json.dumps({"type": "error", "error": str(e)})
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/workflow")
async def chat_workflow(request: ChatRequest) -> StreamingResponse:
    """Handle chat messages with full workflow event streaming.

    Args:
        request: Chat request with user message.

    Returns:
        Streaming response with workflow events via SSE.
    """
    session_id = request.session_id or str(uuid.uuid4())

    # Initialize or retrieve session history
    if session_id not in sessions:
        sessions[session_id] = []

    # Get current user info
    user_profile = get_current_user()

    async def generate() -> AsyncGenerator[str, None]:
        """Generate streaming response with workflow events."""
        # Create event emitter and subscribe
        emitter = EventEmitter()
        event_queue = emitter.subscribe()
        callbacks = create_event_callbacks(emitter)

        # Create workflow with event tracking
        workflow = create_workflow_with_events(emitter)

        # Prepare initial state with user info
        initial_state: AgentState = {
            "messages": [HumanMessage(content=request.message)],
            "iteration": 0,
            "next_action": "start",
            "active_tickets": [],
            "searched_documents": [],
            "user_info": user_profile.to_dict(),
        }

        # Configuration for checkpointer (thread-based memory)
        config = {"configurable": {"thread_id": session_id}}

        # Run workflow in a separate task
        async def run_workflow():
            """Run the workflow and handle errors."""
            callbacks["on_workflow_start"]({"session_id": session_id})

            # Run workflow in thread pool (invoke is synchronous)
            loop = asyncio.get_event_loop()
            final_state = await loop.run_in_executor(
                None, lambda: workflow.invoke(initial_state, config)
            )

            # Extract assistant's response
            assistant_message = ""
            if final_state.get("messages"):
                for msg in reversed(final_state["messages"]):
                    if hasattr(msg, "type") and msg.type == "ai":
                        assistant_message = msg.content
                        break

            if not assistant_message:
                assistant_message = (
                    "I apologize, but I couldn't generate a response. Please try again."
                )

            # Store in session
            sessions[session_id].append(
                {
                    "user": request.message,
                    "assistant": assistant_message,
                }
            )

            # Send completion event
            callbacks["on_done"](
                message=assistant_message,
                data={
                    "session_id": session_id,
                    "iteration": final_state.get("iteration", 0),
                    "next_action": final_state.get("next_action", "end"),
                },
            )

            callbacks["on_workflow_end"]({"session_id": session_id})

        # Start workflow execution
        workflow_task = asyncio.create_task(run_workflow())

        # Stream events as they arrive
        try:
            while True:
                # Check if workflow is done
                if workflow_task.done():
                    # Get any remaining events
                    while True:
                        event = (
                            event_queue.get_nowait()
                            if not event_queue.empty()
                            else None
                        )
                        if event is None:
                            break
                        yield f"data: {event.to_json()}\n\n"
                    break

                # Try to get event with timeout
                try:
                    event = event_queue.get(timeout=0.1)
                    yield f"data: {event.to_json()}\n\n"
                except Empty:
                    # No event available, check if workflow is done
                    if workflow_task.done():
                        continue
                    # Send keepalive
                    await asyncio.sleep(0.1)
        except Exception as e:
            error_data = json.dumps(
                {
                    "type": "error",
                    "error": str(e),
                    "timestamp": "",
                }
            )
            yield f"data: {error_data}\n\n"
        finally:
            emitter.unsubscribe(event_queue)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Handle chat messages from the frontend.

    Args:
        request: Chat request with user message.

    Returns:
        Chat response with assistant's reply.
    """
    # Generate or use existing session ID
    session_id = request.session_id or str(uuid.uuid4())

    # Initialize or retrieve session history
    if session_id not in sessions:
        sessions[session_id] = []

    # Get current user info
    user_profile = get_current_user()

    # Create workflow
    workflow = create_workflow()

    # Prepare initial state with user info
    initial_state: AgentState = {
        "messages": [HumanMessage(content=request.message)],
        "iteration": 0,
        "next_action": "start",
        "active_tickets": [],
        "searched_documents": [],
        "user_info": user_profile.to_dict(),
    }

    # Configuration for checkpointer (thread-based memory)
    config = {"configurable": {"thread_id": session_id}}

    # Run workflow
    final_state = workflow.invoke(initial_state, config)

    # Extract assistant's response
    assistant_message = ""
    if final_state.get("messages"):
        for msg in reversed(final_state["messages"]):
            if hasattr(msg, "type") and msg.type == "ai":
                assistant_message = msg.content
                break

    if not assistant_message:
        assistant_message = (
            "I apologize, but I couldn't generate a response. Please try again."
        )

    # Store in session
    sessions[session_id].append(
        {
            "user": request.message,
            "assistant": assistant_message,
        }
    )

    # Return response
    return ChatResponse(
        message=assistant_message,
        session_id=session_id,
        iteration=final_state.get("iteration", 0),
        next_action=final_state.get("next_action", "end"),
    )


@router.delete("/{session_id}")
async def clear_session(session_id: str) -> dict:
    """Clear a chat session.

    Args:
        session_id: Session ID to clear.

    Returns:
        Success message.
    """
    if session_id in sessions:
        del sessions[session_id]

    return {"status": "success", "message": "Session cleared"}


@router.get("/{session_id}")
async def get_session(session_id: str) -> dict:
    """Get chat history for a session.

    Args:
        session_id: Session ID to retrieve.

    Returns:
        Session history.
    """
    from fastapi import HTTPException

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session_id,
        "history": sessions[session_id],
    }
