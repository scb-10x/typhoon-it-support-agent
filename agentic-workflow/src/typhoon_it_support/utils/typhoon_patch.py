"""Patch for Typhoon API compatibility with LangChain.

The Typhoon API expects 'max_tokens' parameter but LangChain's ChatOpenAI
converts it to 'max_completion_tokens' which the Typhoon API doesn't handle correctly.
This patch ensures the correct parameter is sent to the API.
"""

import openai
from typing import Any

_PATCH_APPLIED = False
_ORIGINAL_CREATE = None


def apply_typhoon_api_patch() -> None:
    """Apply monkey patch to OpenAI client for Typhoon API compatibility.
    
    This patch converts 'max_completion_tokens' to 'max_tokens' in API requests,
    which is required for the Typhoon API to properly handle token limits.
    
    The patch is idempotent - calling it multiple times has no additional effect.
    """
    global _PATCH_APPLIED, _ORIGINAL_CREATE
    
    if _PATCH_APPLIED:
        return
    
    # Store original create method
    _ORIGINAL_CREATE = openai.resources.chat.completions.Completions.create
    
    def patched_create(self: Any, **kwargs: Any) -> Any:
        """Patched create method that converts max_completion_tokens to max_tokens."""
        if 'max_completion_tokens' in kwargs:
            # Typhoon API uses max_tokens, not max_completion_tokens
            max_val = kwargs.pop('max_completion_tokens')
            kwargs['max_tokens'] = max_val
        
        return _ORIGINAL_CREATE(self, **kwargs)
    
    # Apply monkey patch
    openai.resources.chat.completions.Completions.create = patched_create
    _PATCH_APPLIED = True

