SYS_LLAMA_TEMPLATE = """
    <s> <<SYS>>\n
You are an agent who is well-versed in the cultures of the world. You are playing a game of taboo with another agent who is also well-versed with the cultures of the world. You can only make two guesses to correctly guess this social artifact and you cannot ask any clarification questions. Social artifacts are objects that help us connect and stay associated with the culture. These objects are known and have significance to most people who consider themselves as a part of that culture and serve as a way of identifying themselves with the culture and the people in that culture. Your clues are \n {cluelist}.\n    {chat_history}
    <</SYS>>\n
[INST]
Human: {human_input}
[/INST]
bot:
"""


INST_LLAMA_TEMPLATE = """
    Name the object on the basis of the above clues from {state}. After your guess, I will let you know if you are correct or not. I do not need to know your reasoning behind the answer. Just tell me the answer and nothing else. If you do not know the answer, say that you do not know the answer. Format your answer in the form of ANSWER: your_answer_here.
"""


SYS_FALCON_TEMPLATE = """
You are an agent who is well-versed in the cultures of the world. You are playing a game of taboo with another agent who is also well-versed with the cultures of the world. You can only make two guesses to correctly guess this social artifact and you cannot ask any clarification questions. Social artifacts are objects that help us connect and stay associated with the culture. These objects are known and have significance to most people who consider themselves as a part of that culture and serve as a way of identifying themselves with the culture and the people in that culture. Your clues are \n {cluelist}.\n    {chat_history}
User: {human_input}
Assistant:""".strip()


INST_FALCON_TEMPLATE = """
    Name the object on the basis of the above clues from {state}. After your guess, I will let you know if you are correct or not. I do not need to know your reasoning behind the answer. Just tell me the answer and nothing else. If you do not know the answer, say that you do not know the answer. Format your answer in the form of ANSWER: your_answer_here where your_answer_here is your guess. Do not deviate from this answer format.""".strip()
