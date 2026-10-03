"""Regenerate high-resolution WebP slide images from the preserved source PDF.

Requires Poppler (pdftoppm) and Pillow. Only needed when replacing slide images;
the regular site build uses the already-committed images.
"""
from pathlib import Path
import subprocess
import tempfile
from PIL import Image

root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='data-summary-slides-') as tmp:
    prefix=Path(tmp)/'slide'
    subprocess.run(['pdftoppm','-scale-to','2000','-png',str(root/'assets/source/01-data-summary.pdf'),str(prefix)],check=True)
    images=sorted(Path(tmp).glob('slide-*.png'))
    if len(images)!=31: raise ValueError(f'Expected 31 pages, found {len(images)}')
    for n,path in enumerate(images,1):
        Image.open(path).convert('RGB').save(root/'assets/slides'/f'{n:02}.webp',quality=90,method=6)
print('Rendered all 31 slide images.')
