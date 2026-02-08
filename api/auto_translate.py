# translate_and_compile.py

import os
import subprocess
from googletrans import Translator

# Languages to support
languages = ['hi', 'mr', 'ta']

# Initialize translator
translator = Translator()

# Step 1: Create .po files if not exist
for lang in languages:
    path = f'locale/{lang}/LC_MESSAGES'
    os.makedirs(path, exist_ok=True)
    po_file = os.path.join(path, 'django.po')
    if not os.path.exists(po_file):
        open(po_file, 'a').close()  # create empty file

# Step 2: Run makemessages for each language
for lang in languages:
    subprocess.run(['django-admin', 'makemessages', '-l', lang])

# Step 3: Translate msgid -> msgstr automatically
for lang in languages:
    po_file = f'locale/{lang}/LC_MESSAGES/django.po'
    lines = []
    with open(po_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    msgid = None
    for line in lines:
        if line.startswith('msgid '):
            msgid = line[6:].strip().strip('"')
            new_lines.append(line)
        elif line.startswith('msgstr '):
            if msgid:
                translated = translator.translate(msgid, dest=lang).text
                new_lines.append(f'msgstr "{translated}"\n')
                msgid = None
        else:
            new_lines.append(line)

    with open(po_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

# Step 4: Compile messages
subprocess.run(['django-admin', 'compilemessages'])

print("✅ All languages translated and compiled successfully!")
