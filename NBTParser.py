import struct

import Tag
from TagTypes import TagType


class Parser():
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.bytes_buffer = None
        self.parsed_root = None
    
    def print_root(self):
        print(self.parsed_root)
    
    def parse(self) -> None:
        with open(self.file_path, 'rb') as file:
            self.bytes_buffer = file.read()
        
        tag_type = self.parse_byte()
            
        if tag_type == TagType.TAG_COMPOUND.value:
            self.parsed_root = self.parse_compound_tag()
        else:
            # TODO: custom exception
            raise Exception("First tag should be compound!")
    
    def save_to_file(self, output_file_path: str) -> None:
        pass

    def split_buffer(self, length):
        buff = self.bytes_buffer[0:length]
        self.bytes_buffer = self.bytes_buffer[length:]
        
        return buff

    def parse_name(self):
        length = struct.unpack(">h", self.split_buffer(2))[0]
        name = struct.unpack(f">{length}s", self.split_buffer(length))[0]
        
        return name

    def parse_int(self):
        integer = struct.unpack(">i", self.split_buffer(4))[0]
        return integer

    def parse_byte(self):
        byte = struct.unpack(">b", self.split_buffer(1))[0]
        return byte

    def parse_compound_tag(self) -> Tag.TagCompound:
        name = self.parse_name()
        compound_tag = Tag.TagCompound(name)
        
        while True:
            tag_type = self.parse_byte()
            
            match tag_type:
                case TagType.TAG_END.value:
                    return compound_tag
                case TagType.TAG_STRING.value:
                    current_tag = self.parse_string_tag()
                case _:
                    # TODO: custom exception
                    raise Exception("Unknown tag type")
            
            compound_tag.append(current_tag)
            
    def parse_string_tag(self):
        name = self.parse_name()
        length = struct.unpack(">h", self.split_buffer(2))[0]
        value = struct.unpack(f">{length}s", self.split_buffer(length))[0]
        
        return Tag.TagString(name, Tag.TagShort("", length), value.decode())
