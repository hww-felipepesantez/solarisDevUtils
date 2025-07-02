from pxr import Usd, UsdGeom, Sdf
 
nodes = hou.selectedNodes()
prims_with_id = {}
 
def process_prim(prim, val):
    if prim.IsA(UsdGeom.Mesh):        
        primvars_api = UsdGeom.PrimvarsAPI(prim)
        if primvars_api.HasPrimvar("multimatte_id"):
            primvar = primvars_api.GetPrimvar("multimatte_id")
            value = primvar.Get()
            if value == val:
                prims_with_id[prim] = value  
    for child in prim.GetChildren():
        process_prim(child, val)
 
for node in nodes:
    stage = node.stage()
    root_prim = stage.GetPrimAtPath("/")
    matte_val = 1
    process_prim(root_prim, matte_val)
    
def print_hash(hash):
    for k,v in hash.items():
        print(f"Prim: {k.GetPrimPath()} -> Multimatte Value: {v}")
        print("-------------------------")
    print("===============================================================")
    
print("===============================================================")    
print_hash(prims_with_id)
