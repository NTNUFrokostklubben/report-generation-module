# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

block_cipher = None

imagecodecs_datas, imagecodecs_binaries, imagecodecs_hiddenimports = collect_all('imagecodecs')

a = Analysis(
    ['src/server.py'],
    pathex=['src'],
    binaries=imagecodecs_binaries,
    datas=[
        ('src/templates', 'templates'),
        *imagecodecs_datas,
    ],
    hiddenimports=[
        'grpc',
        'skavl_proto',
        'skavl_proto.report_pb2',
        'skavl_proto.report_pb2_grpc',
        'skavl_proto.anomaly_pb2',
        'skavl_proto.anomaly_pb2_grpc',
        'weasyprint',
        'tifffile',
        'imagecodecs',
        *imagecodecs_hiddenimports,
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='report-server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
