import os
import json

class TemplateGenerator:
    def __init__(self, user_problem="Unbekanntes Problem"):
        self.user_problem = user_problem
        self.blocks = []
        self.history = []
        self.output_dir = "data/outputs"
        os.makedirs(self.output_dir, exist_ok=True)

    def add_block(self, ebene, text, action, priority):
        block = {
            "ebene": ebene,
            "text": text,
            "action": action,
            "priority": priority
        }
        self.blocks.append(block)
        self.history.append({"action": "add", "block": block})

    def remove_block(self, index):
        if 0 <= index < len(self.blocks):
            block = self.blocks.pop(index)
            self.history.append({"action": "remove", "block": block, "index": index})

    def undo(self):
        if not self.history:
            return None
        last = self.history.pop()
        if last["action"] == "add":
            self.blocks.remove(last["block"])
        elif last["action"] == "remove":
            self.blocks.insert(last["index"], last["block"])
        elif last["action"] == "edit":
            old_block, _, index = last
            self.blocks[index] = old_block
            return {"action": "edit", "block": old_block, "index": index}
        return last["block"]

    def generate_output(self):
        """Generiert Markdown-Ausgabe nach Ebenen und Priorität."""
        output = f"## Problem: {self.user_problem}\n\n"
        ebenen_dict = {}
        for b in self.blocks:
            if b["ebene"] not in ebenen_dict:
                ebenen_dict[b["ebene"]] = []
            stars = "*" * b["priority"]
            ebenen_dict[b["ebene"]].append(f"[{b['action']}] {stars}: {b['text']}")

        for ebene, blks in ebenen_dict.items():
            output += f"### {ebene}\n"
            for blk in blks:
                output += f"{blk}\n"
            output += "\n"
        return output

    def generate_tree_text(self):
        """Generiert LLM-kompatible schematische Baum-Textdarstellung."""
        tree_text = f"Problem: {self.user_problem}\n"
        ebenen_dict = {}
        for b in self.blocks:
            ebenen_dict.setdefault(b["ebene"], []).append(b)
        for ebene, blks in ebenen_dict.items():
            tree_text += f"├─ {ebene}\n"
            for blk in blks:
                stars = "*" * blk["priority"]
                tree_text += f"│  ├─ [{blk['action']}] {stars} {blk['text']}\n"
        return tree_text

    def save_output(self, filename, content, is_json=False):
        os.makedirs(self.output_dir, exist_ok=True)
        if is_json:
            if not filename.endswith(".json"):
                filename += ".json"
            path = os.path.join(self.output_dir, filename)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(content, f, indent=2)
        else:
            if not filename.endswith(".txt"):
                filename += ".txt"
            path = os.path.join(self.output_dir, filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        return path

    def list_saved_outputs(self):
        return sorted([f for f in os.listdir(self.output_dir) if f.endswith(".txt")])

    def load_output(self, filename):
        path = os.path.join(self.output_dir, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return ""