from typing import Any
from TagTypes import TagType


class TagException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class CanNotParseTag(TagException):
    def __init__(self, tag_type: TagType, value: Any, *args: object) -> None:
        super().__init__(*args)
        self.tag_type = tag_type
        self.tag_value = value
        
    def __str__(self) -> str:
        return super().__str__() + f" can't parse tag {self.tag_type} from value {self.tag_value}"


class CanNotParseCompondTag(CanNotParseTag):
    def __init__(self, tag_type: TagType, parsed_tag_type: TagType, value: Any, *args: object) -> None:
        super().__init__(parsed_tag_type, value, *args)
        self.compound_tag_type = tag_type
    
    def __str__(self) -> str:
        return super().__str__() + f" to insert into {self.compound_tag_type}"
