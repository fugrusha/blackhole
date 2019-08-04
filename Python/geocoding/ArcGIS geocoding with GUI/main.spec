# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['QtWindow.py', 'images_rc.py', 'main_geo_module.py', 'mydesign.py'],
             pathex=['C:\\Users\\win10_env\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'C:\\Users\\win10_env\\Desktop\\geocoder'],
             binaries=[],
             datas=[],
             hiddenimports=['numpy.random.common', 'PyQt', 'numpy.random.bounded_integers', 'numpy.random.entropy'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ArcGISgeocoder',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, icon='C:\\Users\\win10_env\\Desktop\\geocoder\\map.ico' )
