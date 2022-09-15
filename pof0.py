from .Utilities import *

from .njhm import *
from .njlm import *
from .njtl import *
import njhm

class POF0:

    def __init__(self) -> None:
    
        self.header_size = 0
        self.size = 0

        self.njtl_list = []
        self.njlm_list = []

    def read(self, br):

        self.header_size = br.readUInt()
        header_position = br.tell()

        if self.header_size != 0:

            br.readUInt()

        br.seek(header_position + self.header_size, 0)

        subheader = br.bytesToString(br.readBytes(4)).replace("\0", "")

        if subheader == "NJTL":
            njtl = NJTL()
            njtl.read(br)
            self.njtl_list.append(njtl)
        
        elif subheader == "NJLM":
            njlm = NJLM()
            njlm.read(br)
            self.njlm_list.append(njlm)

        elif subheader == "NJHM":
            njhm = NJHM()
            njhm.read(br)

    def get_structure_order(self, br):
        # WTF
        header = br.bytesToString(br.readBytes(4)).replace("\0", "")
        size = br.readUInt()
        structure_order = ""
        for i in range(size):
            structure_order +=  br.bytesToString(br.readBytes(1)).replace("\0", "")




        


