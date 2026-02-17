import customtkinter as ctk
import socket
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CyberScan Pro - v1.1")
        self.geometry("500x550")

        # UI Elements
        self.label = ctk.CTkLabel(self, text="Scanner de Portas", font=("Roboto", 24))
        self.label.pack(pady=20)

        self.ip_entry = ctk.CTkEntry(self, placeholder_text="IP do Alvo (ex: 8.8.8.8)", width=300)
        self.ip_entry.pack(pady=10)

        # Barra de Progresso
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0) # Inicia em 0%

        self.btn_scan = ctk.CTkButton(self, text="Iniciar Varredura", command=self.start_scan_thread)
        self.btn_scan.pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, width=400, height=200)
        self.textbox.pack(pady=20)

    def start_scan_thread(self):
        thread = threading.Thread(target=self.run_scanner)
        thread.daemon = True # Fecha a thread se o app fechar
        thread.start()

    def run_scanner(self):
        target = self.ip_entry.get()
        if not target:
            return

        self.btn_scan.configure(state="disabled")
        self.textbox.delete("0.0", "end")
        self.progress_bar.set(0)
        
        # Lista de portas (mesmas do teste anterior + algumas extras)
        ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3306, 3389, 8080]
        total_ports = len(ports)

        for i, port in enumerate(ports):
            # Atualiza a barra de progresso (valor entre 0 e 1)
            self.progress_bar.set((i + 1) / total_ports)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.5)
            
            result = sock.connect_ex((target, port))
            if result == 0:
                self.textbox.insert("end", f"[+] Porta {port}: ABERTA\n")
            
            sock.close()
        

        self.textbox.insert("end", "\n[!] Varredura completa.")
        self.btn_scan.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()