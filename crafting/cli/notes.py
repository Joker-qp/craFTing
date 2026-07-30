from typing import Optional
import typer
from rich import print
from rich.console import Console
from rich.table import Table
from crafting.core.models import Note
from crafting.core.security import encrypt_contetn, decrypt_content
from crafting.db.connection import init_db
from crafting.db.repository import NoteRepository
import json
from pathlib import Path

def add_note(
        title: str,
        content: str,
        tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Not etiketleri (virgülle ayırın: python,fikir"),
        encrypt: bool = typer.Option(False, "--encrypt", "-e", help="Notu şifreleyerek kaydet")
):
    init_db()

    if encrypt:
        password = typer.prompt("🔒 Şifreleme parolası belirleyin", hide_input=True, confirmation_prompt=True)
        content = encrypt_contetn(content, password)

    note = Note(title=title, content=content, tags=tag, is_encrypted=encrypt)
    note_id = NoteRepository.add(note)
    status_msg = "[red]🔒 Şifreli[/red]" if encrypt else "[green]Açık[/green]"
    print(f"[bold green]✓[/bold green] Not eklendi! (ID: [cyan]{note_id}[/cyan], Durum: {status_msg})")

console = Console()

def list_notes():
    console.clear()
    init_db()
    notes = NoteRepository.get_all()
    if not notes:
        print("[yellow]Henüz kaydedilmiş bir not yok.[/yellow]")
        return

    table = Table(
        title="📋 Not Kasası",
        show_header=True,
        header_style="bold magenta",
        expand=True
    )

    table.add_column("ID", style="cyan", justify="center", no_wrap=True)
    table.add_column("Başlık", style="bold white", ratio=1)
    table.add_column("Etiket", style="yellow", no_wrap=True)
    table.add_column("Şifreli mi?", justify="center", no_wrap=True)
    table.add_column("Oluşturma Tarihi", style="dim", justify="center", no_wrap=True)

    for n in notes:
        status = "[red]🔒 Şifreli[/red]" if n.is_encrypted else "[green]🔒 Açık[/green]"
        tags_display = n.tags if n.tags else "-"
        table.add_row(str(n.id), n.title, tags_display, status, n.created_at)

    print(table)

def show_note(note_id: int):
    console.clear()
    init_db()
    note = NoteRepository.get_by_id(note_id)
    if not note:
        print(f"[bold red]Hata:[/bold red] ID: {note_id} olan bir not bulunamadı.")
        return
    content_to_display = note.content
    if note.is_encrypted:
        password = typer.prompt("🔒 Bu not şifreli. Paraloyı girin", hide_input=True)
        try:
            content_to_display = decrypt_content(note.content, password)
        except ValueError:
            print("\n[bold red]❌ Hata:[/bold red] Yanlış parola! Not içeriği çözülemedi.\n")
            return
    tags_info = f" [yellow]#[{note.tags}][yellow]" if note.tags else ""
    print(f"\n[bold cyan]📌 {note.title}[/bold cyan]{tags_info} [dim]({note.created_at})[/dim]")
    print("─" * 40)
    print(content_to_display)
    print("─" * 40 + "\n")

def search_notes(query: str):
    console.clear()
    init_db()
    results = NoteRepository.search(query)
    if not results:
        print(f"[yellow]''{query}'' araması için eşleşen not bulunamadı.[/yellow]")
        return

    table = Table(
        title=f"🔍 Arama Sonuçları ('{query}')", 
        show_header=True, 
        header_style="bold blue",
        expand=True
    )
    
    table.add_column("ID", style="cyan", justify="center", no_wrap=True)
    table.add_column("Başlık", style="bold white", ratio=1)
    table.add_column("Etiketler", style="yellow", no_wrap=True)
    table.add_column("Şifreli mi?", justify="center", no_wrap=True)

    for n in results:
        status = "[red]🔒 Şifreli[/red]" if n.is_encrypted else "[green]🔓 Açık[/green]"
        tags_display = n.tags if n.tags else "-"
        table.add_row(str(n.id), n.title, tags_display, status)

    print(table)

def delete_note(note_id: int):
    init_db()
    deleted = NoteRepository.delete(note_id)
    if deleted:
        print(f"[bold green]✓[/bold green] ID: [cyan]{note_id}[/cyan] olan not silindi.")
    else:
        print(f"[bold red]Hata:[/bold red] ID: {note_id} olan bir not bulunamadı.")

def export_notes(file_path: str = typer.Option("creating_backup.json", "--out", "-o", help="Yedek dosya adı/yolu")):
    init_db()
    notes = NoteRepository.get_all()
    if not notes:
        print("[yelow]Dışa aktarılacak not bulunamadı.[/yellow]")
        return

    data = [
        {
            "title": n.title,
            "content": n.content,
            "tags": n.tags,
            "is_encrypted": n.is_encrypted,
            "created_at": n.created_at,
            "updated_at": n.updated_at,
        }
        for n in notes
    ]

    path = Path(file_path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"[bold green]✓[/bold green] {len(notes)} adet not [cyan]{path.resolve()}[/cyan] dosyasına aktarıldı.")

def import_notes(file_path: str):
    init_db()
    path = Path(file_path)
    if not path.exists():
        print(f"[bold red]Hata:[/bold red] '{file_path}' dosyası bulunamadı.")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        count = 0
        for item in data:
            note = Note(
                title=item["title"],
                content=item["content"],
                tags=item.get("tags"),
                is_encrypted=item.get("is_encrypted", False),
                created_at=item.get("created_at"),
                updated_at=item.get("updated_at")
            )
            NoteRepository.add(note)
            count += 1

        print(f"[bold green]✓[/bold green] {count} adet not başarıyla kasaya aktarıldı.")
    except Exception as e:
        print(f"[bold red]Hata:[/bold red] Geçersiz yedek dosyası formatı! ({e})")