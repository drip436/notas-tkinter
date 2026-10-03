import os
import json
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class NotasApp(tk.Tk):
    """Aplicación para gestión de notas rápidas en Tkinter."""

    ARCHIVO_NOTAS = "notas.json"

    def __init__(self):
        super().__init__()
        
        # 1. Configuración general y centrado de la ventana
        self.title("Mis Notas Rápidas")
        ancho, alto = 550, 580
        pos_x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        pos_y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")

        # Estado inicial
        self.notas = []          # Lista principal de notas
        self.es_modo_oscuro = True
        self.style = ttk.Style(self)
        
        # 2. Inicializar interfaz y cargar datos
        self._configurar_interfaz()
        self._aplicar_tema()
        self.cargar_notas()

    def _configurar_interfaz(self):
        """Crea y organiza todos los widgets centrados en la interfaz."""
        
        # Frame Principal Contenedor
        self.main_frame = ttk.Frame(self, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        # Header: Título y Botón de Tema (Claro/Oscuro)
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill="x", pady=(0, 10))

        lbl_titulo = ttk.Label(header_frame, text="✨ Mis Notas", font=("Segoe UI", 16, "bold"))
        lbl_titulo.pack(side="left")

        self.btn_tema = ttk.Button(header_frame, text="☀️ Modo Claro", command=self.alternar_tema, width=14)
        self.btn_tema.pack(side="right")

        # Campo de entrada de nuevas notas
        lbl_entrada = ttk.Label(self.main_frame, text="Nueva Nota:", font=("Segoe UI", 10))
        lbl_entrada.pack(anchor="center", pady=(5, 2))

        self.input_nota = ttk.Entry(self.main_frame, font=("Segoe UI", 11), justify="center")
        self.input_nota.pack(fill="x", pady=(0, 10), ipady=4)
        self.input_nota.bind("<Return>", lambda event: self.agregar_nota())

        # Fila de Botones de Acción
        frame_acciones = ttk.Frame(self.main_frame)
        frame_acciones.pack(anchor="center", pady=(0, 10))

        btn_agregar = ttk.Button(frame_acciones, text="➕ Agregar", command=self.agregar_nota, width=12)
        btn_agregar.pack(side="left", padx=4)

        btn_editar = ttk.Button(frame_acciones, text="✏️ Editar", command=self.editar_nota, width=12)
        btn_editar.pack(side="left", padx=4)

        btn_eliminar = ttk.Button(frame_acciones, text="🗑️ Eliminar", command=self.eliminar_nota, width=12)
        btn_eliminar.pack(side="left", padx=4)

        # Filtro / Búsqueda en tiempo real
        lbl_buscar = ttk.Label(self.main_frame, text="🔍 Buscar nota:", font=("Segoe UI", 10))
        lbl_buscar.pack(anchor="center", pady=(10, 2))

        self.input_buscar = ttk.Entry(self.main_frame, font=("Segoe UI", 10), justify="center")
        self.input_buscar.pack(fill="x", pady=(0, 10))
        self.input_buscar.bind("<KeyRelease>", lambda event: self.filtrar_notas())

        # Contador de notas
        self.var_contador = tk.StringVar(value="0 notas registradas")
        lbl_contador = ttk.Label(self.main_frame, textvariable=self.var_contador, font=("Segoe UI", 9, "italic"))
        lbl_contador.pack(pady=(0, 5))

        # Lista de Notas (Listbox)
        self.lista_box = tk.Listbox(
            self.main_frame, font=("Segoe UI", 11), justify="center", bd=1, relief="solid", activestyle="none"
        )
        self.lista_box.pack(fill="both", expand=True, pady=(0, 5))
        self.lista_box.bind("<Double-Button-1>", lambda event: self.editar_nota())

    # =========================================================
    # EXTENSIÓN: TEMAS CLARO Y OSCURO (ttk)
    # =========================================================
    def _aplicar_tema(self):
        """Aplica la paleta de colores según el tema activo."""
        if self.es_modo_oscuro:
            bg_color, fg_color, entry_bg = "#1e1e2e", "#cdd6f4", "#313244"
            select_bg, select_fg = "#89b4fa", "#11111b"
            self.btn_tema.config(text="☀️ Modo Claro")
        else:
            bg_color, fg_color, entry_bg = "#f5f5f5", "#11111b", "#ffffff"
            select_bg, select_fg = "#2563eb", "#ffffff"
            self.btn_tema.config(text="🌙 Modo Oscuro")

        self.configure(bg=bg_color)
        self.style.theme_use("clam")

        # Configuración de estilos ttk
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabel", background=bg_color, foreground=fg_color)
        self.style.configure("TEntry", fieldbackground=entry_bg, foreground=fg_color)
        self.style.configure("TButton", font=("Segoe UI", 9, "bold"), padding=4)

        # Configurar Listbox nativa
        self.lista_box.config(
            bg=entry_bg, fg=fg_color, selectbackground=select_bg, selectforeground=select_fg
        )

    def alternar_tema(self):
        """Cambia entre tema claro y oscuro."""
        self.es_modo_oscuro = not self.es_modo_oscuro
        self._aplicar_tema()

    # =========================================================
    # LÓGICA DE EVENTOS Y ACCIONES
    # =========================================================
    def actualizar_contador(self):
        n = len(self.notas)
        self.var_contador.set(f"{n} nota registrada" if n == 1 else f"{n} notas registradas")

    def agregar_nota(self):
        texto = self.input_nota.get().strip()
        if texto:
            self.notas.append(texto)
            self.input_nota.delete(0, "end")
            self.guardar_notas()
            self.filtrar_notas()

    def eliminar_nota(self):
        sel = self.lista_box.curselection()
        if not sel:
            messagebox.showinfo("Atención", "Selecciona una nota para eliminar.")
            return
        
        texto_seleccionado = self.lista_box.get(sel[0])
        if texto_seleccionado in self.notas:
            self.notas.remove(texto_seleccionado)
            self.guardar_notas()
            self.filtrar_notas()

    def editar_nota(self):
        sel = self.lista_box.curselection()
        if not sel:
            messagebox.showinfo("Atención", "Selecciona una nota para editar.")
            return
        
        texto_actual = self.lista_box.get(sel[0])
        idx_real = self.notas.index(texto_actual)

        nuevo_texto = simpledialog.askstring("Editar Nota", "Modifica tu nota:", initialvalue=texto_actual)
        if nuevo_texto and nuevo_texto.strip():
            self.notas[idx_real] = nuevo_texto.strip()
            self.guardar_notas()
            self.filtrar_notas()

    # =========================================================
    # EXTENSIÓN: FILTRO / BÚSQUEDA EN TIEMPO REAL
    # =========================================================
    def filtrar_notas(self):
        """Filtra la lista mostrada según el texto ingresado en la búsqueda."""
        criterio = self.input_buscar.get().strip().lower()
        self.lista_box.delete(0, "end")

        for nota in self.notas:
            if criterio in nota.lower():
                self.lista_box.insert("end", nota)

        self.actualizar_contador()

    # =========================================================
    # EXTENSIÓN: PERSISTENCIA SIMPLE (JSON)
    # =========================================================
    def guardar_notas(self):
        """Guarda la lista de notas en un archivo JSON."""
        try:
            with open(self.ARCHIVO_NOTAS, "w", encoding="utf-8") as f:
                json.dump(self.notas, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar las notas: {e}")

    def cargar_notas(self):
        """Carga las notas desde el archivo JSON si existe."""
        if os.path.exists(self.ARCHIVO_NOTAS):
            try:
                with open(self.ARCHIVO_NOTAS, "r", encoding="utf-8") as f:
                    self.notas = json.load(f)
                self.filtrar_notas()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron cargar las notas: {e}")


if __name__ == "__main__":
    app = NotasApp()
    app.mainloop()