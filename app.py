from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Log, ProgressBar
from textual.reactive import reactive
from textual.containers import Horizontal
import os, asyncio
from main import detectar_qr_codes, move_to_folder


class QRApp(App):
    CSS = """
    #welcome {
        text-align: center;
        color: cyan;
        margin: 1 0;
    }
    #status {
        color: yellow;
        margin: 1 0;
        text-align: center;
    }
    #buttons {
    align: center middle;
    margin: 1 0;
    }
    #start, #refresh {
        width: 20%;
        margin: 0 2;
    }

    #start {
        margin: 1 0;
        width: 50%;
        align: center middle;
    }
    #log {
        height: 20;
        border: round green;
        margin: 1 2;
    }
    #progress {
        width: 80%;
        height: 1;
        margin: 1 0;
        align: center middle;
    }
    """

    progress_value = reactive(0)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(" Poupa tempo 40k\n", id="welcome")
        yield Static("", id="status")
        yield Static("  Como usar:\n", id="Tutorial")
        yield Static(" 1) Meta os arquivos dentro da pasta 'imgs-raw'\n", id="t1")
        yield Static(" 2) Atualize a lista de arquivos\n", id="t2")
        yield Static(" 3) Aperta o play\n", id="t3")
        yield Static(" 4) Feito! Os arquivos processados irão aparecer na pasta 'imgs_new'\n", id="t4")
        yield Button("▶ Iniciar processamento", id="start")
        yield Button("🔄 Atualizar lista", id="refresh")
        yield ProgressBar(id="progress", show_percentage=True)
        yield Log(id="log")
        yield Static("v.1.1")
        yield Footer()


    def on_mount(self):
        self.folder = "imgs-raw"
        status = self.query_one("#status")

        # Cria automaticamente se não existir
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            status.update("[yellow]📁 Pasta 'imgs-raw' criada automaticamente![/yellow]")
            self.files = []
        else:
            self.files = [f for f in os.listdir(self.folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
            total = len(self.files)
            status.update(f"[yellow]📂 {total} arquivo(s) encontrado(s) em '{self.folder}'.[/yellow]")
            self.query_one("#progress").total = total
        self.refresh_folder()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "start":
            self.query_one("#log").clear()
            self.progress_value = 0
            self.run_worker(self.processar, thread=True)

        elif event.button.id == "refresh":
            self.refresh_folder()

    def refresh_folder(self):
        status = self.query_one("#status")
        log = self.query_one("#log")
        pb = self.query_one("#progress")

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            status.update("📁 Pasta 'imgs-raw' criada automaticamente!")
            log.write("📁 Pasta 'imgs-raw' criada automaticamente!\n")
            self.files = []
            pb.total = 1
            pb.progress = 0
            return

        self.files = [f for f in os.listdir(self.folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        total = len(self.files)

        if total > 0:
            status.update(f"📂 {total} arquivo(s) encontrado(s) em '{self.folder}'.")
            log.write(f"🔄 Pasta recarregada! {total} arquivo(s) encontrados.\n")
        else:
            status.update("❌ Nenhum arquivo encontrado em 'imgs-raw'.")
            log.write("⚠ Nenhum arquivo encontrado após atualizar.\n")

        pb.total = total or 1
        pb.progress = 0


    async def processar(self):
        log = self.query_one("#log")
        pb = self.query_one("#progress")

        total = len(self.files)
        if total == 0:
            log.write("❌ Nenhum arquivo encontrado em imgs-raw.\n")
            return

        for file in self.files:
            path = os.path.join(self.folder, file)
            try:
                qr_codes = detectar_qr_codes(path)
                code = qr_codes[0] if qr_codes else None
                move_to_folder(self.folder, file, code)

                if code:
                    log.write(f"✔ QR code detectado em {file}\n")
                else:
                    log.write(f"⚠ Nenhum QR code detectado em {file}\n")
            except Exception as e:
                log.write(f"✖ Erro ao processar {file}: {e}\n")

            pb.advance(1)
            await asyncio.sleep(0.05)  # mantém fluidez da interface

        log.write("\n✅ Feito!\n")

if __name__ == "__main__":
    QRApp().run()
