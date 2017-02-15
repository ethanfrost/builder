#-------------------------------------------------
#   File builder_door_builder.py
#-------------------------------------------------

import bpy

class create_door(bpy.types.Operator):
    
    bl_idname = 'mesh.builder_door_builder'
    bl_label = 'Add Door'
    bl_description = 'Add a door object to current scene'
    bl_category = 'Builder'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        print("##")
        return {'FINISHED'}
