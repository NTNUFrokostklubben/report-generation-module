# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_all, collect_submodules
from PyInstaller.utils.hooks.conda import collect_dynamic_libs as collect_conda_dynamic_libs

binaries = []
datas = []
hiddenimports = []

# Collect Conda-shared DLLs from env/Library/bin for Windows (shared lib for Unix)
binaries += collect_conda_dynamic_libs("grpcio", dependencies=True)
binaries += collect_conda_dynamic_libs("pillow", dependencies=True)
binaries += collect_conda_dynamic_libs("weasyprint", dependencies=True)

# imagecodecs ships many codec extensions — collect_all is the safest approach
imagecodecs_datas, imagecodecs_binaries, imagecodecs_hiddenimports = collect_all("imagecodecs")
binaries += imagecodecs_binaries
datas += imagecodecs_datas

# grpc sometimes benefits from explicit submodule collection
hiddenimports += collect_submodules("grpc")
hiddenimports += [
    "skavl_proto",
    "skavl_proto.report_pb2",
    "skavl_proto.report_pb2_grpc",
    "skavl_proto.anomaly_pb2",
    "skavl_proto.anomaly_pb2_grpc",
    "weasyprint",
    "tifffile",
    "imagecodecs",
    *imagecodecs_hiddenimports,
]

a = Analysis(
    [str(Path("src") / "server.py")],
    pathex=[],
    binaries=binaries,
    datas=[
        (str(Path("src") / "templates"), "templates"),
        *datas,
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="skavl-report-server",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    contents_directory=".",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="server",
)
