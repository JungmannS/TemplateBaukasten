from gui.app import TemplateGUI
import tkinter as tk
import ttkbootstrap as tb

def main():
    root = tb.Window(themename="flatly")  # ttkbootstrap-Theme
    app = TemplateGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
