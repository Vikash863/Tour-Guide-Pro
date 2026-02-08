from deep_translator import GoogleTranslator
import polib

# Languages you want to translate into
languages = ["hi", "mr", "ta"]

for lang in languages:
    po_file = f"locale/{lang}/LC_MESSAGES/django.po"
    po = polib.pofile(po_file)

    for entry in po:
        if entry.msgstr.strip() == "":
            try:
                entry.msgstr = GoogleTranslator(source='auto', target=lang).translate(entry.msgid)
                print(f"{entry.msgid} -> {entry.msgstr} ({lang})")
            except Exception as e:
                print(f"Failed to translate {entry.msgid}: {e}")

    po.save()
    print(f"Saved translations for {lang}")
