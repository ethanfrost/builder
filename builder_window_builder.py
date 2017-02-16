#-------------------------------------------------
#   File builder_window_builder.py
#-------------------------------------------------

import bpy

#-------------------------------------------------
#   Create class Window
#-------------------------------------------------

class create_window(bpy.types.Operator):
    
    bl_idname = 'mesh.builder_window_builder'
    bl_label = 'Add Window'
    bl_description = 'Add a window object to current scene'
    bl_options = {'REGISTER', 'UNDO'}
    bl_category = 'Builder'
    
    def draw(self, context):
        
        self.layout.label('Look in the properties panel for more configuration options', icon = 'INFO')
        
    def execute(self, context):
        
        create_object(self, context)
        
        return {'FINISHED'}

def create_object(self, context):
    pass

def update_object(self, context):
    pass

class WindowProperty(bpy.types.PropertyGroup):
    
    window_frame_width = bpy.props.IntProperty(name = 'Window Width', default = 1.0, min = 1.0, max = 100.0, update = update_object, description = 'Width of the window')
    window_frame_height = bpy.props.IntProperty(name = 'Window Height', default = 1.0, min = 1.0, max = 100.0, update = update_object, description = 'Height of the window')
    window_frame_thickness = bpy.props.IntProperty(name = 'Window Thickness', default = 1.0, min = 1.0, max = 100.0, update = update_object, description = 'Thickness of the window')
    window_frame_depth = bpy.props.IntProperty(name = 'Window Depth', default = 1.0, min = 1.0, max = 100.0, update = update_object, description = 'Depth of the window')
    
#-------------------------------------------------
#   Register the property class
#-------------------------------------------------

bpy.utils.register_class(WindowProperty)
bpy.types.Object.window_property = bpy.props.CollectionProperty(type = WindowProperty)

class VIEW3D_PT_window_builder_config(bpy.types.Panel):
    
    bl_idname = 'VIEW3D_PT_window_builder_config'
    bl_label = 'Window Properties'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_description = 'Configure window object'
    bl_category = 'Builder'
    
    @classmethos
    def poll(cls, context):
        ob = context.object
        
        if ob is None:
            return False
        if 'window_property' not in ob:
            return False
        else:
            return True
    
    def draw(self, context):
        
        ob = context.object
        
        try:
            if 'window_propery' not in ob:
                return
        except:
            return
        
        layout = self.layout
        window_properties = ob.window_property[0]
        
        layout.props(window_properties, 'window_frame_width')
        layout.props(window_properties, 'window_frame_height')
        layout.props(window_properties, 'window_frame_depth')
        layout.props(window_properties, 'window_frame_thickness')
