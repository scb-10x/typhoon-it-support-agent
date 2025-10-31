"""LLM factory utilities to reduce duplication."""

from langchain_openai import ChatOpenAI

from ..config import get_settings


def create_llm(
    temperature: float | None = None,
    max_tokens: int | None = None,
    streaming: bool = False,
) -> ChatOpenAI:
    """Create LLM instance with consistent settings.

    Args:
        temperature: Temperature setting for LLM. If None, uses settings default.
        max_tokens: Maximum tokens for LLM. If None, uses settings default.
        streaming: Enable streaming responses.

    Returns:
        Configured ChatOpenAI instance.
    """
    settings = get_settings()

    return ChatOpenAI(
        model=settings.typhoon_model,
        temperature=temperature if temperature is not None else settings.temperature,
        max_tokens=max_tokens if max_tokens is not None else settings.max_tokens,
        api_key=settings.typhoon_api_key,
        base_url=settings.typhoon_base_url,
        streaming=streaming,
    )


def create_tool_llm(tools: list) -> ChatOpenAI:
    """Create LLM with tools bound.

    Args:
        tools: List of tools to bind to LLM.

    Returns:
        ChatOpenAI instance with tools bound.
    """
    llm = create_llm(temperature=0.2, streaming=False)
    return llm.bind_tools(tools)


def create_routing_llm() -> ChatOpenAI:
    """Create LLM optimized for routing decisions.

    Returns:
        ChatOpenAI instance configured for routing.
    """
    return create_llm(temperature=0.1, max_tokens=50, streaming=False)


def create_streaming_llm() -> ChatOpenAI:
    """Create LLM with streaming enabled for responses.

    Returns:
        ChatOpenAI instance with streaming enabled.
    """
    return create_llm(streaming=True)



