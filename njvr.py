from .Utilities import *

class NJVR:

    def __init__(self) -> None:
        
        self.size = 0

        self.table_entries = []
        self.nnmhs = []

    def read(self, br):

        br.readFloat()
        br.readUInt()
        br.readUInt()

        for i in range(256):
            self.table_entries.append((br.readUInt(), br.readUInt()))