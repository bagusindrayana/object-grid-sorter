bl_info = {
    "name": "Object Grid Sorter",
    "author": "Bagus Indrayana",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "ObjectSorter > Sort Objects",
    "description": "Sort selected objects in a non-overlapping grid",
    "warning": "",
    "wiki_url": "",
    "category": "Object"
}

import bpy
import mathutils
import math



class OBJECT_OT_sort_objects(bpy.types.Operator):
    bl_idname = "object.sort_objects"
    bl_label = "Sort Objects"
    bl_description = "Sort selected objects in a non-overlapping grid"
    bl_options = {'UNDO'}

    # fungsi untuk menghitung volume dari objek
    def get_volume(self,obj):
        bbox = obj.bound_box
        bbox_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in bbox]
        length = max(bbox_corners, key=lambda v: v.x).x - min(bbox_corners, key=lambda v: v.x).x
        width = max(bbox_corners, key=lambda v: v.y).y - min(bbox_corners, key=lambda v: v.y).y
        height = max(bbox_corners, key=lambda v: v.z).z - min(bbox_corners, key=lambda v: v.z).z
        ttl = length * width * height
        print(width)
        return [length,width,height,ttl]

    def execute(self, context):
        # Dapatkan objek terpilih
        selected = bpy.context.selected_objects

        # Dapatkan ukuran terbesar dari objek terpilih
        max_x = max([self.get_volume(obj)[0] for obj in selected])
        max_y = max([self.get_volume(obj)[1] for obj in selected])
        max_z = max([self.get_volume(obj)[2] for obj in selected])
        
        # Hitung jumlah objek pada setiap baris
        row_size = math.ceil(math.sqrt(len(selected)))
        
        # Hitung ukuran grid dan margin
        # grid = context.scene.grid_size + context.scene.margin
        margin = context.scene.margin

        # Set posisi untuk setiap objek
        for i, obj in enumerate(selected):
            # Hitung posisi relatif objek
            x = i % row_size
            y = i // row_size
            
            # Geser objek agar posisi tidak saling tumpang tindih
            x_pos = x * (max_x + margin)
            y_pos = y * (max_y + margin)
            z_pos = y * (max_z + margin)
            
            if context.scene.align_axis == 'X':
                pos = mathutils.Vector((x_pos, y_pos, 0))
            elif context.scene.align_axis == 'Y':
                pos = mathutils.Vector((y_pos, x_pos, 0))
            else:
                pos = mathutils.Vector((0, x_pos, z_pos))

            # Terapkan posisi baru pada objek
            obj.location = pos

        return {'FINISHED'}

class VIEW3D_PT_sort_objects(bpy.types.Panel):
    bl_label = "Sort Objects"
    bl_idname = "VIEW3D_PT_sort_objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ObjectSorter"  
    
    def draw(self, context):
        layout = self.layout
        
        # Tampilkan pengaturan margin dan ukuran grid\
        row = layout.row()
        row.prop(context.scene, "margin")
        row = layout.row()
        # row.prop(context.scene, "grid_size")
        # row = layout.row()
        row.prop(context.scene, "align_axis")
        layout.separator()

        # Tampilkan tombol untuk menjalankan operator
        row = layout.row()
        row.operator("object.sort_objects", text="Sort Objects")
        


def register():
    classes = [OBJECT_OT_sort_objects, VIEW3D_PT_sort_objects]
    bpy.types.Scene.margin = bpy.props.FloatProperty(name="Margin", default=1)
    bpy.types.Scene.grid_size = bpy.props.FloatProperty(name="Grid Size", default=1)
    bpy.types.Scene.align_axis = bpy.props.EnumProperty(
        name="Align Axis",
        items=[
            ('X', "X", "Align along the X axis"),
            ('Y', "Y", "Align along the Y axis"),
            ('Z', "Z", "Align along the Z axis")
        ],
        default='X'
    )
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    del bpy.types.Scene.margin
    del bpy.types.Scene.grid_size
    del bpy.types.Scene.align_axis
    for cls in classes:
        bpy.utils.unregister_class(cls)
        

if __name__ == "__main__":
    register()