from .Utilities import *

class NJHM:

    def __init__(self) -> None:
        
        self.size = 0

    def read(self, br):
        
        self.size = br.readUInt()
