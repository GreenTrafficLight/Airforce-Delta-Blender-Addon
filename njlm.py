from .Utilities import *

class NJLM:

    def __init__(self) -> None:

        self.size = 0

        self.tables_entries = []

        self.meshes = []

    class TABLE_ENTRY:

        def __init__(self) -> None:
            self.unk1 = 0
            self.unk2 = 0
            self.unk3 = 0
            self.unk4 = None
            self.unk5 = None
            self.unk6 = None
            self.unk7 = 0
            self.vertex_count = 0
            self.face_count = 0
            self.unk8 = 0
            self.face_buffer_offset = 0

        def read(self, br):
            self.unk1 = br.readUInt()
            self.unk2 = br.readUInt()
            self.unk3 = br.readUInt()
            self.unk4 = (br.readFloat(), br.readFloat(), br.readFloat(), br.readFloat())
            self.unk5 = (br.readFloat(), br.readFloat(), br.readFloat(), br.readFloat())
            self.unk6 = (br.readFloat(), br.readFloat(), br.readFloat(), br.readFloat())
            self.unk7 = br.readUInt()
            self.vertex_count = br.readUInt()
            self.face_count = br.readUInt() + 2
            self.unk8 = br.readUInt()
            self.face_buffer_offset = br.readUInt() * 2

    class MESH:

        def __init__(self) -> None:
            
            self.vertices = None
            self.indices = []

    def read(self, br, xbox_version = False):
        self.size = br.readUInt()
        header_position = br.tell()
        br.readBytes(112)
        
        table_count = br.readUInt()
        vertex_count = br.readUInt()
        face_count = br.readUInt()
        br.readUInt()
        br.readUInt()
        vertex_buffer_offset = br.readUInt()
        face_buffer_offset = br.readUInt()
        br.readUInt()

        self.read_table_entries(br, table_count)

        for table_entry in self.tables_entries:
            mesh = NJLM.MESH()
            br.seek(vertex_buffer_offset + header_position, 0)
            mesh.vertices = self.read_vertex(br, table_entry.vertex_count)
            br.seek(face_buffer_offset + header_position, 0)
            mesh.indices = self.read_indices(br, table_entry.face_buffer_offset, table_entry.face_count, xbox_version)
            self.meshes.append(mesh)

        br.seek(header_position + self.size, 0)
            
    def read_table_entries(self, br, count):

        for i in range(count):
            table_entry = NJLM.TABLE_ENTRY()
            table_entry.read(br)
            self.tables_entries.append(table_entry)

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

    def read_indices(self, br, offset, count, xbox_version = False):

        indices = []

        br.seek(offset, 1)
        for i in range(count):
            indices.append(br.readUShort())

        if xbox_version:
            indices = StripToTriangle(indices, True)
        else:
            indices = StripToTriangle(indices)

        return indices


