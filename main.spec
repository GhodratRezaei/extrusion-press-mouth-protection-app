# -*- mode: python ; coding: utf-8 -*-


a = Analysis(['main.py'],
             pathex=['E:\\Danieli Breda\\Extrusion Press\\Automation\\mouth-protection\\pyqt-app'],
             binaries=[],
             datas=[('resources\\favicon.ico', 'resources'), ('resources\\logo.jpg', 'resources')], 
             hiddenimports=[],
             hookspath=[], 
             runtime_hooks=[],
             excludes=['camera.py', 'pyqt5designer', 'help', 'mouthProtectionApp_RemoteRepository_Password', '.gitignore'])  
  
pyz = PYZ(a.pure)  

exe = EXE(
    pyz,
    a.scripts, 
    a.binaries,   
    a.datas,   
    [],
    icon="resources\\favicon.ico",
    name="Danieli Mouth Protectoion Application",        
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,     
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,  
    console=False,  
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)