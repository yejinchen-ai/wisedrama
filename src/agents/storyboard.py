"""Public storyboard-agent module.

The implementation remains compatible with the historical ``prompter`` module so existing
imports continue to work while new code can use the domain-specific StoryboardAgent name.
"""

from .prompter import EnhancedPrompts, OptimizedPrompt, StoryboardAgent

__all__ = ["EnhancedPrompts", "OptimizedPrompt", "StoryboardAgent"]
