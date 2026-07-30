# 🛠️ craFTing CLI

[![PyPI version](https://img.shields.io/pypi/v/crafting-cli.svg)](https://pypi.org/project/crafting-cli/)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🇹🇷 **[Türkçe dokümantasyon için buraya tıklayın](#-crafting-cli-tr)**

**craFTing** is a modern, fast, and sleek CLI note vault application that allows you to securely store, encrypt, and manage your notes directly from your terminal.

---

## ✨ Features

- 🔐 **Strong Encryption:** Securely protect your notes with password encryption.
- 🎨 **Sleek Terminal Interface:** 3D RGB gradient welcome banner and colorful `Rich` outputs.
- 🌐 **Multi-Language Support:** Dynamic language toggle between Turkish (`tr`) and English (`en`).
- ⚡ **Fast Search & Tagging:** Organize notes with tags and search instantly.
- 💾 **Backup & Migration:** Secure JSON export and import capabilities.
- 🗄️ **SQLite Backend:** Fast and reliable local database storage.

---

## 🚀 Installation

You can install `craFTing` directly from PyPI:

```bash
pip install crafting-cli
```

Or install it as an isolated CLI tool using `pipx`:

```bash
pipx install crafting-cli
```

---

## 📖 Usage

Run `cr` or `crafting` directly in your terminal.

### 🏠 Welcome Screen
```bash
cr
```

### ➕ Add Notes
```bash
# Standard Note
cr add "Meeting Notes" "Project presentation at 14:00." -t work

# Encrypted Note
cr add "Secret Note" "Top secret content..." -e
```

### 📋 List & Read Notes
```bash
# List all notes
cr list

# View specific note details
cr show 1
```

### 🔍 Search & Delete
```bash
# Search notes
cr search "presentation"

# Delete a note
cr delete 1
```

### 🌐 Change Language
```bash
# Switch to English
cr lang en

# Switch to Turkish
cr lang tr
```

### 📤 Export & Import
```bash
# Backup notes to JSON
cr export

# Import from backup
cr import backup.json
```

---

<br>

## 🇹🇷 craFTing CLI (TR)

**craFTing**, terminal üzerinden notlarınızı güvenle saklamanızı, şifrelemenizi ve yönetmenizi sağlayan modern, hızlı ve şık bir CLI not kasası uygulamasıdır.

### ✨ Özellikler
- 🔐 **Güçlü Şifreleme:** Notlarınızı parola ile güvenli bir şekilde saklayın.
- 🎨 **Şık Terminal Arayüzü:** 3D RGB renk geçişli karşılama ekranı ve `Rich` tabanlı renkli çıktılar.
- 🌐 **Çoklu Dil Desteği:** Türkçe (`tr`) ve İngilizce (`en`) dinamik dil seçeneği.
- ⚡ **Hızlı Arama & Etiketleme:** Notlarınızı etiketlerle organize edin ve anında arama yapın.
- 💾 **Yedekleme & Aktarım:** JSON formatında güvenli dışa/içe aktarma (export/import) desteği.
- 🗄️ **SQLite Altyapısı:** Hızlı ve güvenilir yerel veritabanı.

### 🚀 Kurulum
```bash
pip install crafting-cli
```

---

## 📄 License / Lisans

This project is licensed under the [MIT License](LICENSE).
