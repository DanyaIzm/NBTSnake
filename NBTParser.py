import struct
from gzip import GzipFile, BadGzipFile

import Tag
from TagTypes import TagType


class Parser():
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.bytes_buffer = None
        self.parsed_root = None
    
    def print_root(self):
        print(self.parsed_root.tree(0))
    
    def parse(self) -> None:
        try:
            with GzipFile(self.file_path) as file:
                self.bytes_buffer = file.read()
        except BadGzipFile:
            print("File is not GZipped. Trying to read like uncompressed binary file")
            
            with open(self.file_path, 'rb') as file:
                self.bytes_buffer = file.read()
        
        tag_type = self.parse_byte()
            
        if tag_type == TagType.TAG_COMPOUND.value:
            self.parsed_root = self.parse_compound_tag(False)
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

    def parse_byte(self):
        return struct.unpack(">b", self.split_buffer(1))[0]
    
    def parse_short(self):
        return struct.unpack(">h", self.split_buffer(2))[0]

    def parse_int(self):
        return struct.unpack(">i", self.split_buffer(4))[0]

    def parse_long(self):
        return struct.unpack(">q", self.split_buffer(8))[0]

    def parse_float(self):
        return struct.unpack(">f", self.split_buffer(4))[0]
    
    def parse_double(self):
        return struct.unpack(">d", self.split_buffer(8))[0]
    
    def parse_typed_tag(self, tag_type, is_unnamed):
        match tag_type:
            case TagType.TAG_END.value:
                return Tag.TagEnd()
            case TagType.TAG_BYTE.value:
                current_tag = self.parse_byte_tag(is_unnamed)
            case TagType.TAG_SHORT.value:
                current_tag = self.parse_short_tag(is_unnamed)
            case TagType.TAG_INT.value:
                current_tag = self.parse_int_tag(is_unnamed)
            case TagType.TAG_LONG.value:
                current_tag = self.parse_long_tag(is_unnamed)
            case TagType.TAG_FLOAT.value:
                current_tag = self.parse_float_tag(is_unnamed)
            case TagType.TAG_DOUBLE.value:
                current_tag = self.parse_double_tag(is_unnamed)
            case TagType.TAG_BYTE_ARRAY.value:
                current_tag = self.parse_byte_array_tag(is_unnamed)
            case TagType.TAG_STRING.value:
                current_tag = self.parse_string_tag(is_unnamed)
            case TagType.TAG_LIST.value:
                current_tag = self.parse_list_tag(is_unnamed)
            case TagType.TAG_COMPOUND.value:
                current_tag = self.parse_compound_tag(is_unnamed)
            case _:
                # TODO: custom exception
                raise Exception(f"Unknown tag type -> TAG_TYPE {tag_type}")
        
        return current_tag
    
    def parse_tag(self, is_unnamed) -> Tag.Tag:
        tag_type = self.parse_byte()
            
        return self.parse_typed_tag(tag_type, is_unnamed)

    def parse_compound_tag(self, is_unnamed) -> Tag.TagCompound:
        name = self.parse_name() if not is_unnamed else ""
        compound_tag = Tag.TagCompound(name)
        
        while True:
            current_tag = self.parse_tag(False)
            
            if type(current_tag) == Tag.TagEnd:
                return compound_tag
            
            compound_tag.append(current_tag)
    
    def parse_byte_tag(self, is_unnamed):
        name = self.parse_name() if not is_unnamed else ""
        value = self.parse_byte()
        
        return Tag.TagByte(name, value)
    
    def parse_short_tag(self, is_unnamed):
        name = self.parse_name() if not is_unnamed else ""
        value = self.parse_short()
        
        return Tag.TagShort(name, value)
    
    def parse_int_tag(self, is_unnamed):
        name = self.parse_name() if not is_unnamed else ""
        value = self.parse_int()
        
        return Tag.TagInt(name, value)
    
    def parse_long_tag(self, is_unnamed):
        name = self.parse_name() if not is_unnamed else ""
        value = self.parse_long()
        
        return Tag.TagLong(name, value)
    
    def parse_float_tag(self, is_unnamed):
        name = self.parse_name() if not is_unnamed else ""
        value = self.parse_float()
        
        return Tag.TagFloat(name, value)
    
    def parse_double_tag(self, is_unnamed):
        name = self.parse_name() if not is_unnamed else ""
        value = self.parse_double()
        
        return Tag.TagDouble(name, value)
    
    def parse_byte_array_tag(self, is_unnamed):
        name = self.parse_name() if not is_unnamed else ""
        length = self.parse_int()
        value = struct.unpack(f">{length}s", self.split_buffer(length))[0]
        
        return Tag.TagByteArray(name, Tag.TagInt("", length), value)
            
    def parse_string_tag(self, is_unnamed):
        name = self.parse_name() if not is_unnamed else ""
        length = self.parse_short()
        value = struct.unpack(f">{length}s", self.split_buffer(length))[0]

        return Tag.TagString(name, Tag.TagShort("", length), value.decode())
    
    def parse_list_tag(self, is_unnamed):
        name = self.parse_name() if not is_unnamed else ""
        tag_id = self.parse_byte()
        length = self.parse_int()
        tags = []
        
        for _ in range(length):
            current_tag = self.parse_typed_tag(tag_id, True)
            
            tags.append(current_tag)
        
        return Tag.TagList(name, Tag.TagByte("", tag_id), Tag.TagInt("", length), tags)
