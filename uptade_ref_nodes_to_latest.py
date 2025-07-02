import hou
import os

nodes = hou.selectedNodes()

def update_to_latest_version(node):
    parm_ref = node.parm('filepath1')
    ref_dir = "/".join(parm_ref.eval().split("/")[:-2])
    versions = sorted(os.listdir(ref_dir))
    latest_version = versions[-1]
    new_root_path = os.path.join(ref_dir, latest_version)
    latest_usd_file = os.listdir(new_root_path)[0]
    new_version_path = os.path.join(new_root_path, latest_usd_file)
    
    constructed_name = "hww_" + latest_usd_file.replace("3d_layout","assetLayout").replace(".usd","")
    parm_ref.set(new_version_path)
    node.setName(constructed_name)
    
    print("Switched to USD file: ", latest_usd_file)
    
for node in nodes:    
    update_to_latest_version(node)
