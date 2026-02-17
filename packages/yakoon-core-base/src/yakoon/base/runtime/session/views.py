from __future__ import annotations


def v_text(text: str, *, role: str = "info", mode: str = "append") -> dict:
    return {
        "kind": "view",
        "mode": mode,
        "message": {
            "kind": "message",
            "role": role,
            "blocks": [{"type": "text", "text": text}],
        },
    }


def v_error(text: str, *, mode: str = "append") -> dict:
    return v_text(text, role="error", mode=mode)


def v_status(text: str, *, mode: str = "append") -> dict:
    return v_text(text, role="info", mode=mode)
