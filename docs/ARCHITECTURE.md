# Architecture

Understanding the design and components of the Typhoon IT Support system.

## System Overview

The system implements an **agentic workflow** pattern using LangGraph, where an AI agent can think, act, and observe through multiple iterations to solve IT support problems.

## High-Level Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Frontend      │ ───► │    Backend       │ ───► │   LangGraph     │
│   (Next.js)     │ HTTP │   (FastAPI)      │      │   Workflow      │
│                 │ ◄─── │                  │ ◄─── │                 │
│ - Chat UI       │ SSE  │ - API Routes     │      │ - Agent Nodes   │
│ - Streaming     │      │ - Session Mgmt   │      │ - Tools         │
│ - Markdown      │      │ - Event System   │      │ - State Mgmt    │
└─────────────────┘      └──────────────────┘      └─────────────────┘
```

## Core Components

### 1. Frontend (Next.js + React)

**Location:** `frontend/app/components/Chat.tsx`

Responsibilities:
- Render chat interface with Thai localization
- Stream responses using Server-Sent Events (SSE)
- Display markdown-formatted messages
- Manage session state

Key Features:
- Real-time token streaming
- Markdown rendering with syntax highlighting
- Thai-first UI design
- Dark mode support

### 2. Backend (FastAPI)

**Location:** `agentic-workflow/src/typhoon_it_support/api/`

Responsibilities:
- Expose REST API endpoints
- Stream responses via SSE
- Manage user sessions
- Handle CORS and security

Endpoints:
- `POST /chat` - Standard chat (returns JSON)
- `POST /chat/stream` - Streaming chat (returns SSE)
- `GET /health` - Health check
- Ticket management endpoints

### 3. LangGraph Workflow

**Location:** `agentic-workflow/src/typhoon_it_support/graph/workflow.py`

The core agentic workflow implementing the Think → Act → Observe pattern.

#### Workflow Graph

```
START
  ↓
agent (THINK)
  ↓
tools (ACT)
  ↓
observe (OBSERVE)
  ↓
router (DECIDE)
  ├─→ continue → agent (loop back)
  ├─→ escalate → END
  └─→ end → END
```

#### Node Descriptions

**Agent Node** (`agents/agent_node.py`)
- **Think phase**: Decide what action to take
- Uses Typhoon LLM with system prompt
- Can invoke tools or respond directly

**Tool Node** (`agents/tool_node.py`)
- **Act phase**: Execute requested tools
- Runs document search, ticket operations, etc.
- Tracks context to avoid redundant operations

**Observe Node** (implicit in agent)
- **Observe phase**: Process tool results
- Formulate response based on outcomes
- Decide if more actions needed

**Router Node** (routing logic)
- **Decide phase**: Determine next action
- Options: continue, escalate, or end
- Checks iteration limits and completion signals

### 4. State Management

**Location:** `agentic-workflow/src/typhoon_it_support/models/state.py`

```python
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # Conversation history
    iteration: int                            # Current iteration count
    context: dict                             # Active context (tickets, docs)
```

State flows through the graph, accumulating messages and context.

### 5. Tools

**Location:** `agentic-workflow/src/typhoon_it_support/tools/`

Tools extend the agent's capabilities:

**Document Search:**
- `search_it_policy` - Search IT policies
- `search_troubleshooting_guide` - Search troubleshooting docs
- Uses FAISS vector store for semantic search

**Ticket Management:**
- `create_ticket` - Create support tickets
- `get_ticket` - Retrieve ticket details
- `update_ticket_status` - Update ticket status
- `add_ticket_comment` - Add comments
- `search_tickets` - Search existing tickets

**Utilities:**
- `get_current_time` - Get current timestamp

### 6. Event System

**Location:** `agentic-workflow/src/typhoon_it_support/events/`

Enables real-time streaming:

**Emitter:**
- Publishes events (tokens, chunks, errors)
- Thread-safe event queue

**Middleware:**
- Intercepts LLM callbacks
- Converts to SSE format
- Streams to frontend

### 7. Prompts

**Location:** `agentic-workflow/src/typhoon_it_support/prompts/agent_prompts.py`

System prompts define agent behavior:

**AGENT_SYSTEM_PROMPT:**
- Role definition and guidelines
- Tool usage instructions
- Response format (always Thai)
- Best practices (avoid redundant searches)

**Design Principles:**
- Internal reasoning in English
- User-facing responses in Thai
- Concise and structured
- Clear tool documentation

## Data Flow

### Request Processing

1. **User Input**
   - User types message in frontend
   - Frontend sends POST to `/chat/stream`

2. **Session Management**
   - Backend retrieves or creates session
   - Loads conversation history from checkpointer

3. **Workflow Invocation**
   - Create initial state with user message
   - Invoke LangGraph workflow

4. **Agent Execution**
   - Agent analyzes message and context
   - Decides to use tools or respond directly
   - If tools needed, invokes tool node

5. **Tool Execution**
   - Tool node executes requested tools
   - Returns results to agent
   - Updates context

6. **Response Generation**
   - Agent formulates response based on tool results
   - Streams tokens via event system
   - Frontend displays in real-time

7. **Routing Decision**
   - Router checks if conversation complete
   - Continues loop if more actions needed
   - Ends workflow when resolved

8. **State Persistence**
   - Final state saved to checkpointer
   - Session preserved for follow-up questions

## Memory & Checkpointing

**Checkpointer Types:**

### Memory Checkpointer (Development)
- In-memory storage
- Fast performance
- Lost on restart
- Good for development

### SQLite Checkpointer (Production)
- Persistent storage in SQLite database
- Survives application restarts
- Thread-safe
- Production-ready

**Session Management:**
- Each user gets unique `session_id`
- Conversations isolated by session
- Full message history maintained
- Context carries across turns

## Vector Store

**Technology:** FAISS (Facebook AI Similarity Search)

**Location:** `vector_store/`

**Process:**
1. Documents loaded from `documents/`
2. Text split into chunks
3. Embeddings created with Typhoon
4. Stored in FAISS index

**Usage:**
- Fast semantic search (<100ms)
- Retrieves relevant document sections
- Feeds context to agent

## Configuration System

**Location:** `agentic-workflow/src/typhoon_it_support/config/settings.py`

**Hierarchy:**
1. Default values
2. Environment variables (`.env`)
3. Constructor arguments (if applicable)

**Key Settings:**
- `TYPHOON_API_KEY` - API authentication
- `TYPHOON_MODEL` - Model selection
- `TEMPERATURE` - Response creativity
- `MAX_TOKENS` - Response length
- `MAX_ITERATIONS` - Loop limit

## Security Considerations

### API Key Management
- Stored in `.env` file
- Not committed to git
- Accessed via environment variables

### Input Validation
- Type checking with Pydantic
- Request size limits
- Session validation

### CORS Configuration
- Configured for frontend origin
- Credentials support enabled
- Preflight handling

## Performance Optimizations

### Streaming
- Token-by-token delivery
- First token in <1s
- Better perceived performance

### Caching
- Vector store loaded once
- Checkpointer maintains state
- LLM responses not cached (intentional)

### Context Management
- Track searched documents
- Avoid redundant tool calls
- Trim old messages if needed

## Error Handling

### Levels
1. **Input Validation** - Pydantic models
2. **Tool Execution** - Try-catch with fallbacks
3. **LLM Failures** - Retry logic
4. **Workflow Errors** - Graceful degradation

### Strategy
- Log all errors
- Return user-friendly messages
- Preserve session state
- Enable recovery

## Scalability

### Horizontal Scaling
- Stateless backend services
- Session state in shared storage (SQLite/Redis)
- Load balancer friendly

### Vertical Scaling
- Efficient state management
- Minimal memory footprint
- Connection pooling

### Future Improvements
- Redis for distributed sessions
- Message queue for background tasks
- Caching layer for common queries

## Extension Points

### Adding Tools
1. Create tool function in `tools/`
2. Export from `tools/__init__.py`
3. Document in tool docstring
4. Agent automatically discovers it

### Adding Agent Nodes
1. Create node function
2. Add to workflow graph
3. Define edges and routing
4. Update state model if needed

### Custom Prompts
1. Edit `prompts/agent_prompts.py`
2. Version control changes
3. Test with evaluation suite

## Monitoring & Observability

### Logging
- Structured logging with Python logging
- Log levels: DEBUG, INFO, WARNING, ERROR
- Logs to console and file

### Metrics
- Response times tracked
- Tool usage counted
- Error rates monitored

### Events
- Real-time event stream
- Token counts
- Tool invocations

## Design Principles

1. **Separation of Concerns**
   - Each module has single responsibility
   - Clear boundaries between components

2. **Type Safety**
   - Type hints everywhere
   - Pydantic models for validation
   - Static type checking with mypy

3. **Testability**
   - Modular design enables unit tests
   - Fixtures for common test data
   - High test coverage (79%)

4. **Extensibility**
   - Easy to add new tools
   - Simple to modify prompts
   - Pluggable components

5. **Production Ready**
   - Proper error handling
   - Security considerations
   - Performance optimizations
   - Comprehensive testing

## Summary

The architecture provides a solid foundation for building intelligent agentic systems:

- **Frontend**: Modern, responsive chat interface
- **Backend**: Robust API with streaming support
- **Workflow**: Flexible LangGraph agent loop
- **Tools**: Extensible tool ecosystem
- **State**: Persistent conversation memory

All components work together to deliver a production-ready IT support assistant powered by Typhoon 2.5.

---

**Next:** Learn how to [extend the system](EXTENDING.md) with your own tools and features.


