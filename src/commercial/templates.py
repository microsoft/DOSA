SYS_PALM_TEMPLATE = """

You are an agent who is well versed with the cultures of the world. You are playing a game of taboo with another agent who is also well- versed with the cultures of the world. You can only make two guesses to correctly guess this social artifact and you cannot ask any clarification questions. Social artifacts are objects that helps us connect and stay associated with the culture. These objects are known and have a significance to most people who consider themselves as a part of that culture and serve as way of identifying ourselves with the culture and the people in that culture. Your clues are: \n {cluelist}.\n

"""

INST_PALM_TEMPLATE = """
   Name the object on the basis of the above clues from {state}. After your guess, I will let you know if you are correct or not. I do not need to know your reasoning behind the answer. Just tell me the answer and nothing else. If you do not know the answer, say that you do not know the answer. Do not continue the conversation. Wait for my instruction. Format your answer in the form of ANSWER: your_answer_here.
"""

SYS_GPT_TEMPLATE = """

You are an agent who is well versed with the cultures of the world. You are playing a game of taboo with another agent who is also well- versed with the cultures of the world. You can only make two guesses to correctly guess this social artifact and you cannot ask any clarification questions. Social artifacts are objects that helps us connect and stay associated with the culture. These objects are known and have a significance to most people who consider themselves as a part of that culture and serve as way of identifying ourselves with the culture and the people in that culture. Your clues are: \n {cluelist}.\n

{chat_history}

Human: {input}
Agent:

"""

INST_GPT_TEMPLATE = """
   Name the object on the basis of the above clues from {state}. I do not need to know your reasoning behind the answer. Just tell me the answer and nothing else. If you do not know the answer, say that you do not know the answer. Format your answer in the form of ANSWER: your_answer_here.
"""