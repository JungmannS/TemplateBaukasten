import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import ttkbootstrap as tb
from core.generator import TemplateGenerator
from core.diagram import show_tree
import os
import json


class TemplateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Prompt Template-Baukasten")
        self.root.geometry("1200x750")
        self.generator = TemplateGenerator()

        self.ebenen_liste = ["Verständnis", "Hintergrund", "Teilproblem", "Planung", "Umsetzung"]
        self.actions = ["+", "?", "!", "-"]

        self._build_ui()

    def _build_ui(self):
        # Problem-Eingabe
        tb.Label(self.root, text="Problem/Prompt-Ziel:", bootstyle="primary").pack(pady=5)
        self.problem_entry = tb.Entry(self.root, width=70, bootstyle="info")
        self.problem_entry.pack(pady=5)

        # Layout-Container
        container = tb.Frame(self.root, padding=10)
        container.pack(fill=tk.BOTH, expand=True)

        # Links: Bausteine
        left = tb.Labelframe(container, text="⚙️ Bausteine", bootstyle="secondary", padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.ebene_var = tk.StringVar(value=self.ebenen_liste[0])
        self.ebene_menu = tb.Combobox(left, textvariable=self.ebene_var,
                                      values=self.ebenen_liste, state="readonly")
        self.ebene_menu.pack(pady=5, fill=tk.X)
        tb.Button(left, text="➕ Neue Ebene", bootstyle="info-outline", command=self.add_custom_ebene).pack(pady=5, fill=tk.X)

        self.action_var = tk.StringVar(value=self.actions[0])
        self.action_menu = tb.Combobox(left, textvariable=self.action_var, values=self.actions, state="readonly")
        self.action_menu.pack(pady=5, fill=tk.X)

        self.priority_var = tk.IntVar(value=1)
        tb.Label(left, text="Priorität:").pack()
        tb.Spinbox(left, from_=1, to=5, textvariable=self.priority_var, width=5, bootstyle="success").pack(pady=5)

        self.text_entry = tk.Text(left, height=4, width=30, font=("Courier New", 10))
        self.text_entry.pack(pady=5)
        tb.Button(left, text="➕ Block hinzufügen", bootstyle="success-outline", command=self.add_block).pack(pady=5, fill=tk.X)

        # Mitte: Arbeitsfläche
        mid = tb.Labelframe(container, text="📝 Arbeitsfläche", bootstyle="primary", padding=10)
        mid.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.workspace = tk.Listbox(mid, width=60, height=20)
        self.workspace.pack(fill=tk.BOTH, expand=True)

        btn_frame = tb.Frame(mid)
        btn_frame.pack(pady=5)
        tb.Button(btn_frame, text="✏️ Bearbeiten", bootstyle="warning-outline", command=self.edit_block).pack(side=tk.LEFT, padx=5)
        tb.Button(btn_frame, text="🗑️ Löschen", bootstyle="danger-outline", command=self.delete_block).pack(side=tk.LEFT, padx=5)
        tb.Button(btn_frame, text="↩️ Undo", bootstyle="secondary-outline", command=self.undo_block).pack(side=tk.LEFT, padx=5)

        # Rechts: Aktionen
        right = tb.Labelframe(container, text="🚀 Aktionen", bootstyle="secondary", padding=10)
        right.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        tb.Button(right, text="📄 Markdown generieren", bootstyle="info", command=self.generate_markdown).pack(pady=5, fill=tk.X)
        tb.Button(right, text="🌳 Baum-Text generieren", bootstyle="info", command=self.generate_tree_text).pack(pady=5, fill=tk.X)
        tb.Button(right, text="📈 Projektpfad", bootstyle="warning", command=self.show_project_path).pack(pady=5, fill=tk.X)
        tb.Button(right, text="💾 Template speichern", bootstyle="success", command=self.save_output).pack(pady=5, fill=tk.X)
        tb.Button(right, text="📂 Gespeicherte Templates", bootstyle="info-outline", command=self.show_saved_outputs).pack(pady=5, fill=tk.X)
        tb.Button(right, text="💾 Projekt speichern", bootstyle="success-outline", command=self.save_project).pack(pady=5, fill=tk.X)
        tb.Button(right, text="📂 Projekt laden", bootstyle="info-outline", command=self.load_project).pack(pady=5, fill=tk.X)

        # Ausgabe
        tb.Label(self.root, text="📤 Ausgabe", bootstyle="primary").pack(pady=5)
        self.output = tk.Text(self.root, height=15, width=110, font=("Courier New", 10))
        self.output.pack(pady=5)

    # -------------------------- #
    # Baustein-Funktionen
    # -------------------------- #
    def add_custom_ebene(self):
        neue_ebene = simpledialog.askstring("Neue Ebene", "Ebene eingeben:", parent=self.root)
        if neue_ebene and neue_ebene.strip() not in self.ebenen_liste:
            self.ebenen_liste.append(neue_ebene.strip())
            self.ebene_menu.configure(values=self.ebenen_liste)
            self.ebene_var.set(neue_ebene.strip())
        else:
            messagebox.showwarning("Warnung", "Ungültige oder doppelte Ebene!")

    def add_block(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Fehler", "Text darf nicht leer sein!")
            return
        self.generator.add_block(self.ebene_var.get(), text, self.action_var.get(), self.priority_var.get())
        self.workspace.insert(tk.END, f"[{self.action_var.get()}] {self.ebene_var.get()}: {text}")
        self.text_entry.delete("1.0", tk.END)

    def edit_block(self):
        sel = self.workspace.curselection()
        if not sel:
            messagebox.showwarning("Warnung", "Kein Block ausgewählt!")
            return
        idx = sel[0]
        block = self.generator.blocks[idx]
        self.ebene_var.set(block["ebene"])
        self.action_var.set(block["action"])
        self.priority_var.set(block["priority"])
        self.text_entry.delete("1.0", tk.END)
        self.text_entry.insert("1.0", block["text"])
        self.generator.remove_block(idx)
        self.workspace.delete(idx)

    def delete_block(self):
        sel = self.workspace.curselection()
        if not sel: return
        idx = sel[0]
        self.generator.remove_block(idx)
        self.workspace.delete(idx)
        messagebox.showinfo("Erfolg", "Block gelöscht!")

    def undo_block(self):
        if self.generator.undo():
            self.workspace.delete(tk.END)
            messagebox.showinfo("Erfolg", "Letzte Aktion rückgängig gemacht!")
        else:
            messagebox.showwarning("Warnung", "Nichts zum Rückgängigmachen!")

    # -------------------------- #
    # Ausgabe-Funktionen
    # -------------------------- #
    def generate_markdown(self):
        self.generator.user_problem = self.problem_entry.get().strip() or "Unbekanntes Problem"
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, self.generator.generate_output())

    def generate_tree_text(self):
        self.generator.user_problem = self.problem_entry.get().strip() or "Unbekanntes Problem"
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, self.generator.generate_tree_text())

    def show_project_path(self):
        self.generator.user_problem = self.problem_entry.get().strip() or "Unbekanntes Problem"
        show_tree(self.generator.user_problem, self.generator.blocks)

    def save_output(self):
        filename = simpledialog.askstring("Dateiname", "Dateiname für Template:", parent=self.root)
        if filename:
            self.generator.save_output(filename, self.generator.generate_tree_text())
            self.generator.save_output(filename,
                                       {"problem": self.generator.user_problem, "blocks": self.generator.blocks},
                                       is_json=True)
            messagebox.showinfo("Gespeichert", "Template gespeichert!")

    # -------------------------- #
    # Projekt speichern/laden
    # -------------------------- #
    def save_project(self):
        name = simpledialog.askstring("Projekt speichern", "Projektname eingeben:", parent=self.root)
        if not name: return
        self.generator.save_output(name, {"problem": self.generator.user_problem,
                                          "blocks": self.generator.blocks}, is_json=True)
        messagebox.showinfo("Gespeichert", "Projekt gespeichert.")

    def load_project(self):
        filepath = filedialog.askopenfilename(title="Projekt laden", filetypes=[("JSON Dateien", "*.json")])
        if not filepath: return
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.generator.user_problem = data["problem"]
        self.generator.blocks = data["blocks"]
        self.problem_entry.delete(0, tk.END)
        self.problem_entry.insert(0, data["problem"])
        self.workspace.delete(0, tk.END)
        for block in self.generator.blocks:
            self.workspace.insert(tk.END, f"[{block['action']}] {block['ebene']}: {block['text']}")
        messagebox.showinfo("Geladen", f"Projekt '{os.path.basename(filepath)}' geladen.")

    # -------------------------- #
    # Gespeicherte Templates anzeigen
    # -------------------------- #
    def show_saved_outputs(self):
        top = tk.Toplevel(self.root)
        top.title("Gespeicherte Templates")
        top.geometry("500x500")

        search_var = tk.StringVar()
        tb.Label(top, text="Filter:").pack(pady=2)
        tb.Entry(top, textvariable=search_var).pack(fill=tk.X, padx=5)

        lb = tk.Listbox(top)
        lb.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        def refresh_list(*args):
            lb.delete(0, tk.END)
            files = self.generator.list_saved_outputs()
            query = search_var.get().lower()
            for f in files:
                if query in f.lower():
                    lb.insert(tk.END, f)

        search_var.trace_add("write", refresh_list)
        refresh_list()

        def load_selected():
            sel = lb.curselection()
            if not sel: return
            filename = lb.get(sel[0])
            
            # Textinhalt
            content = self.generator.load_output(filename)
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, content)
            
            # JSON falls vorhanden
            json_filename = os.path.splitext(filename)[0] + ".json"
            json_path = os.path.join(self.generator.output_dir, json_filename)
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.generator.user_problem = data.get("problem", "Unbekanntes Problem")
                    self.generator.blocks = data.get("blocks", [])
                    
                    # Arbeitsfläche und Problem aktualisieren
                    self.problem_entry.delete(0, tk.END)
                    self.problem_entry.insert(0, self.generator.user_problem)
                    self.workspace.delete(0, tk.END)
                    for block in self.generator.blocks:
                        self.workspace.insert(tk.END, f"[{block['action']}] {block['ebene']}: {block['text']}")

        tb.Button(top, text="🔄 Laden", bootstyle="info", command=load_selected).pack(pady=5)

        # Sortier-Buttons
        btn_frame = tb.Frame(top)
        btn_frame.pack(pady=5)
        tb.Button(btn_frame, text="🔼 Sort A-Z", bootstyle="secondary-outline",
                  command=lambda: self._sort_list(lb, asc=True)).pack(side=tk.LEFT, padx=5)
        tb.Button(btn_frame, text="🔽 Sort Z-A", bootstyle="secondary-outline",
                  command=lambda: self._sort_list(lb, asc=False)).pack(side=tk.LEFT, padx=5)

    def _sort_list(self, lb, asc=True):
        files = sorted(self.generator.list_saved_outputs(), reverse=not asc)
        lb.delete(0, tk.END)
        for f in files:
            lb.insert(tk.END, f)


if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    app = TemplateGUI(root)
    root.mainloop()
