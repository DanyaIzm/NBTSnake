"""
    NBT Tags
"""

from typing import Any
from TagExceptions import CanNotParseCompondTag, CanNotParseTag
from TagTypes import TagType
        
        
class TagNotNamed():
    def __init__(self, tag_type: TagType, payload: Any | None) -> None:
        self.tag_type = tag_type


class Tag(TagNotNamed):
    def __init__(self, tag_type: TagType, name: str, payload: Any | None) -> None:
        super().__init__(tag_type, payload)
        self.name = name


class TagCompoundBase(Tag):
    def __init__(self, tag_type: TagType, name: str) -> None:
        super().__init__(tag_type, name, None)
        self.tags: list[Tag] = []
    
    def append(self, tag: Tag) -> None:
        self.tags.append(tag)


class TagCompound(TagCompoundBase):
    def __init__(self, name: str) -> None:
        super().__init__(TagType.TAG_COMPOUND, name)


class TagEnd(TagNotNamed):
    def __init__(self) -> None:
        super().__init__(TagType.TAG_END)


class TagByte(Tag):
    def __init__(self, name: str, payload: Any | None) -> None:
        if type(payload) != int:
            raise CanNotParseTag(TagType.TAG_BYTE, payload)
        
        super().__init__(TagType.TAG_BYTE, name, int(payload))


class TagShort(Tag):
    def __init__(self, name: str, payload: Any | None) -> None:
        if type(payload) != int:
            raise CanNotParseTag(TagType.TAG_SHORT, payload)
        
        super().__init__(TagType.TAG_SHORT, name, int(payload))


class TagInt(Tag):
    def __init__(self, name: str, payload: Any | None) -> None:
        if type(payload) != int:
            raise CanNotParseTag(TagType.TAG_INT, payload)
        
        super().__init__(TagType.TAG_INT, name, int(payload))


class TagLong(Tag):
    def __init__(self, name: str, payload: Any | None) -> None:
        if type(payload) != int:
            raise CanNotParseTag(TagType.TAG_LONG, payload)
        
        super().__init__(TagType.TAG_LONG, name, int(payload))


class TagFloat(Tag):
    def __init__(self, name: str, payload: Any | None) -> None:
        if type(payload) != float:
            raise CanNotParseTag(TagType.TAG_FLOAT, payload)
        
        super().__init__(TagType.TAG_FLOAT, name, float(payload))


class TagDouble(Tag):
    def __init__(self, name: str, payload: Any | None) -> None:
        if type(payload) != float:
            raise CanNotParseTag(TagType.TAG_DOUBLE, payload)
        
        super().__init__(TagType.TAG_DOUBLE, name, float(payload))
        
        
class TagByteArray(TagCompoundBase):
    def __init__(self, name: str, length: TagInt, array: bytes) -> None:
        super().__init__(TagType.TAG_BYTE_ARRAY, name)

        if type(length) != TagInt:
            raise CanNotParseCompondTag(TagType.TAG_BYTE_ARRAY, TagType.TAG_INT, length)
        
        if type(array) != bytes:
            raise CanNotParseCompondTag(TagType.TAG_BYTE_ARRAY, bytes, array)
        
        self.append(length)
        self.append(array)


class TagString(TagCompoundBase):
    def __init__(self, name: str, length: TagInt, string: str) -> None:
        super().__init__(TagType.TAG_STRING, name)

        if type(length) != TagInt:
            raise CanNotParseCompondTag(TagType.TAG_STRING, TagType.TAG_INT, length)
        
        if type(string) != str:
            raise CanNotParseCompondTag(TagType.TAG_STRING, str, length)

        
        self.append(length)
        self.append(string)


class TagList(TagCompoundBase):
    def __init__(self, name: str, tag_id: TagByte, length: TagInt, tags: list[TagNotNamed]) -> None:
        super().__init__(TagType.TAG_LIST, name)

        if type(tag_id) != TagByte:
            raise CanNotParseCompondTag(TagType.TAG_LIST, TagType.TAG_INT, tag_id)
        
        if type(length) != TagInt:
            raise CanNotParseCompondTag(TagType.TAG_LIST, TagType.TAG_INT, length)
        
        if type(tags) != list:
            raise CanNotParseCompondTag(TagType.TAG_LIST, list, tags)
        
        # TODO: check for TagNotNamed in tags list
        
        self.append(tag_id)
        self.append(length)
        self.tagsList = tags
