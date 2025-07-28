import hou
import os
from pxr import Usd, UsdGeom, Sdf
import sys

parent_path = hou.pwd().parent().path()
mat_node = hou.node("/stage/materiallibrary")
mtlx_ref_tmp = hou.node('/stage/materiallibrary/mtlxmaterial')

texture_structure = {}

#reference for textures on disk
ref_dir = hou.node(parent_path + "/usd_ref").parm("filepath1").eval().replace('"','')
textures_ref_dir = "/".join(ref_dir.split("/")[:-1]) + "/resources/textures"
texture_files = [file for file in os.listdir(textures_ref_dir) if file.endswith(".exr") or file.endswith(".png")]

#asset components
ref_stage = hou.node(parent_path + "/sop_stage").stage()
xform_ref = [prim for prim in ref_stage.Traverse() if prim.IsA(UsdGeom.Xform)][0]
prim = ref_stage.GetPrimAtPath(f"{xform_ref.GetPath()}/geometry")
asset_components = [child for child in prim.GetChildren() if child.IsA(UsdGeom.Mesh)]
tmp_asset_map = {child.GetName().lower(): child.GetPath() for child in prim.GetChildren() if child.IsA(UsdGeom.Mesh)}

#TODO: refactor these temporary bad loops for initial test
for component in asset_components:
    texture_structure[component.GetName().lower()] = []

for k,v in texture_structure.items():
    for texture in texture_files:
        if k.replace("_","") in texture.replace("_",""):
            texture_structure[k].append(texture)

def add_mtlx_texture(
    parent, 
    name, 
    file_path, 
    output_name="out"):
    """
    Adds a mtlxtexture node to read the texture files on disk
    Args:
        parent: the parent node mtlx builder subnet
        name: the name for the mtlximage node
        file_path: the file path for the texture on disk
        output_name: the name of the output on the mtlximage node
    Returns:
        the new mtlximage node created with the file parameter set to read the texture file
    """
    tex_node = parent.createNode("mtlximage", name)
    tex_node.parm("file").set(file_path)
    #tex_node.setPosition(stdsurf.position() + hou.Vector2(-2, -len(parent.children())))
    return tex_node

#matlib LOP main UI
mat_node.parm("materials").set(len(asset_components))    
    
i = 0

for component, textures in texture_structure.items():
    i += 1
    
    new_node = mtlx_ref_tmp.copyTo(mat_node)
    new_node.setName(f"{component}" + "_mtl", unique_name=True)
    new_node.moveToGoodPosition()
    
    stdsurf = hou.node(new_node.path() + "/mtlxstandard_surface")
    stdsurf_inputs_map = stdsurf.inputNames()
    
    #assuming all bottles, droplets and ice will have these default values 
    if not "artwork" in component:
        if "droplet" in component or "bottle" in component or "bubble" in component or "liquid" in component:
            stdsurf.parm("base").set(0)
            stdsurf.parm("transmission").set(0.99)
    
    for texture in textures:
        #print(texture)
        #print(component)
        if texture.startswith("_artwork") and component == "bottle":
            continue
        for in_name in stdsurf_inputs_map:
            if in_name == "base":
                continue
            
            texture_name = texture.replace("_","").split("-")[-1][:-4]
            
            if in_name.replace("_","") == texture_name:
                texture_full_path = os.path.join(textures_ref_dir, texture)
                mtlx_texture_node = add_mtlx_texture(new_node, in_name, texture_full_path)
                
                if texture_name == "normal":
                    normal_node = new_node.createNode("mtlxnormalmap")
                    normal_node.setNamedInput("in", mtlx_texture_node, "out")
                    has_normal_map = True
                    stdsurf.setNamedInput("normal", normal_node, "out") 
                else:
                    stdsurf.setNamedInput(in_name, mtlx_texture_node, "out")
    new_node.layoutChildren()
                    
    mat_node.parm(f"matnode{i}").set(new_node.name())
    mat_node.parm(f"geopath{i}").set(str(tmp_asset_map[component]))
    mat_node.parm(f"matpath{i}").set(f"{xform_ref.GetPath()}/Look/{new_node.name()}")
    
    
