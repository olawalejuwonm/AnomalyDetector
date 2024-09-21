# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\HP\\Documents\\GitHub\\UoL-Projects\\AnomalyDetector\\app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\HP\\Documents\\GitHub\\UoL-Projects\\BuildAnomaly\\.env', '.'), ('C:\\Users\\HP\\Documents\\GitHub\\UoL-Projects\\BuildAnomaly\\main.py', '.'), ('C:\\Users\\HP\\Documents\\GitHub\\UoL-Projects\\BuildAnomaly\\yolov8n.pt', '.\\'), ('C:\\Users\\HP\\Documents\\GitHub\\UoL-Projects\\BuildAnomaly\\templates', 'templates/'), ('C:\\Users\\HP\\Documents\\GitHub\\UoL-Projects\\BuildAnomaly\\static\\recorded_videos\\.gitkeep', '.'), ('C:\\Users\\HP\\Documents\\GitHub\\UoL-Projects\\BuildAnomaly\\static\\recorded_videos', 'recorded_videos/'), ('C:\\Users\\HP\\Documents\\GitHub\\UoL-Projects\\BuildAnomaly\\static\\styles.css', '.\\static'), ('C:\\Users\\HP\\Documents\\GitHub\\UoL-Projects\\AnomalyDetector\\.venv\\Lib\\site-packages\\ultralytics\\cfg\\default.yaml', '.\\ultralytics\\cfg')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Intelligent Surveillance System',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
