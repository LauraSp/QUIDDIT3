# -*- mode: python -*-

block_cipher = None


a = Analysis(['QMainWindow.py'],
             pathex=['D:\\Users\\Laura\\Anaconda3\\envs\\QUIDDITworkenv\\Library', 'D:\\QUIDDIT3'],
             binaries=[],
             datas=[('CAXBD.csv', '.'), ('typeIIa.csv', '.'), ('QUIDDITlogo.gif', '.')],
             hiddenimports=[],
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
          [],
          exclude_binaries=True,
          name='QUIDDIT',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='QUIDDITicon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='QUIDDIT')
