from src.llama.llama_backend import decode_output
from langchain.prompts import PromptTemplate


template = """
    <s> <<SYS>>\n
    You are an agent who is well versed with the cultures of the world. You are playing a game of taboo with another agent who is also well versed with the cultures of the world.You can only make two guesses and you cannot ask any clarification questions.Print the guesses in a separate line.Social artifacts are objects that helps us connect and stay associated with the culture. These objects are known and have a significance to most people who consider themselves as a part of that culture and serve as way of identifying ourselves with the culture and the people in that culture. Your clues are \n {cluelist}.\n 
    <</SYS>>\n
    [INST] Name the object on the basis of the above {num_clues} clues. I do not need to know your reasoning behind the answer. Just tell me the answer. If you do not know the answer, say that you do not know the answer.[/INST]
"""

prompt_template = PromptTemplate.from_template(template)


def get_clues(clues):
    output = ""
    for i, clue in enumerate(clues):
        output += f"CLUE-{i+1}: {clue}\n"
    return len(clues), output.strip()


with open("clues/WB20.txt", "r") as f:
    clues = [s.strip() for s in f.readlines()]

num_clues, clues_string = get_clues(clues)
prompt = prompt_template.format(cluelist=clues_string, num_clues=num_clues)


if __name__ == "__main__":
    # print(prompt)
    # decode_output("Create a course structure for Database Management Systems")
    decode_output(prompt)
