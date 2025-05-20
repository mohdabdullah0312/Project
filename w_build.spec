import os
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

hidden_imports = collect_submodules("your_project_folder") + [
    "ecdh_key_ex",
    "enc_dec",
    "file_share",
    "requirements_installer"
]

datas = [("requirements.txt", ".")]

project_path = os.path.abspath(".")

a = Analysis(
    ["main.py"],
    pathex=[project_path],
    hiddenimports=hidden_imports,
    datas=datas
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name="SecureShare",
    debug=False,
    console=True,              
    icon="icon.ico"        
)

coll = COLLECT(
    exe,
    binaries=a.binaries,
    zipfiles=a.zipfiles,
    datas=a.datas,
    strip=True,
    upx=True,
    name="SecureShare"
)
