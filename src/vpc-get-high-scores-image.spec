# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['createHighScoreImage.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['charset_normalizer', 'charset_normalizer.md__mypyc'],
    hookspath=[],
    runtime_hooks=[],
    excludes=['tkinter', 'unittest'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='vpc-get-high-scores-image',
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
    version='version.rc',
)
