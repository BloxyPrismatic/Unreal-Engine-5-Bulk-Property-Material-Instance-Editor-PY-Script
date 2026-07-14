import os
import unreal

"""
# 🛠️ Bulk Material Instance Setup Script for UE5

This Python script automates editing multiple Material Instances at once. It sets specific slider values and automatically searches a sibling `Textures` folder to find and link matching texture maps.

### 📌 Requirements & Folder Setup
Your project folders and files must follow this standard structure:
```text
📁 Asset_Folder
├── 📁 Materials <--- Run script on Material Instances inside here
└── 📁 Textures <--- Put your texture files inside here
```
* **Naming Example:** If your instance is `MI_Wall`, it looks for textures containing `Wall` with suffixes like `_A` (Ambient), `_AO` (Occlusion), or `_E` (Emissive).

### 🚀 How To Use
1. **Select Assets:** Select all target Material Instances in your **Content Browser**.
2. **Open Console:** Go to the bottom of Unreal Engine and find the **Cmd** input bar.
3. **Switch to Python:** Click the arrow next to **Cmd** and change the mode to **Python**.
4. **Run Script:** Paste the script into the bar and press **Enter**.

*Tip: You can change the values (like `EmissiveColorMapWeightValue`) at the top of the script before running it.*
"""

# 1. Get all assets currently selected in your Content Browser
selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()

#____Global_Scalar_Parameter_Values____#
# DEFAULT PARAMETERS : AmbientColorMapWeight, AmbientOcclusionMapWeight, EmissiveColorMapWeight
AmbientColorMapWeight = "AmbientColorMapWeight"
AmbientOcclusionMapWeight = "AmbientOcclusionMapWeight"
EmissiveColorMapWeight = "EmissiveColorMapWeight"

# VALUES
AmbientColorMapWeightValue = 1.0
AmbientOcclusionMapWeightValue = 1.0
EmissiveColorMapWeightValue = 1.0

#____Global_Texture_Parameter_Values____#
# DEFAULT PARAMETERS : AmbientColorMap, AmbientOcclusionMap, EmissiveColorMap
AmbientColorMap = "AmbientColorMap"
AmbientOcclusionMap = "AmbientOcclusionMap"
EmissiveColorMap = "EmissiveColorMap"

# 3. Loop through everything you selected
for asset in selected_assets:
    # Check if the asset is actually a Material Instance
    if isinstance(asset, unreal.MaterialInstanceConstant):
        
        #____Global_Scalar_Parameter_Values____#
        unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(asset, AmbientColorMapWeight, AmbientColorMapWeightValue)
        unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(asset, AmbientOcclusionMapWeight, AmbientOcclusionMapWeightValue)
        unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(asset, EmissiveColorMapWeight, EmissiveColorMapWeightValue)

        #____RECURSIVE TEXTURE SEARCH SEQUENCE____#
        asset_name = asset.get_name()
        search_name = asset_name.replace("MI_", "")

        material_folder_path = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(asset)
        material_dir = os.path.dirname(material_folder_path)

        parent_dir = os.path.dirname(material_dir)
        texture_folder_path = f"{parent_dir}/Textures"

        if not unreal.EditorAssetLibrary.does_directory_exist(texture_folder_path):
            print(f"Skipping: Textures folder does not exist at {texture_folder_path}")
            unreal.EditorAssetLibrary.save_loaded_asset(asset)
            continue

        texture_assets = unreal.EditorAssetLibrary.list_assets(texture_folder_path)
        
        # Initialize placeholders for specific maps
        found_ambient = None
        found_ao = None
        found_emissive = None
        fallback_standard_texture = None

        # Search through the files for a matching name
        for tex_path in texture_assets:
            tex_name = os.path.basename(tex_path).split('.')[0]
            clean_tex_name = tex_name.replace("T_", "")

            # Check if texture name relates to the material instance
            if search_name.lower() in clean_tex_name.lower() or clean_tex_name.lower() in search_name.lower():
                clean_path = tex_path.split('.')[0]
                texture_object = unreal.EditorAssetLibrary.load_asset(clean_path)
                
                if not texture_object:
                    continue

                # DETECT SUFFIXES (Case-insensitive check)
                lower_name = tex_name.lower()
                
                # Check for Albedo/Ambient Maps
                if lower_name.endswith("_a") or lower_name.endswith("_d") or "_albedo" in lower_name or "_diffuse" in lower_name:
                    found_ambient = texture_object
                # Check for Ambient Occlusion Maps
                elif lower_name.endswith("_ao") or "_occlusion" in lower_name:
                    found_ao = texture_object
                # Check for Emissive Maps
                elif lower_name.endswith("_e") or "_emissive" in lower_name or "_glow" in lower_name:
                    found_emissive = texture_object
                # Standard map with no specific suffix found yet
                else:
                    fallback_standard_texture = texture_object

        #____ASSIGN TEXTURE PARAMETERS SEQUENCE____#
        # Apply specific Ambient map, fallback to standard if missing
        final_ambient = found_ambient if found_ambient else fallback_standard_texture
        if final_ambient:
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(asset, AmbientColorMap, final_ambient)
            print(f"Success: Linked Ambient Map to {asset_name}")

        # Apply specific AO map, fallback to standard if missing
        final_ao = found_ao if found_ao else fallback_standard_texture
        if final_ao:
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(asset, AmbientOcclusionMap, final_ao)
            print(f"Success: Linked AO Map to {asset_name}")

        # Apply specific Emissive map, fallback to standard if missing
        final_emissive = found_emissive if found_emissive else fallback_standard_texture
        if final_emissive:
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(asset, EmissiveColorMap, final_emissive)
            print(f"Success: Linked Emissive Map to {asset_name}")

        # Save the asset so you don't lose the change
        unreal.EditorAssetLibrary.save_loaded_asset(asset)
        print(f"Successfully updated all properties for: {asset_name}\n")

print("Done! All selected material instances have been updated cleanly.")
