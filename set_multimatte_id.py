from pxr import Usd, UsdGeom, Sdf
 
node = hou.pwd()
stage = node.editableStage()
 
root_prim = stage.GetPrimAtPath("path/to/prim_on_stage") #example: /ASSET/geo/render
matte_val = 1
 
def process_prim(prim, val):
    if prim.IsA(UsdGeom.Mesh):
        primvars_api = UsdGeom.PrimvarsAPI(prim)
        primvar = primvars_api.CreatePrimvar('multimatte_id', Sdf.ValueTypeNames.Int)
        primvar.Set(val)
    for child in prim.GetChildren():
        process_prim(child, val)
 
process_prim(root_prim, matte_val)
