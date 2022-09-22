import bpy
import bmesh

import gzip
import os
import struct

from math import *
from mathutils import *

from .nnmh import *
from .kap import *

from .Utilities import *
from .Blender import*

def build_nnhm(nnhm, filename, rotate = False):

    for pof0 in nnhm.pof0_list:

        index = 0

        for njlm in pof0.njlm_list:

            build_njlm(njlm, filename, index)

            index += 1

        for njhm in pof0.njhm_list:

            build_njhm(njhm, filename, index, rotate)

            index +=1

def build_njlm(njlm, filename, njlm_index):

    bpy.ops.object.add(type="ARMATURE")
    ob = bpy.context.object
    ob.rotation_euler = ( radians(90), 0, 0 )
    ob.name = str(filename)

    amt = ob.data
    amt.name = str(filename)

    mesh_index = 0

    for njlm_mesh in njlm.meshes:

        empty = add_empty(str(mesh_index), ob)

        mesh = bpy.data.meshes.new(str(mesh_index))
        obj = bpy.data.objects.new(str(mesh_index), mesh)

        empty.users_collection[0].objects.link(obj)

        obj.parent = empty

        vertexList = {}
        facesList = []
        normals = []

        last_vertex_count = 0

        bm = bmesh.new()
        bm.from_mesh(mesh)

        # Set vertices
        for j in range(len(njlm_mesh.vertices["positions"])):
            vertex = bm.verts.new(njlm_mesh.vertices["positions"][j])

            if njlm_mesh.vertices["normals"] != []:
                vertex.normal = njlm_mesh.vertices["normals"][j]
                normals.append(njlm_mesh.vertices["normals"][j])
                        
            vertex.index = last_vertex_count + j

            vertexList[last_vertex_count + j] = vertex

        # Set faces
        for j in range(0, len(njlm_mesh.indices)):
            try:
                face = bm.faces.new([vertexList[njlm_mesh.indices[j][0] + last_vertex_count], vertexList[njlm_mesh.indices[j][1] + last_vertex_count], vertexList[njlm_mesh.indices[j][2] + last_vertex_count]])
                face.smooth = True
                facesList.append([face, [vertexList[njlm_mesh.indices[j][0] + last_vertex_count], vertexList[njlm_mesh.indices[j][1] + last_vertex_count], vertexList[njlm_mesh.indices[j][2]] + last_vertex_count]])
            except:
                pass

        if njlm_mesh.vertices["uvs"] != []:

            uv_name = "UV1Map"
            uv_layer1 = bm.loops.layers.uv.get(uv_name) or bm.loops.layers.uv.new(uv_name)

            for f in bm.faces:
                for l in f.loops:
                    if l.vert.index >= last_vertex_count:
                        l[uv_layer1].uv = [njlm_mesh.vertices["uvs"][l.vert.index - last_vertex_count][0], 1 - njlm_mesh.vertices["uvs"][l.vert.index - last_vertex_count][1]]
            
        bm.to_mesh(mesh)
        bm.free()

        # Set normals
        mesh.use_auto_smooth = True

        if normals != []:
            try:
                mesh.normals_split_custom_set_from_vertices(normals)
            except:
                pass

        last_vertex_count += len(njlm_mesh.vertices["positions"])

        mesh_index += 1

def build_njhm(njhm, filename, njhm_index, rotate = False):

    bpy.ops.object.add(type="ARMATURE")
    ob = bpy.context.object
    if rotate:
        ob.rotation_euler = ( radians(90), 0, 0 )
    ob.name = str(filename)

    amt = ob.data
    amt.name = str(filename)

    empty_list = []

    for i in range(len(njhm.transformations)):

        transformation = njhm.transformations[i]
        
        empty = add_empty(str(i), ob, transformation.translation, transformation.rotation, transformation.scale)
        empty.scale = transformation.scale
        
        if njhm.parent_indices[i] != -1:

            empty.parent = empty_list[njhm.parent_indices[i]]

        empty_list.append(empty)

    mesh_index = 0

    for mesh_table_entry in njhm.meshes:

        for njhm_mesh in mesh_table_entry[0]:

            empty = empty_list[mesh_table_entry[1]]
            
            mesh = bpy.data.meshes.new(str(mesh_table_entry[1]))
            obj = bpy.data.objects.new(str(mesh_table_entry[1]), mesh)

            empty.users_collection[0].objects.link(obj)

            obj.parent = empty

            vertexList = {}
            facesList = []
            normals = []

            last_vertex_count = 0

            bm = bmesh.new()
            bm.from_mesh(mesh)

            # Set vertices
            for j in range(len(njhm_mesh.vertices["positions"])):
                vertex = bm.verts.new(njhm_mesh.vertices["positions"][j])

                if njhm_mesh.vertices["normals"] != []:
                    vertex.normal = njhm_mesh.vertices["normals"][j]
                    normals.append(njhm_mesh.vertices["normals"][j])
                            
                vertex.index = last_vertex_count + j

                vertexList[last_vertex_count + j] = vertex

            # Set faces
            for j in range(0, len(njhm_mesh.indices)):
                try:
                    face = bm.faces.new([vertexList[njhm_mesh.indices[j][0] + last_vertex_count], vertexList[njhm_mesh.indices[j][1] + last_vertex_count], vertexList[njhm_mesh.indices[j][2] + last_vertex_count]])
                    face.smooth = True
                    facesList.append([face, [vertexList[njhm_mesh.indices[j][0] + last_vertex_count], vertexList[njhm_mesh.indices[j][1] + last_vertex_count], vertexList[njhm_mesh.indices[j][2]] + last_vertex_count]])
                except:
                    pass

            if njhm_mesh.vertices["uvs"] != []:

                uv_name = "UV1Map"
                uv_layer1 = bm.loops.layers.uv.get(uv_name) or bm.loops.layers.uv.new(uv_name)

                for f in bm.faces:
                    for l in f.loops:
                        if l.vert.index >= last_vertex_count:
                            l[uv_layer1].uv = [njhm_mesh.vertices["uvs"][l.vert.index - last_vertex_count][0], 1 - njhm_mesh.vertices["uvs"][l.vert.index - last_vertex_count][1]]
                
            bm.to_mesh(mesh)
            bm.free()

            # Set normals
            mesh.use_auto_smooth = True

            if normals != []:
                try:
                    mesh.normals_split_custom_set_from_vertices(normals)
                except:
                    pass

            last_vertex_count += len(njhm_mesh.vertices["positions"])

        mesh_index += 1


def main(filepath, files, clear_scene):
    if clear_scene:
        clearScene()

    folder = (os.path.dirname(filepath))

    for i, j in enumerate(files):

        path_to_file = (os.path.join(folder, j.name))

        file = open(path_to_file, 'rb')
        filename =  path_to_file.split("\\")[-1]
        file_extension =  os.path.splitext(path_to_file)[1]
        file_size = os.path.getsize(path_to_file)

        br = BinaryReader(file, "<")

        if file_extension == ".nj":

            header = br.bytesToString(br.readBytes(4)).replace("\0", "")

            if header == "NNMH":

                nnmh = NNMH()
                nnmh.read(br, file_size)
                build_nnhm(nnmh, os.path.splitext(filename)[0])

        elif file_extension == ".kap":

            kap = KAP()
            kap.read(br)

            for table_entry in kap.table_entries:

                br.seek(table_entry.offset)

                if table_entry.header == "SK":
                    header = br.bytesToString(br.readBytes(4)).replace("\0", "")
                    nnmh = NNMH()
                    nnmh.read(br, br.tell() + table_entry.size - 4, True)
                    if table_entry.index == 1:
                        build_nnhm(nnmh, table_entry.name, True)
                    else:
                        build_nnhm(nnmh, table_entry.name)

    