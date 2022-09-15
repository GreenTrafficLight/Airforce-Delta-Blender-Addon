bl_info = {
	"name": "Import Airforce Delta Strik Models format",
	"description": "Import Airforce Delta Strike Model",
	"author": "GreenTrafficLight",
	"version": (1, 0),
	"blender": (2, 92, 0),
	"location": "File > Import > Airforce Delta Strik Importer",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"support": "COMMUNITY",
	"category": "Import-Export"}

import bpy

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

class ImportAirforceDeltaStrike(Operator, ImportHelper):
    """Load a Airforce Delta Strike model file"""
    bl_idname = "import_scene.ads_data"
    bl_label = "Import Airforce Delta Strike Data"

    filename_ext = ".nj"
    filter_glob: StringProperty(default="*.nj", options={'HIDDEN'}, maxlen=255,)

    clear_scene: BoolProperty(
        name="Clear scene",
        description="Clear everything from the scene",
        default=False,
    )

    def execute(self, context):
        from . import  import_ads
        import_ads.main(self.filepath, self.clear_scene)
        return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(ImportAirforceDeltaStrike.bl_idname, text="Airforce Delta Strike")


def register():
    bpy.utils.register_class(ImportAirforceDeltaStrike)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportAirforceDeltaStrike)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()