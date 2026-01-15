# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Supervertaler.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('docs', 'docs'),
        ('modules', 'modules'),
        ('assets', 'assets'),
        ('user_data', 'user_data'),
        ('README.md', '.'),
        ('CHANGELOG.md', '.'),
        ('FAQ.md', '.'),
        ('api_keys.example.txt', '.'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtWebEngineWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5', 
        'tkinter',
        # CUDA/GPU - not needed for CPU inference
        'torch.cuda',
        'torch.distributed',
        'torch._C._cuda',
        'torch.backends.cuda',
        'torch.backends.cudnn',
        'triton',
        # Heavy ML backends not needed
        'tensorflow',
        'tensorboard',
        'keras',
        # Jupyter/notebook stuff
        'notebook',
        'jupyter',
        'IPython',
        # Testing frameworks
        'pytest',
        'unittest',
        # Dev tools
        'black',
        'isort',
        'mypy',
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Supervertaler',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets\\icon.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Supervertaler',
)
