from .Utilities import *

from .nnmh import *

class NJVR:

    def __init__(self) -> None:
        
        self.size = 0

        
        self.nnmhs = []

    def read(self, br, file_size):

        br.readFloat()
        br.readUInt()
        br.readUInt()

        table_entries = []
        for i in range(256):
            table_entries.append((br.readUInt(), br.readUInt()))

        for table_entry in table_entries:

            for i in range(table_entry[0]):

                br.readBytes(32)

        subheader = ""

        while br.tell() < file_size:

            subheader += br.bytesToString(br.readBytes(1)).replace("\0", "")

            if "NNMH" in subheader:
                
                print(br.tell())
                nnmh = NNMH()
                nnmh.read(br, file_size)
                subheader = ""
                self.nnmhs.append(nnmh)

        print(br.tell())