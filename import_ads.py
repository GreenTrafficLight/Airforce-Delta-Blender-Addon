import bpy
import bmesh

import gzip
import os
import struct

from math import *
from mathutils import *

from .nnmh import *

from .Utilities import *
from .Blender import*

def build_nnhm(nnhm):

    for pof0 in nnhm.pof0_list:

        index = 0

        for njlm in pof0.njlm_list:

            build_njlm(njlm, index)

            index += 1

        for njhm in pof0.njhm_list:

            build_njhm(njhm, index)

            index +=1

def build_njlm(njlm, njlm_index):

    bpy.ops.object.add(type="ARMATURE")
    ob = bpy.context.object
    ob.rotation_euler = ( radians(90), 0, 0 )
    ob.name = str(njlm_index)

    amt = ob.data
    amt.name = str(njlm_index)

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

        faces = StripToTriangle(njlm_mesh.indices)

        # Set faces
        for j in range(0, len(faces)):
            try:
                face = bm.faces.new([vertexList[faces[j][0] + last_vertex_count], vertexList[faces[j][1] + last_vertex_count], vertexList[faces[j][2] + last_vertex_count]])
                face.smooth = True
                facesList.append([face, [vertexList[faces[j][0] + last_vertex_count], vertexList[faces[j][1] + last_vertex_count], vertexList[faces[j][2]] + last_vertex_count]])
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

def build_njhm(njhm, njhm_index):

    bpy.ops.object.add(type="ARMATURE")
    ob = bpy.context.object
    #ob.rotation_euler = ( radians(90), 0, 0 )
    ob.name = str(njhm_index)

    amt = ob.data
    amt.name = str(njhm_index)

    mesh_index = 0

    for njhm_mesh in njhm.meshes:

        
        if njhm_mesh[1] != []:
            empty = add_empty(str(mesh_index), ob, njhm_mesh[1][-1].translation, njhm_mesh[1][-1].rotation, njhm_mesh[1][-1].scale)
            empty.scale = njhm_mesh[1][-1].scale
        else:
            empty = add_empty(str(mesh_index), ob)
        
        #empty = add_empty(str(mesh_index), ob)

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
        for j in range(len(njhm_mesh[0].vertices["positions"])):
            vertex = bm.verts.new(njhm_mesh[0].vertices["positions"][j])

            if njhm_mesh[0].vertices["normals"] != []:
                vertex.normal = njhm_mesh[0].vertices["normals"][j]
                normals.append(njhm_mesh[0].vertices["normals"][j])
                        
            vertex.index = last_vertex_count + j

            vertexList[last_vertex_count + j] = vertex

        # Set faces
        for j in range(0, len(njhm_mesh[0].indices)):
            try:
                face = bm.faces.new([vertexList[njhm_mesh[0].indices[j][0] + last_vertex_count], vertexList[njhm_mesh[0].indices[j][1] + last_vertex_count], vertexList[njhm_mesh[0].indices[j][2] + last_vertex_count]])
                face.smooth = True
                facesList.append([face, [vertexList[njhm_mesh[0].indices[j][0] + last_vertex_count], vertexList[njhm_mesh[0].indices[j][1] + last_vertex_count], vertexList[njhm_mesh[0].indices[j][2]] + last_vertex_count]])
            except:
                pass

        if njhm_mesh[0].vertices["uvs"] != []:

            uv_name = "UV1Map"
            uv_layer1 = bm.loops.layers.uv.get(uv_name) or bm.loops.layers.uv.new(uv_name)

            for f in bm.faces:
                for l in f.loops:
                    if l.vert.index >= last_vertex_count:
                        l[uv_layer1].uv = [njhm_mesh[0].vertices["uvs"][l.vert.index - last_vertex_count][0], 1 - njhm_mesh[0].vertices["uvs"][l.vert.index - last_vertex_count][1]]
            
        bm.to_mesh(mesh)
        bm.free()

        # Set normals
        mesh.use_auto_smooth = True

        if normals != []:
            try:
                mesh.normals_split_custom_set_from_vertices(normals)
            except:
                pass

        last_vertex_count += len(njhm_mesh[0].vertices["positions"])

        mesh_index += 1


def main(filepath, clear_scene):
    if clear_scene:
        clearScene()

    file = open(filepath, 'rb')
    filename =  filepath.split("\\")[-1]
    file_extension =  os.path.splitext(filepath)[1]
    file_size = os.path.getsize(filepath)

    br = BinaryReader(file, "<")

    if file_extension == ".nj":

        header = br.bytesToString(br.readBytes(4)).replace("\0", "")

        if header == "NNMH":

            nnhm = NNMH()
            nnhm.read(br, file_size)
            build_nnhm(nnhm)

    