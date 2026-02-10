import polib
import sys
from pathlib import Path

base = Path(__file__).resolve().parents[1]
locale_dir = base / 'locale'

if not locale_dir.exists():
    print('No locale directory found')
    sys.exit(1)

for lang_dir in locale_dir.iterdir():
    lc_messages = lang_dir / 'LC_MESSAGES'
    if not lc_messages.exists():
        continue
    for po in lc_messages.glob('*.po'):
        mo = po.with_suffix('.mo')
        print(f'Compiling {po} -> {mo}')
        pofile = polib.pofile(str(po))
        pofile.save_as_mofile(str(mo))
print('Done')
