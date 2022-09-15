from .Utilities import *

class NJTL:

    def __init__(self) -> None:
        
        self.size = 0

        self.table_entries = []
        self.names = []

    class TABLE_ENTRY:

        def __init__(self) -> None:
            self.offset = 0
            self.unk1 = 0
            self.unk2 = 0

        def read(self, br):
            self.offset = br.readUInt()
            self.unk1 = br.readUInt()
            self.unk2 = br.readUInt()

    def read(self, br):
        self.size = br.readUInt()
        header_position = br.tell()
        br.readUInt()
        count = br.readUInt()

        self.read_table_entries(br, count)

        self.read_names(br, header_position)

        br.seek(header_position + self.size, 0)

    def read_table_entries(self, br, count):

        for i in range(count):
            table_entry = NJTL.TABLE_ENTRY()
            table_entry.read(br)
            self.table_entries.append(table_entry)

    def read_names(self, br, header_position):

        for table_entry in self.table_entries:
            br.seek(table_entry.offset + header_position, 0)
            self.names.append(br.readString())