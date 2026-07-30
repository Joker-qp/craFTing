import typer
from rich import print as rprint
from rich.console import Console
from crafting.cli.notes import add_note,list_notes,show_note,delete_note,search_notes, import_notes, export_notes
from crafting.core.i18n import t, set_lang, get_lang

console = Console()

app = typer.Typer(
    name="crafting",
    help="craFTing - Terminal Tabanlı Not Kasası",
    add_completion=False,
)

BANNER_LINES = [
    "██████╗  ██████╗   █████╗  ███████╗ ████████╗ ██████╗  ███╗   ██╗ ██████╗ ",
    "██╔═══╝  ██╔══██╗ ██╔══██╗ ██╔════╝ ╚══██╔══╝ ╚═██╔═╝  ████╗  ██║ ██╔════╝",
    "██║      ██████╔╝ ███████║ █████╗      ██║      ██║    ██╔██╗ ██║ ██║  ███╗",
    "██║      ██╔══██╗ ██╔══██║ ██╔══╝      ██║      ██║    ██║╚██╗██║ ██║   ██║",
    "╚██████╗ ██║  ██║ ██║  ██║ ██║         ██║    ██████╗  ██║ ╚████║ ╚██████╔╝",
    " ╚═════╝ ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═╝         ╚═╝    ╚═════╝  ╚═╝  ╚═══╝  ╚═════╝ "
]

GRADIENT_COLORS = [
    (220, 235, 255),
    (170, 210, 255),
    (110, 170, 255),
    (60,  120, 240),
    (30,   80, 210),
    (15,   40, 150)
]

def print_gradient_banner():
    """3D Logo ve RGB geçişini ekrana basar."""
    print()
    for line, (r, g, b) in zip(BANNER_LINES, GRADIENT_COLORS):
        # ANSI RGB Renk Kodu
        print(f"\033[38;2;{r};{g};{b}m{line}\033[0m")
    print(f"\033[90m      {t('sub_title')}\033[0m\n")

@app.callback(invoke_without_command=True)
def main_callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        console.clear()
        print_gradient_banner()

        lbl_add = f"{t('add'):<22}"
        lbl_add_enc = f"{t('add_enc'):<22}"
        lbl_list = f"{t('list'):<22}"
        lbl_show = f"{t('show'):<22}"
        lbl_search = f"{t('search'):<22}"
        lbl_exp_imp = f"{t('export_import'):<22}"

        guide = f"""[bold yellow]{t('guide_title')}[/bold yellow]
    [bold cyan]{lbl_add}[/bold cyan] cr add "Başlık" "İçerik" [-t etiket]
    [bold cyan]{lbl_add_enc}[/bold cyan] cr add "Başlık" "İçerik" -e
    [bold cyan]{lbl_list}[/bold cyan] cr list
    [bold cyan]{lbl_show}[/bold cyan] cr show <id>
    [bold cyan]{lbl_search}[/bold cyan] cr search <kelime>
    [bold cyan]{lbl_exp_imp}[/bold cyan] cr export | cr import <dosya>

💡 [italic]{t('tip')}[/italic]     [link=https://github.com/Joker-qp/craFTing] [bold blue]GitHub[/bold blue][/link]
"""
        rprint(guide)

@app.command("lang", help="Dil tercihini değiştir (tr / en)")
def change_language(language: str):
    if set_lang(language):
        rprint(f"[bold green]{t('lang_changed')}[/bold green] [cyan]{language.lower()}[/cyan]")
    else:
        rprint(f"[bold red]{t('invalid_lang')}[/bold red]")

# Doğrudan erişilebilir komutlar
app.command("add", help="Yeni not ekler")(add_note)
app.command("list", help="Notları listeler")(list_notes)
app.command("show", help="Not detaylarını gösterir")(show_note)
app.command("search", help="Notlarda arama yapar")(search_notes)
app.command("delete", help="Not siler")(delete_note)
app.command("export", help="Notları JSON dosyasına aktarır")(export_notes)
app.command("import", help="JSON dosyasından notları yükler")(import_notes)

@app.command()
def version():
    rprint("[bold cyan]craFTing[/bold cyan] [green]v0.1.0[/green]")
    