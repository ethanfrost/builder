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
        self.report({'INFO'}, 'Exceution succesful')
        return {'FINISHED'}

def create_object(self, context):
    
    # Deselect all objects before adding window object
    
    objects = context.scene.objects
    
    for ob in objects:
        ob.select = False
    
    # Add the window object
    
    mesh = bpy.data.meshes.new('WindowMesh')
    mesh_object = bpy.data.objects.new('Window', mesh)
    context.scene.objects.link(mesh_object)
    mesh_object.location = context.scene.cursor_location
    
    mesh_object.window_property.add()
    
    w = mesh_object.window_property[0].window_frame_width / 2
    h = mesh_object.window_property[0].window_frame_height / 2
    d = mesh_object.window_property[0].window_frame_depth / 2
    t = mesh_object.window_property[0].window_frame_thickness
    
    vertices = [
                (-w, -d, h),
                (w, -d, h),
                (w, -d, -h),
                (-w, -d, -h),
                (-w+t, -d, h-t),
                (w-t, -d, h-t),
                (w-t, -d, -h+t),
                (-w+t, -d, -h+t),
                (-w, d, h),
                (w, d, h),
                (w, d, -h),
                (-w, d, -h),
                (-w+t, d, h-t),
                (w-t, d, h-t),
                (w-t, d, -h+t),
                (-w+t, d, -h+t)
    ]
    
    faces = [
            (0, 4, 5, 1),
            (1, 5, 6, 2),
            (2, 6, 7, 3),
            (3, 7, 4, 0),
            (8, 12, 13, 9),
            (9, 13, 14, 10),
            (10, 14, 15, 11),
            (11, 15, 12, 8),
            (0, 1, 9, 8),
            (1, 2, 10, 9),
            (2, 3, 11, 10),
            (3, 0, 8, 11),
            (4, 12, 13, 5),
            (5, 13, 14, 6),
            (7, 6, 14, 15),
            (4, 7, 15, 12)
    ]
    
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    mesh_object.select = True
    context.scene.objects.active = mesh_object

def update_object(self, context):
    
    # Update the old mesh with the updated window attributes
    
    ob = context.object
    
    # Deselect all objects
    
    objects = context.scene.objects
    
    for o in objects:
        o.select = False
    
    oldmesh = ob.data
    oldname = ob.data.name
    temp_mesh = bpy.data.meshes.new(oldname + 'temp')
    
    w = ob.window_property[0].window_frame_width / 2
    h = ob.window_property[0].window_frame_height / 2
    d = ob.window_property[0].window_frame_depth / 2
    t = ob.window_property[0].window_frame_thickness
    
    vertices = [
                (-w, -d, h),
                (w, -d, h),
                (w, -d, -h),
                (-w, -d, -h),
                (-w+t, -d, h-t),
                (w-t, -d, h-t),
                (w-t, -d, -h+t),
                (-w+t, -d, -h+t),
                (-w, d, h),
                (w, d, h),
                (w, d, -h),
                (-w, d, -h),
                (-w+t, d, h-t),
                (w-t, d, h-t),
                (w-t, d, -h+t),
                (-w+t, d, -h+t)
    ]
    
    faces = [
            (0, 4, 5, 1),
            (1, 5, 6, 2),
            (2, 6, 7, 3),
            (3, 7, 4, 0),
            (8, 12, 13, 9),
            (9, 13, 14, 10),
            (10, 14, 15, 11),
            (11, 15, 12, 8),
            (0, 1, 9, 8),
            (1, 2, 10, 9),
            (2, 3, 11, 10),
            (3, 0, 8, 11),
            (4, 12, 13, 5),
            (5, 13, 14, 6),
            (7, 6, 14, 15),
            (4, 7, 15, 12)
    ]
    
    temp_mesh.from_pydata(vertices, [], faces)
    temp_mesh.update()
    ob.data = temp_mesh
    bpy.data.meshes.remove(oldmesh)
    temp_mesh.name = oldname
    
    ob.select = True
    context.scene.objects.active = ob

class WindowProperty(bpy.types.PropertyGroup):
    
    window_frame_width = bpy.props.FloatProperty(name = 'Window Width', default = 6.0, min = 1.0, max = 100.0, update = update_object, description = 'Width of the window')
    window_frame_height = bpy.props.FloatProperty(name = 'Window Height', default = 2.0, min = 1.0, max = 100.0, update = update_object, description = 'Height of the window')
    window_frame_thickness = bpy.props.FloatProperty(name = 'Window Thickness', default = 0.2, min = 0.1, max = 100.0, update = update_object, description = 'Thickness of the window')
    window_frame_depth = bpy.props.FloatProperty(name = 'Window Depth', default = 0.4, min = 0.1, max = 100.0, update = update_object, description = 'Depth of the window')
    
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
    
    @classmethod
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
            if 'window_property' not in ob:
                return
        except:
            return
        
        layout = self.layout
        window_properties = ob.window_property[0]
        
        layout.prop(window_properties, 'window_frame_width')
        layout.prop(window_properties, 'window_frame_height')
        layout.prop(window_properties, 'window_frame_depth')
        layout.prop(window_properties, 'window_frame_thickness')
