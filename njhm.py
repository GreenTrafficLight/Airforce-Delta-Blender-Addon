from mathutils import *

from .Utilities import *

class NJHM:

    def __init__(self) -> None:
        
        self.header_position = 0
        self.size = 0

        self.table_entries = []
        self.transformations = []

        self.meshes = []

    class MESH_TABLE_ENTRY:

        def __init__(self) -> None:
            self.unk1 = 0
            self.unk2 = 0
            self.unk3 = 0
            self.unk4 = None
            self.unk5 = None
            self.unk6 = None
            self.unk7 = 0
            self.face_count = 0
            self.vertex_count = 0
            self.stride = 0
            self.face_buffer_offset = 0
            self.unk8 = 0
            self.unk9 = 0

        def read(self, br):
            self.unk1 = br.readUInt()
            if self.unk1 != 8 and self.unk1 != 4:
                self.unk2 = br.readUInt()
                self.unk3 = br.readUInt()
            self.unk4 = br.readUInt()
            self.unk5 = br.readUInt()
            self.unk6 = (br.readFloat(), br.readFloat(), br.readFloat(), br.readFloat())
            self.unk7 = (br.readFloat(), br.readFloat(), br.readFloat(), br.readFloat())
            self.unk8 = (br.readFloat(), br.readFloat(), br.readFloat(), br.readFloat())
            self.unk9 = br.readUInt()
            self.vertex_count = br.readUInt()
            self.face_count = br.readUInt()
            self.stride = br.readUInt()
            self.face_buffer_offset = br.readUInt()
            self.unk10 = br.readUInt()
            self.vertex_buffer_offset = br.readUInt()

    class TRANSFORMATION_TABLE_ENTRY:

        def __init__(self) -> None:
            self.unk1 = 0
            self.unk2 = 0
            self.rotation = None
            self.scale = None
            self.offset1 = 0
            self.offset2 = 0
            self.offset3 = 0

        def read(self, br):
            self.unk1 = br.readInt()
            self.unk2 = br.readUInt()
            self.translation = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
            self.rotation = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
            self.scale = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
            self.offset1 = br.readUInt() # offset for the 20 unknowns float
            self.offset2 = br.readUInt() # offset for child node ?
            self.offset3 = br.readUInt() # offset for ?
            if self.offset1 != 0:
                (br.readFloat(), br.readFloat(), br.readFloat(), br.readFloat(), br.readFloat())

    class MESH:

        def __init__(self) -> None:
            
            self.vertices = None
            self.indices = []

    def read(self, br):
        
        self.size = br.readUInt()
        header_position = br.tell()

        br.seek(header_position + self.size, 0)
        structure_order = self.get_structure_letters(br)

        br.seek(header_position, 0)

        transformation_table_entries = []

        table_entry = 0

        for letters in structure_order:

            if letters == "KAA":
                transformation_table_entry = NJHM.TRANSFORMATION_TABLE_ENTRY()
                transformation_table_entry.read(br)

                transformation_table_entries.append(transformation_table_entry)

            elif letters == "LAA":
                transformation_table_entry = NJHM.TRANSFORMATION_TABLE_ENTRY()
                transformation_table_entry.read(br)

                transformation_table_entries.append(transformation_table_entry)

            elif letters == "V":
                print(str(table_entry) + " " + "start : " + str(br.tell()))   
                mesh_table_entry = NJHM.MESH_TABLE_ENTRY()
                mesh_table_entry.read(br)
                print(str(table_entry) + " " + "end : " + str(br.tell()))   
                table_entry += 1
                
                self.table_entries.append((mesh_table_entry, transformation_table_entries))

                transformation_table_entries = []
    
        print(br.tell())   

        for table_entry in self.table_entries:
            mesh = NJHM.MESH()
            br.seek(table_entry[0].vertex_buffer_offset + header_position, 0)
            mesh.vertices = self.read_vertex(br, table_entry[0].face_count * 3)
            mesh.indices = self.get_indices(table_entry[0].face_count)
            self.meshes.append((mesh, table_entry[1]))

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

    def read_vertex(self, br, count):

        vertices = {
            "positions" : [],
            "normals": [],
            "uvs" : [],
        }

        for i in range(count):

            vertices["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
            vertices["normals"].append([br.readFloat(), br.readFloat(), br.readFloat()])
            vertices["uvs"].append([br.readFloat(), br.readFloat()])

        return vertices

    def get_indices(self, count):

        indices = []

        face_index = 0
        for i in range(count):
            indices.append([face_index, face_index+1, face_index+2])
            face_index += 3

        return indices