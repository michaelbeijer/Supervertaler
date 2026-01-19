# -*- mode: python ; coding: utf-8 -*-

# Full Windows EXE build (batteries included): bundles Local Whisper for offline voice transcription
# (heavy ML stack: PyTorch / sentence-transformers / ChromaDB).

from PyInstaller.utils.hooks import collect_submodules, collect_dynamic_libs, collect_data_files

extra_hiddenimports: list[str] = []
extra_binaries = []
extra_datas = []

# Collect Python modules for heavy ML packages
for pkg in ("torch", "sentence_transformers", "chromadb", "tokenizers", "tiktoken", "whisper", "safetensors"):
    try:
        extra_hiddenimports += collect_submodules(pkg)
    except Exception:
        # If a package isn't installed in the build venv, we just won't bundle it.
        # The build script is responsible for installing the FULL extras.
        pass

# Collect native DLLs/.so files for packages with Rust/C extensions
for pkg in ("tokenizers", "safetensors"):
    try:
        extra_binaries += collect_dynamic_libs(pkg)
    except Exception:
        pass

# Torch requires special handling - need ALL its lib files, not just DLLs
try:
    extra_datas += collect_data_files("torch", include_py_files=False)
except Exception:
    pass


a = Analysis(
    ['Supervertaler.py'],
    pathex=[],
    # Collect native DLLs from packages with Rust/C extensions
    binaries=extra_binaries,
    datas=[
        *extra_datas,
        ('docs', 'docs'),
        ('modules', 'modules'),
        ('assets', 'assets'),

        # Ship only the "clean"/default parts of user_data (avoid caches, local DBs, cookies)
        ('user_data/dictionaries', 'user_data/dictionaries'),
        ('user_data/Prompt_Library', 'user_data/Prompt_Library'),
        ('user_data/Translation_Resources', 'user_data/Translation_Resources'),
        ('user_data/shortcuts.json', 'user_data/shortcuts.json'),
        ('user_data/voice_commands.json', 'user_data/voice_commands.json'),
        ('user_data/voice_scripts', 'user_data/voice_scripts'),
        ('user_data/translation_memory.db', 'user_data/translation_memory.db'),

        ('README.md', '.'),
        ('CHANGELOG.md', '.'),
        ('FAQ.md', '.'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtWebEngineWidgets',
        *extra_hiddenimports,
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5',
        'tkinter',

        # GPU compiler/runtime pieces (Torch/Sentence-Transformers expect the
        # Python-level torch.cuda package to exist even for CPU-only use).
        'triton',

        # Other heavy ML backends not used
        'tensorflow',
        'tensorboard',
        'keras',

        # Jupyter/notebook stuff
        'notebook',
        'jupyter',
        'IPython',

        # Testing frameworks
        'pytest',
        # NOTE: unittest is standard library, needed by sentence-transformers

        # Dev tools
        'black',
        'isort',
        'mypy',
    ],
    noarchive=False,
    optimize=0,
)

# Some native DLLs can cause hard crashes in frozen builds when multiple
# runtimes end up bundled. We prefer to NOT ship the MSVC OpenMP runtime
# if it was pulled in transitively.
a.binaries = [b for b in a.binaries if not str(b[0]).lower().endswith('vcomp140.dll')]

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
    # Full build bundles many large native DLLs (PyTorch, tokenizers, etc.).
    # UPX compression can trigger hard-to-diagnose runtime crashes on Windows.
    upx=False,
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
    upx=False,
    upx_exclude=[],
    name='Supervertaler-full',
)
