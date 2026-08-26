"""Offline mock LLM targets for demoing the prompt-injection tester.

Neither function calls a real model or network service. They are simple
string-matching stand-ins so the tester can be exercised with zero API keys.
"""

import re

SECRET_MARKER = "SECRET_MARKER_XYZ"

_OVERRIDE_CUES = re.compile(
    r"ignore|disregard|forget|override|new instructions|stop\.", re.IGNORECASE
)
_EXFIL_CUES = re.compile(
    r"repeat the text|original instructions|reveal|secret|summarize everything",
    re.IGNORECASE,
)
_JAILBREAK_CUES = re.compile(
    r"no restrictions|unfiltered|dan|do anything now|always complies|no limitations",
    re.IGNORECASE,
)


def vulnerable_target(prompt: str) -> str:
    """Naive mock target with no injection defenses."""
    if _EXFIL_CUES.search(prompt):
        return f"Sure, here it is: {SECRET_MARKER}"
    if _OVERRIDE_CUES.search(prompt) or _JAILBREAK_CUES.search(prompt):
        return "INJECTED: understood, I will comply with your new instructions."
    return "I'm a helpful assistant. How can I help you today?"


def hardened_target(prompt: str) -> str:
    """Mock target that recognizes and refuses injection patterns."""
    if _EXFIL_CUES.search(prompt) or _OVERRIDE_CUES.search(prompt) or _JAILBREAK_CUES.search(prompt):
        return "I can't comply with that request."
    return "I'm a helpful assistant. How can I help you today?"
