from utils import generate_abs_path

STATE_CLUES_NOTES_DICT = {
    "jharkhand": [
        generate_abs_path("clues/jharkhand/artifact_clues.csv"),
        generate_abs_path("clues/jharkhand/notes.csv"),
    ],
    "assam": [
        generate_abs_path("clues/assam/artifacts_clues.csv"),
        generate_abs_path("clues/assam/notes.csv"),
    ],
    "gujarat": [generate_abs_path("clues/gujarat/gujarat_clues.csv")],
    "karnataka": [
        generate_abs_path("clues/karnataka/karnataka_clues.csv"),
        generate_abs_path("clues/karnataka/karnataka_notes.csv"),
    ],
    "maharashtra": [
        generate_abs_path("clues/maharashtra/maharashtra_clues.csv"),
        generate_abs_path("clues/maharashtra/maharashtra_notes.csv"),
    ],
    "odisha": [
        generate_abs_path("clues/odisha/artifact_clues.csv"),
        generate_abs_path("clues/odisha/notes.csv"),
    ],
    "punjab": [
        generate_abs_path("clues/punjab/punjab_clues.csv"),
        generate_abs_path("clues/punjab/punjab_notes.csv"),
    ],
    "tamil_nadu": [
        generate_abs_path("clues/tamil_nadu/tamil_clues.csv"),
        generate_abs_path("clues/tamil_nadu/tamil_notes.csv"),
    ],
    "telangana": [
        generate_abs_path("clues/telangana/clues_artifact.csv"),
        generate_abs_path("clues/telangana/notes.csv"),
    ],
    "west_bengal": [generate_abs_path("clues/west_bengal/west_bengal_clues.csv")],
    "kerala": [
        generate_abs_path("clues/kerala/kerala_clues.csv"),
        generate_abs_path("clues/kerala/kerala_notes.csv"),
    ],
    "chattisgarh": [generate_abs_path("clues/chhattisgarh/artifact_clues.csv")],
    "delhi": [generate_abs_path("clues/delhi/delhi_clues.csv")],
    "bihar": [
        generate_abs_path("clues/bihar/bihar_clues.csv"),
        generate_abs_path("clues/bihar/bihar_notes.csv"),
    ],
    "andhra_pradesh":[
        generate_abs_path("clues/andhra_pradesh/andhra_clues.csv"),
        generate_abs_path("clues/andhra_pradesh/notes_clues.csv")
    ]
}
