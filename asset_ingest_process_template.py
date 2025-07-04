import hou
import os

ASSET_ROOT = "/vfx/sandbox/felipepesantez/HoudiniDev/asset_ingest_pipe_dev/assets/"
TEMPLATE_HIP = "/vfx/sandbox/felipepesantez/HoudiniDev/asset_ingest_pipe_dev/asset_process_template_v001.hip"
OUTPUT_DIR = "/vfx/sandbox/felipepesantez/HoudiniDev/asset_ingest_pipe_dev/exports/"
    
EXPORT_NODE_PATH = "/stage/componentoutput1" 
GEOMETRY_NODE_PATH = "/stage/componentgeometry1/sopnet/geo/file1" 
FBX_NODE_PATH = "/stage/componentgeometry1/sopnet/geo/fbxcharacterimport1" 
SWITCH_NODE_PATH = "/stage/componentgeometry1/sopnet/geo/geom_type"

MAT_REF_NODE = "/stage/componentgeometry1/sopnet/geo/IN_GEO"
MATLIB_NODE = "/stage/materiallibrary1"

#print(os.listdir(ASSET_ROOT))
hou.hipFile.load(TEMPLATE_HIP, suppress_save_prompt=True)

#set material based on the shopmaterial path attr
def set_material_path(source_node, dest_node):
   mat_ref_node = hou.node(source_node)
   mat_lib_node = hou.node(dest_node)

   geom_ref = mat_ref_node.geometry()
   shopmaterial_attr = list(set(geom_ref.primStringAttribValues('shop_materialpath')))[0]
   mat_lib_node.parm('matnode1').set(shopmaterial_attr)

#set_material_path(source_node=MAT_REF_NODE, dest_node=MATLIB_NODE)

def _find_geo_file(folder):
    for file in os.listdir(folder):
        if file.lower().endswith(".fbx") or file.lower().endswith(".obj"):
            return os.path.join(folder, file)
    return None

def geom_type_process(find_geo_fn, asset_path, switch_node):
    geo_file = find_geo_fn(asset_path)
    if not geo_file:
        print(f"No geometry file found in {asset_path}")
        return

    if geo_file.lower().endswith(".fbx"):
        file_node = hou.node(FBX_NODE_PATH)
        file_node.parm("fbxfile").set(geo_file)
        switch_node.parm("input").set(0)
        print(f"Processed: FBX file {geo_file}")
    elif geo_file.lower().endswith(".obj"):
        file_node = hou.node(GEOMETRY_NODE_PATH)
        file_node.parm("file").set(geo_file)
        switch_node.parm("input").set(1) 
        print(f"Processed: OBJ file {geo_file}")
    
def process_asset(asset_path, export=False):
    switch_node = hou.node(SWITCH_NODE_PATH)
    geom_type_process(_find_geo_file, asset_path, switch_node)
    set_material_path(source_node=MAT_REF_NODE, dest_node=MATLIB_NODE)

    # Optional: set other parameters
    # e.g., hou.node("/obj/geo1/polyreduce1").parm("percentage").set(50)

    asset_name = asset_path.split("/")[-1]
    # Optional: export or save
    if export:
        output_node = hou.node(EXPORT_NODE_PATH)
        if output_node:
            output_node.parm("name").set(asset_name)
            output_node.parm("lopoutput").set(f'{OUTPUT_DIR}`chs("name")`/`chs("filename")`')
            output_node.parm("executebackground").pressButton()

        print(f"Exported: {asset_name}.usd")

def main():
    for subfolder in os.listdir(ASSET_ROOT):
        folder_path = os.path.join(ASSET_ROOT, subfolder)
        if os.path.isdir(folder_path):
            process_asset(folder_path, export=True)

if __name__ == "__main__":
    main()
