#-------------------------------------------------
#   File builder_floor_builder.py
#-------------------------------------------------

import bpy

# Define a variable which holds the reference to the solidify modifier
#ob_modifier = None

class create_floor(bpy.types.Operator):
    
    bl_idname = 'mesh.builder_floor_builder'
    bl_label = 'Add Floor'
    bl_description = 'Add a floor object to current scene'
    bl_category = 'Builder'
    bl_options = {'REGISTER', 'UNDO'}
    
    ob_modifier = None
    
    def draw(self, context):
        
        self.layout.label('Look in the properties panel for more configuration options', icon = 'INFO')
    
    def execute(self, context):
        
#        self.layout.label('Floor', icon = 'OBJECT')
        create_object(self, context)
        self.report({'INFO'}, 'Execution successful')
        return {'FINISHED'}

#-------------------------------------------------
#   create floor object
#-------------------------------------------------

def create_object(self, context):
    
#    global ob_modifier
    # Deselect all objects before adding the floor object
    
    objects = context.scene.objects
    
    for ob in objects:
        
        ob.select = False
    
    # Add the floor object
    
    mesh = bpy.data.meshes.new('FloorMesh')
    mesh_object = bpy.data.objects.new('Floor', mesh)
    context.scene.objects.link(mesh_object)
    mesh_object.location = context.scene.cursor_location
    
    mesh_object.floor_property.add()
    l = mesh_object.floor_property[0].floor_length / 2
    w = mesh_object.floor_property[0].floor_width / 2
    
    vertices = [(-l, w, 0), (l, w, 0), (l, -w, 0), (-l, -w, 0)]
    faces = [(0, 1, 2, 3)]
    
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    mesh_object.select = True
    context.scene.objects.active = mesh_object
#    ob.floor_property[0].floor_length = 

def update_object(self, context):
    ob = context.object
    ob.dimensions = ob.floor_property[0].floor_length, ob.floor_property[0].floor_width, ob.dimensions[2] 
    
    # Check if the thickness of the floor is greater then 0.
    # If true then change the thickness attribute of the modifier
    
    if ob.floor_property[0].floor_thickness != 0:
        if create_floor.ob_modifier is None or create_floor.ob_modifier.name == "":
            
            create_floor.ob_modifier = ob.modifiers.new('Solidify', 'SOLIDIFY')
            create_floor.ob_modifier.thickness = ob.floor_property[0].floor_thickness
        else:
            create_floor.ob_modifier.thickness = ob.floor_property[0].floor_thickness
    else:
        if create_floor.ob_modifier is not None:
            ob.modifiers.remove(create_floor.ob_modifier)
            create_floor.ob_modifier = None
    #ob.floor_property[0].modifier.thickness = ob.floor_property[0].floor_thickness
    
class FloorProperty(bpy.types.PropertyGroup):
    
    floor_length = bpy.props.FloatProperty(name = 'Floor Length', default = 4.0, min = 0, max = 100, update = update_object, description = 'Length of the floor')
    floor_width = bpy.props.FloatProperty(name = 'Floor Width', default = 4.0, min = 0, max = 100, update = update_object, description = 'Width of the floor')
    floor_thickness = bpy.props.FloatProperty(name = 'Floor Thickness', default = 0.0, min = 0, max = 100, update = update_object, description = 'Thickness of the floor')
    modifier = None

bpy.utils.register_class(FloorProperty)
bpy.types.Object.floor_property = bpy.props.CollectionProperty(type = FloorProperty)
    
class VIEW3D_PT_floor_builder_config(bpy.types.Panel):
    
    bl_idname = 'VIEW3D_PT_floor_builder_config'
    bl_label = 'Floor Properties'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_description = 'Configure floor object'
    bl_category = 'Builder'
    
    @classmethod
    def poll(cls, context):
        
        ob = context.object
        
        if ob is None:
            return False
        if 'floor_property' not in ob:
            return False
        else:
            return True
    
    def draw(self, context):
        
        ob = context.object
        
        try:
            if 'floor_property' not in ob:
                return
        except:
            return
        
        layout = self.layout
        
        floor_properties = context.object.floor_property[0]
        
        layout.prop(floor_properties, 'floor_length')
        layout.prop(floor_properties, 'floor_width')
        layout.prop(floor_properties, 'floor_thickness')
