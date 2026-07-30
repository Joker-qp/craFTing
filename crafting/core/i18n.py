import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".crafting_config.json"

MESSAGES = {
    "tr": {
        "sub_title": "v0.1.0 • Terminal Tabanlı Şifreli Not Kasası",
        "guide_title": "📌 Hızlı Başlangıç Rehberi:",
        "add": "1. Not Ekle:",
        "add_enc": "2. Şifreli Not Ekle:",
        "list": "3. Notları Listele:",
        "show": "4. Not Oku:",
        "search": "5. Arama Yap:",
        "export_import": "6. Yedek Al / Yükle:",
        "tip": "İpucu: 'cr --help' yazarak tüm detayları görebilirsin.",
        "lang_changed": "✓ Dil başarıyla güncellendi:",
        "invalid_lang": "Hata: Desteklenen diller sadece 'tr' ve 'en'."
    },
    "en": {
        "sub_title": "v0.1.0 • Terminal-Based Encrypted Note Vault",
        "guide_title": "📌 Quick Start Guide:",
        "add": "1. Add Note:",
        "add_enc": "2. Add Encrypted Note:",
        "list": "3. List Notes:",
        "show": "4. Read Note:",
        "search": "5. Search Notes:",
        "export_import": "6. Backup / Import:",
        "tip": "Tip: Run 'cr --help' to view all command details.",
        "lang_changed": "✓ Language successfully set to:",
        "invalid_lang": "Error: Supported languages are only 'tr' and 'en'."
    }
}

def get_lang() -> str:
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f).get("lang", "tr")
        except Exception:
            pass
    return "tr"

def set_lang(lang: str) -> bool:
    lang = lang.lower()
    if lang not in MESSAGES:
        return False
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({"lang": lang}, f)
    return True

def t(key: str) -> str:
    lang = get_lang()
    return MESSAGES.get(lang, MESSAGES["tr"]).get(key, key)