from .Utilities import *

from .pof0 import *

class NNMH:

    def __init__(self) -> None:
        
        self.header_size = 0
        self.size = 0

        self.pof0_list = []

    def read(self, br, file_size, xbox_version = False):

        self.header_size = br.readUInt()
        header_position = br.tell()
        br.readUShort()
        type1 = br.readUByte()
        type2 = br.readUByte()
        self.size = br.readUInt()

        br.seek(header_position + self.header_size, 0)

        while br.tell() < file_size:

            subheader = br.bytesToString(br.readBytes(4)).replace("\0", "")

            if subheader == "POF0":
                pof0 = POF0()
                pof0.read(br, xbox_version)
                self.pof0_list.append(pof0)

            #print(br.tell())

