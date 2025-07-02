import hou
import toolutils

node = hou.selectedNodes()[0]

p = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
position = p.selectPosition()

pane = toolutils.activePane(kwargs)
context_path = pane.pwd().path()

subnet = hou.node(context_path).createNode('subnet', 'LAY_EDIT')
subnet.setPosition(position)
subnet.setColor(hou.Color((0.4, 0.3, 0.7)))

def create_node(parent_node, node_type, node_name):
    node = parent_node.createNode(node_type, node_name)
    return node
     
#===================switch==========================   
switch_type = node.parm("switch_type").eval()
    
switch_node = subnet.createNode("switch",f"{switch_type}")
switch_node.parm("chooseinputbyname").set(1)
switch_node.parm("selectinputname").set(f"`@{switch_type}`")
switch_node.parm("badinput").set("fallback")
switch_node.parm("selectfallbackname").set("default_product")

products = {}

default_node = create_node(subnet, "null", "default_product")
ref_in = hou.item(subnet.path() + "/1")
default_node.setInput(0, ref_in)
switch_node.setInput(0, default_node)
switch_node.setEditableInputString(0, 'inputname', "")

for i in range(node.parm("products").eval()):
    prim_path = node.parm(f"prim_{i+1}").eval()
    prim_name_ref = prim_path.split("/")[-1]
    products[prim_name_ref] = prim_path
    
    null_prim = create_node(subnet, "null", prim_name_ref)
    null_prim.setInput(0, ref_in)
    switch_node.setNextInput(null_prim)
    switch_node.setEditableInputString(i+1, 'inputname', prim_path)
        
output_node = hou.node(subnet.path() + "/output0")
output_node.setInput(0, switch_node)

subnet.layoutChildren()

print("Switch network created")
