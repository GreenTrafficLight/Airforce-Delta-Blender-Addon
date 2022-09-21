from .Utilities import *

from .nnmh import *

class KAP:

    def __init__(self) -> None:
    
        self.size = 0
        self.header_size = 0

        self.table_entries = []

    class TABLE_ENTRY:

        def __init__(self) -> None:
            
            self.name = ""
            self.header = ""

        def read(self, br):

            self.name = br.bytesToString(br.readBytes(32)).replace("\0", "")
            self.header = br.bytesToString(br.readBytes(4)).replace("\0", "")
            self.size = br.readUInt()
            self.index = br.readUInt()
            self.offset = br.readUInt()

    def read(self, br):

        self.size = br.readUInt()
        table_entry_count = br.readUInt()

        br.seek(32, 0)
        table_entries_offset = br.readUInt()
        self.header_size = br.readUInt()

        br.seek(table_entries_offset, 0)

        for i in range(table_entry_count):
            table_entry = KAP.TABLE_ENTRY()
            table_entry.read(br)
            self.table_entries.append(table_entry)

        br.seek(self.header_size, 0)






            



