# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(
    ['src/statscrypt/cli.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('src/statscrypt', 'statscrypt') # Include the entire statscrypt package
    ],
    hiddenimports=[
        'pandas._libs.interval', # Common pandas hidden import
        'pandas._libs.tslibs.np_datetime',
        'pandas._libs.tslibs.nattype',
        'matplotlib.backends.backend_agg', # Specific matplotlib backend
        'matplotlib.backends.backend_tkagg',
        'matplotlib.pyplot',
        'numpy',
        'statsmodels',
        'tabulate'
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
    [],
    exclude_binaries=True,
    name='statscrypt_engine',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='statscrypt_engine',
)
