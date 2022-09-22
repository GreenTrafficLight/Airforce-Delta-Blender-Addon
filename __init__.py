bl_info = {
	"name": "Import Airforce Delta Models format",
	"description": "Import Airforce Delta Model",
	"author": "GreenTrafficLight",
	"version": (1, 0),
	"blender": (2, 92, 0),
	"location": "File > Import > Airforce Delta Importer",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"support": "COMMUNITY",
	"category": "Import-Export"}

import bpy

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator

class ImportAirforceDelta(Operator, ImportHelper):
    """Load a Airforce Delta model file"""
    bl_idname = "import_scene.ads_data"
    bl_label = "Import Airforce Delta Data"

    filename_ext = ".nj;.kap"
    filter_glob: StringProperty(default="*.nj;*.kap", options={'HIDDEN'}, maxlen=255,)

    # Selected files
    files: CollectionProperty(type=bpy.types.PropertyGroup)

    clear_scene: BoolProperty(
        name="Clear scene",
        description="Clear everything from the scene",
        default=False,
    )

    def execute(self, context):
        from . import  import_ads
        import_ads.main(self.filepath, self.files, self.clear_scene)
        return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(ImportAirforceDelta.bl_idname, text="Airforce Delta")


def register():
    bpy.utils.register_class(ImportAirforceDelta)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportAirforceDelta)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()