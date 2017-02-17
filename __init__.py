#-------------------------------------------------
#   File __init__.py
#-------------------------------------------------

# Add-on info

bl_info = {
    'name':'Builder',
    'author':'Ethan',
    'location':'VIEW_3D > Add > Mesh > Builder',
    'description':'A simple utility for creating architecture entities such as rooms, doors, windows, cabinets',
    'category':'Add Mesh'
}

import os
import sys

path = sys.path
Builder_in_path = False

print("#------------------------------------#")

for i in path:
    if 'builder' in i:
        Builder_in_path = True
if Builder_in_path is False:
    
#    path = os.path.join(os.path.dirname(__file__), '..')
    path = os.path.dirname(__file__)
    print(path)
    sys.path.append(path)

if "bpy" in locals():
    
    import imp
    imp.reload(builder_door_builder)
    imp.reload(builder_floor_builder)
    imp.reload(builder_window_builder)
    print("#---------------------------------#")
    print("Reloaded multifiles")
    print("#---------------------------------#")
    
else:
    
    import builder_door_builder
    import builder_floor_builder
    import builder_window_builder
    print("#---------------------------------#")
    print("Imported multifiles")
    print("#---------------------------------#")

import bpy

class INFO_MT_add_builder_menu(bpy.types.Menu):
    
    bl_idname = "INFO_MT_add_builder_menu"
    bl_label = "Builder"
    
    def draw(self, context):
        
        layout = self.layout
        
        layout.operator('mesh.builder_door_builder', text = 'Add Door', icon = 'PLUGIN')
        layout.operator('mesh.builder_floor_builder', text = 'Add Floor', icon = 'PLUGIN')
        layout.operator('mesh.builder_window_builder', text = 'Add Window', icon = 'PLUGIN')
        
#-------------------------------------------------
#   Draw function for builder main menu
#-------------------------------------------------
        
def BuilderMenuFunc(self, context):
    
    self.layout.menu(INFO_MT_add_builder_menu.bl_idname, icon = "PLUGIN")
    
#-------------------------------------------------
#   Add the menu to INFO_MT_add_mesh menu
#-------------------------------------------------

    
def register():
    
    bpy.utils.register_class(INFO_MT_add_builder_menu)
    bpy.utils.register_class(builder_door_builder.create_door)
    bpy.utils.register_class(builder_floor_builder.create_floor)
    bpy.utils.register_class(builder_window_builder.create_window)
#    bpy.utils.register_class(builder_floor_builder.FloorProperty)
    bpy.utils.register_class(builder_floor_builder.VIEW3D_PT_floor_builder_config)
    bpy.utils.register_class(builder_window_builder.VIEW3D_PT_window_builder_config)
    bpy.types.INFO_MT_mesh_add.append(BuilderMenuFunc)
    
def unregister():
    
    bpy.utils.unregister_class(INFO_MT_add_builder_menu)
    bpy.utils.unregister_class(builder_door_builder.create_door)
    bpy.utils.unregister_class(builder_floor_builder.create_floor)
    bpy.utils.unregister_class(builder_window_builder.create_window)
#    bpy.utils.unregister_class(builder_floor_builder.FloorProperty)
    bpy.utils.unregister_class(builder_floor_builder.VIEW3D_PT_floor_builder_config)
    bpy.utils.unregister_class(builder_window_builder.VIEW3D_PT_window_builder_config)
    bpy.types.INFO_MT_mesh_add.remove(BuilderMenuFunc)
    
if __name__ == '__main__':
    
    register()
    
