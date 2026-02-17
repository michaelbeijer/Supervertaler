# -*- mode: python ; coding: utf-8 -*-
# macOS build spec for Supervertaler
# Usage: pyinstaller Supervertaler_macOS.spec --noconfirm --clean

# Read version from pyproject.toml at build time
try:
    import tomllib
except ImportError:
    import tomli as tomllib
with open('pyproject.toml', 'rb') as _f:
    _version = tomllib.load(_f)['project']['version']

a = Analysis(
    ['Supervertaler.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('pyproject.toml', '.'),
        ('docs', 'docs'),
        ('modules', 'modules'),
        ('assets', 'assets'),
        ('README.md', '.'),
        ('CHANGELOG.md', '.'),
        ('FAQ.md', '.'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtWebEngineCore',
        'pynput.keyboard._darwin',
        'pynput.mouse._darwin',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5',
        'tkinter',
        # CUDA/GPU - not needed
        'torch.cuda', 'torch.distributed', 'torch._C._cuda',
        'torch.backends.cuda', 'torch.backends.cudnn', 'triton',
        # Heavy ML backends
        'tensorflow', 'tensorboard', 'keras',
        # Jupyter
        'notebook', 'jupyter', 'IPython',
        # Testing/dev
        'pytest', 'unittest', 'black', 'isort', 'mypy',
        # Windows-only packages
        'keyboard', 'ahk', 'pyautogui',
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
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.icns',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='Supervertaler',
)

app = BUNDLE(
    coll,
    name='Supervertaler.app',
    icon='assets/icon.icns',
    bundle_identifier='com.michaelbeijer.supervertaler',
    info_plist={
        'CFBundleName': 'Supervertaler',
        'CFBundleDisplayName': 'Supervertaler',
        'CFBundleVersion': _version,
        'CFBundleShortVersionString': _version,
        'NSHighResolutionCapable': True,
        'NSMicrophoneUsageDescription':
            'Supervertaler uses the microphone for voice dictation.',
        'NSAppleEventsUsageDescription':
            'Supervertaler uses AppleScript to send keystrokes for global hotkeys.',
        'LSMinimumSystemVersion': '13.0',
        'CFBundleDocumentTypes': [],
        'NSRequiresAquaSystemAppearance': False,
        # Fix: Finder launches apps with minimal env (no LANG/LC_CTYPE),
        # causing locale-dependent code to crash silently.
        'LSEnvironment': {
            'LANG': 'en_US.UTF-8',
            'LC_CTYPE': 'en_US.UTF-8',
        },
    },
)
