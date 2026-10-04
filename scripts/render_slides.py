"""Regenerate source slide captures with Poppler and Pillow.

Run with --chapter data-summary (default), probability-part1, counting, or all.
Normal site builds use the already committed images.
"""
from pathlib import Path
import argparse
import subprocess
import tempfile
from PIL import Image

root=Path(__file__).resolve().parents[1]
chapters={
    'data-summary':('01-data-summary.pdf','slides',31),
    'probability-part1':('02-probability-part1.pdf','slides/probability-part1',43),
    'counting':('03-counting.pdf','slides/counting',53),
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--chapter',choices=[*chapters,'all'],default='data-summary')
args=parser.parse_args()
selected=chapters if args.chapter=='all' else {args.chapter:chapters[args.chapter]}
for name,(pdf,folder,count) in selected.items():
    destination=root/'assets'/folder
    destination.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f'{name}-slides-') as tmp:
        prefix=Path(tmp)/'slide'
        subprocess.run(['pdftoppm','-scale-to','2000','-png',str(root/'assets/source'/pdf),str(prefix)],check=True)
        images=sorted(Path(tmp).glob('slide-*.png'))
        if len(images)!=count: raise ValueError(f'Expected {count} pages, found {len(images)}')
        for n,path in enumerate(images,1):
            Image.open(path).convert('RGB').save(destination/f'{n:02}.webp',quality=90,method=6)
    print(f'Rendered {count} slide images for {name}.')
