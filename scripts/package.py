from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root/'manifest.json').read_text())
version = manifest['version']
for upload in (False, True):
    suffix = '-upload' if upload else ''
    output = root.parent.parent/f'sleigh-ride-christmas-theme-{version}{suffix}.zip'
    names = ['manifest.json','images','logo'] if upload else ['manifest.json','images','logo','source','scripts','store-assets','README.md','LICENSE']
    with ZipFile(output,'w',ZIP_DEFLATED) as archive:
        for name in names:
            path = root/name
            files = [path] if path.is_file() else sorted(path.rglob('*'))
            for file in files:
                if file.is_file() and '__pycache__' not in file.parts:
                    archive.write(file,file.relative_to(root).as_posix())
    with ZipFile(output) as archive:
        assert archive.testzip() is None
        required = ['manifest.json',manifest['icons']['128'],*manifest['theme']['images']['theme_ntp_background'].values()]
        assert all(name in archive.namelist() for name in required)
    print(output)
