"""
    NBT Tags
"""

from typing import Any
from TagTypes import TagType


class Tag():
    def __init__(self, tag_type: TagType, name: str, payload: Any | None) -> None:
        self.tag_type = tag_type
        self.name = name
