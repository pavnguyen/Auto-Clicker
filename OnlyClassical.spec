# -*- mode: python -*-

block_cipher = None


a = Analysis(['OnlyClassical.py'],
             pathex=['Z:\\Project Python\\Auto Clicker'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=True,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='OnlyClassical',
          debug=False,
          strip=False,
          upx=True,
          console=True , version='version.txt', icon='robo.ico')
