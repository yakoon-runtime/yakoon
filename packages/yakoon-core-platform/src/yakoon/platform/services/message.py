# yakoon/platform/runtime/message/parser.py
from __future__ import annotations

from typing import Any

import yaml

from yakoon.base.models.message import (
    Inline,
    InlineCode,
    InlineLink,
    InlineText,
    KvBlock,
    ListBlock,
    MessageSpec,
    TextBlock,
)


class MessageSpecService:

    async def parse_spec(self, raw: str) -> MessageSpec:
        """
        Parse a YAML-rendered message specification into a Python mapping.

        Args:
            yaml_text: YAML string produced by the template renderer.

        Returns:
            A dict representing the MessageSpec (JSON-serializable).

        Raises:
            TypeError: If the YAML root is not a mapping.
            ValueError: If YAML cannot be parsed.
        """

        raw = yaml.safe_load(raw)

        # print(type(raw), raw)
        if not isinstance(raw, dict):
            raise TypeError("MessageSpec root must be a mapping")

        kind = raw.get("kind")
        if kind != "message":
            raise ValueError("MessageSpec.kind must be 'message'")

        role = raw.get("role")
        if role not in ("info", "success", "warning", "error", "help"):
            raise ValueError(f"Invalid MessageSpec.role: {role!r}")

        title = raw.get("title")
        if title is not None and not isinstance(title, str):
            raise TypeError("MessageSpec.title must be a string or null")

        blocks_raw = raw.get("blocks", [])
        if not isinstance(blocks_raw, list):
            raise TypeError("MessageSpec.blocks must be a list")

        blocks = [self.parse_block(b) for b in blocks_raw]

        meta = raw.get("meta")
        if meta is not None and not isinstance(meta, dict):
            raise TypeError("MessageSpec.meta must be a mapping or null")

        return MessageSpec(
            kind="message",
            role=role,
            title=title,
            blocks=blocks,
            meta=meta,
        )

    def parse_block(self, raw: Any) -> TextBlock | ListBlock | KvBlock:
        """Parse a single block mapping."""
        if not isinstance(raw, dict):
            raise TypeError("Block must be a mapping")

        t = raw.get("type")
        if t == "text":
            text = raw.get("text", "")
            return TextBlock(type="text", text=self.parse_inline_or_str(text))

        if t == "list":
            items = raw.get("items", [])
            if not isinstance(items, list):
                raise TypeError("list.items must be a list")

            parsed_items: list[str | list[Inline]] = []
            for item in items:
                parsed_items.append(self.parse_inline_or_str(item))
            return ListBlock(type="list", items=parsed_items)

        if t == "kv":
            items = raw.get("items", [])
            if not isinstance(items, list):
                raise TypeError("kv.items must be a list of [key, value] pairs")

            pairs: list[tuple[str, str]] = []
            for entry in items:
                if not isinstance(entry, list) or len(entry) != 2:
                    raise TypeError("Each kv item must be a [key, value] list")
                k, v = entry
                pairs.append((str(k), str(v)))
            return KvBlock(type="kv", items=pairs)

        raise ValueError(f"Unknown block type: {t!r}")

    def parse_inline_or_str(self, raw: Any) -> str | list[Inline]:
        """
        Parse inline-capable fields.

        Accepts:
        - plain string -> returned as string
        - list of inline node mappings -> returned as list[Inline]
        """
        if isinstance(raw, str):
            return raw

        if isinstance(raw, list):
            return [self.parse_inline_node(n) for n in raw]

        raise TypeError("Inline field must be a string or a list of inline nodes")

    def parse_inline_node(self, raw: Any) -> Inline:
        """Parse a single inline node mapping."""
        if not isinstance(raw, dict):
            raise TypeError("Inline node must be a mapping")

        t = raw.get("type")
        if t == "text":
            return InlineText(type="text", text=str(raw.get("text", "")))

        if t == "code":
            return InlineCode(type="code", code=str(raw.get("code", "")))

        if t == "link":
            text = raw.get("text")
            href = raw.get("href")
            if not isinstance(text, str) or not isinstance(href, str):
                raise TypeError("link requires string fields: text, href")
            return InlineLink(type="link", text=text, href=href)

        raise ValueError(f"Unknown inline type: {t!r}")
