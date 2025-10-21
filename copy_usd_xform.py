from pxr import Usd, UsdGeom, Gf

node = hou.pwd()

# Get both stages
stage_a = hou.node(hou.pwd().parm('refstage').eval()).stage()
stage_b = hou.pwd().editableStage()

# Path to the prims
prim_a_path = node.parent().parm("product").eval()
prim_b_path = node.inputs()[0].parm("primpath").eval()

# Get prims
prim_a = stage_a.GetPrimAtPath(prim_a_path)
prim_b = stage_b.GetPrimAtPath(prim_b_path)


if not prim_a or not prim_b:
    raise ValueError("Prim not found on one of the stages.")
    
src_xform = UsdGeom.Xformable(prim_a)
dst_xform = UsdGeom.Xformable(prim_b)


for op in src_xform.GetOrderedXformOps():
    suffix = ""
    if ":" in op.GetOpName():
        parts = op.GetOpName().split(":")
        if len(parts) > 2:
            suffix = parts[-1]
    
    new_op = dst_xform.AddXformOp(
        op.GetOpType(),
        op.GetPrecision(),
        suffix,
        op.IsInverseOp()
    )

    
    time_samples = op.GetTimeSamples()
    if time_samples:
        for t in time_samples:
            new_op.Set(op.Get(t), t)
    else:
        new_op.Set(op.Get())

print("Xform copied")
