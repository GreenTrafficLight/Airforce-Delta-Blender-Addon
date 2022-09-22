from mathutils import *
from math import *

from .Utilities import *



class NJHM:

    def __init__(self) -> None:
        
        self.header_position = 0
        self.size = 0

        self.table_entries = []
        
        self.transformations = []
        self.meshes = []
        self.parent_indices = []

    class MESH_TABLE_ENTRY:

        def __init__(self) -> None:
            self.unk1 = 0
            self.offset1 = 0 # offset to mesh table entry
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
            self.offset1 = br.readUInt()
            if self.offset1 == 0 or self.offset1 == 1:
                self.unk3 = br.readUInt()
            else :
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
            self.child_node_offset = 0
            self.sibling_node_offset = 0

        def read(self, br, header_position, xbox_version = False):
            self.node_offset = br.tell() - header_position
            self.unk1 = br.readInt()
            self.unk2 = br.readUInt()
            self.translation = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
            if xbox_version:
                self.rotation = Vector((radians(br.readInt() / 182.044), radians(br.readInt() / 182.044), radians(br.readInt() / 182.044)))
            else:
                self.rotation = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
            self.scale = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
            self.offset1 = br.readUInt() # offset for the 20 unknowns float
            self.child_node_offset = br.readUInt() # offset for child node
            self.sibling_node_offset = br.readUInt() # offset for sibling node
            if self.offset1 != 0:
                (br.readFloat(), br.readFloat(), br.readFloat(), br.readFloat(), br.readFloat())

    class MESH:

        def __init__(self) -> None:
            
            self.vertices = None
            self.indices = []

    def read(self, br, xbox_version = False):
        
        self.size = br.readUInt()
        header_position = br.tell()

        br.seek(header_position + self.size, 0)
        structure_order = self.get_structure_letters(br)

        br.seek(header_position, 0)

        root_transformation_table_entry = None
        meshes_table_entries = []

        table_entry = 0

        transformation_index = -1

        for letters in structure_order:

            if letters == "KAA":
                root_transformation_table_entry = NJHM.TRANSFORMATION_TABLE_ENTRY()
                root_transformation_table_entry.read(br, header_position, xbox_version)

            elif letters == "LAA":
                transformation_table_entry = NJHM.TRANSFORMATION_TABLE_ENTRY()
                transformation_table_entry.read(br, header_position, xbox_version)

                self.transformations.append(transformation_table_entry)

                transformation_index += 1

            elif letters == "G":
                meshes_table_entries = []

            elif "V" in letters:

                for i in range(len(letters)):
                    
                    print(str(table_entry) + " " + "start : " + str(br.tell()))   
                    mesh_table_entry = NJHM.MESH_TABLE_ENTRY()
                    mesh_table_entry.read(br)
                    print(str(table_entry) + " " + "end : " + str(br.tell()))   
                         
                    meshes_table_entries.append(mesh_table_entry)
                
                table_entry += 1
                
                self.table_entries.append((meshes_table_entries, transformation_index))
    
        print(br.tell())   

        index = 0

        for table_entry in self.table_entries:
            
            meshes = []

            for mesh_node in table_entry[0]:

                mesh = NJHM.MESH()
                br.seek(mesh_node.vertex_buffer_offset + header_position, 0)
                mesh.vertices = self.read_vertex(br, mesh_node.face_count * 3)
                mesh.indices = self.get_indices(mesh_node.face_count, xbox_version)
                meshes.append(mesh)

            index += 1

            self.meshes.append((meshes, table_entry[1]))

        for i in range(len(self.transformations)):

            print(str(i) + " : " + str(self.transformations[i].node_offset) + " " + str(self.transformations[i].child_node_offset) + " " + str(self.transformations[i].sibling_node_offset) + " " + str(self.transformations[i].unk1))

        self.parent_indices = [-1 for i in range(len(self.transformations))]

        for i in range(len(self.transformations)):

            child_node_offset = self.transformations[i].child_node_offset

            # If node has child, replace parent indices

            if (child_node_offset != 0):

                for j in range(len(self.transformations)): # 

                    #

                    if (child_node_offset <= self.transformations[j].node_offset):

                        self.parent_indices[j] = i

                        #

                        if (self.transformations[j].sibling_node_offset == 0):

                            break

            

            

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
                structure_order.append("G")
                structure_letters = ""
                
            if structure_letters == "V":
                if "V" in structure_order[-1]:
                    structure_order[-1] += "V"
                else:
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

    def get_indices(self, count, xbox_version = False):

        indices = []

        face_index = 0
        for i in range(count):
            if xbox_version:
                indices.append([face_index+2, face_index+1, face_index])
            else:
                indices.append([face_index, face_index+1, face_index+2])
            face_index += 3

        return indices