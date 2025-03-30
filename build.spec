# PyInstaller Build Specification File
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

# List all hidden imports (modules used dynamically)
hidden_imports = collect_submodules("your_project_folder") + [
    "ecdh_key_ex",
    "enc_dec",
    "file_share",
    "requirements_installer"
]

# Explicitly include `requirements.txt`
datas = [("requirements.txt", ".")]

# Analysis step: Collects everything needed for packaging
a = Analysis(
    ["main.py"],  # Main script
    pathex=["."],  # Search path
    hiddenimports=hidden_imports,  # Include dynamically loaded modules
    datas=datas,  # Include external files (e.g., requirements.txt)
)

# Pack everything
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas, name="SecureFileManager", debug=False)
coll = COLLECT(exe, a.datas, a.binaries, strip=False, upx=True, name="SecureFileManager")
