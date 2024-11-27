# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 定義資料檔案
added_files = [
    # 移除不需要的圖片檔案
]

a = Analysis(
    ['TurboTicket.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=['babel.numbers'],  # tkcalendar 需要的相依套件
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='台鐵訂票助手',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不顯示控制台
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='train.ico',  # 改用 train.ico 作為程式圖示
) 