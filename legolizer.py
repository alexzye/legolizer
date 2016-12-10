bl_info = {
    "name": "Legolizer",
    "category": "Mesh",
}

import bpy
import bmesh
from mathutils import Vector

OCTREE_DEPTH = 6
UP_VECTOR = Vector((0.0, 0.0, 1.0));

def calculate_radius(obj):
    v0 = obj.matrix_world * obj.data.vertices[obj.data.edges[0].vertices[0]].co
    v1 = obj.matrix_world * obj.data.vertices[obj.data.edges[0].vertices[1]].co
    return (v1-v0).length / 2.8
    
class Legolizer(bpy.types.Operator):
    """Legolizer"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "object.legolize"        # unique identifier for buttons and menu items to reference.
    bl_label = "Legolize"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
 
    def execute(self, context):        # execute() is called by blender when running the operator.
        for obj in bpy.context.selected_objects:
            context.scene.objects.active = obj
            bpy.ops.object.modifier_add(type='REMESH')
            context.object.modifiers["Remesh"].mode = 'BLOCKS'
            context.object.modifiers["Remesh"].octree_depth = OCTREE_DEPTH
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Remesh")
            radius = calculate_radius(obj)
            for polygon in obj.data.polygons:
                if polygon.normal == UP_VECTOR:
                    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=1.4*radius, location=polygon.center)
                    bump = bpy.context.object
                    bump.parent = obj
            bpy.ops.object.select_all(action='DESELECT')
            context.scene.objects.active = obj
            bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
            obj.select = True
            for so in context.selected_objects:
                if so.type != 'MESH':
                    so.select = False
            if len(context.selected_objects):
                context.scene.objects.active = context.selected_objects[0]        
                bpy.ops.object.join()
                            
            return {'FINISHED'}            # this lets blender know the operator finished successfully.
        

def b_print(to_print):
    print(to_print)
    
def register():
    bpy.utils.register_class(Legolizer)

def unregister():
    bpy.utils.unregister_class(Legolizer)

# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()