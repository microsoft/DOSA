import os

def get_clues(clue_path):
    with open(clue_path, "r") as f:
        clues = [s.strip() for s in f.readlines()]
    output = ""
    for i, clue in enumerate(clues):
        output += f"CLUE-{i+1}: {clue}\n"
    return output.strip()

def generate_abs_path(relative_path):
    file_abs_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(file_abs_path,relative_path)