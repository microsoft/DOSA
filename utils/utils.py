
def get_clues(clue_path):
    with open(clue_path, "r") as f:
        clues = [s.strip() for s in f.readlines()]
    output = ""
    for i, clue in enumerate(clues):
        output += f"CLUE-{i+1}: {clue}\n"
    return output.strip()