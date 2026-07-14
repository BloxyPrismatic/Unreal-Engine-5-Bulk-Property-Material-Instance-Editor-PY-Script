# UE5-Bulk-Material-Editor
I was unable to do a bulk edit so I made a py script that can handle texture directory and parameter editing when you have the material instances you want to edit selected in your content browser!

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
*Tip: If The Material Is Too Bright Adjust The EmissiveColorMapWeightValue (e.g .05)*


