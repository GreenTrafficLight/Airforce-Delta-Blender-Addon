from .Utilities import *

class NJHM:

    def __init__(self) -> None:
        
        self.header_position = 0
        self.size = 0

    def read(self, br):
        
        header_position = br.tell()
        self.size = br.readUInt()

        br.seek(header_position + self.size, 0)
        structure_order = self.get_structure_letters(br)

        br.seek(header_position + 4, 0)
        

    def get_structure_letters(self, br):

        # WTF
        header = br.bytesToString(br.readBytes(4)).replace("\0", "")
        size = br.readUInt()
        structure_letters = ""
        structure_order = []
        
        for i in range(size):
            structure_letters +=  br.bytesToString(br.readBytes(1)).replace("\0", "")
            
            if structure_letters == "KAA":
                structure_order.append("KAA")
                structure_letters = ""
            
            if structure_letters == "LAA":
                structure_order.append("LAA")
                structure_letters = ""

            if structure_letters == "G":
                structure_letters = ""
                
            if structure_letters == "V":
                structure_order.append("V")
                structure_letters = ""

        return structure_order
