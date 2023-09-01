from src.opensource.llama_backend import decode_output, generate_text
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import HuggingFacePipeline
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import load_tools
from langchain.agents import initialize_agent


sys_template = """
    <s> <<SYS>>\n
    You are an agent who is well versed with the cultures of the world. You are playing a game of taboo with another agent who is also well- versed with the cultures of the world. You can only make two guesses to correctly guess this social artifact and you cannot ask any clarification questions. Social artifacts are objects that helps us connect and stay associated with the culture. These objects are known and have a significance to most people who consider themselves as a part of that culture and serve as way of identifying ourselves with the culture and the people in that culture. Your clues are \n {cluelist}.\n 
    {chat_history}
    <</SYS>>\n
[INST]
Human: {human_input}
[/INST]
bot:
"""

inst_template = """
    [INST] Name the object on the basis of the above clues. After your guess, I will let you know if you are correct or not. Accordingly, make your second and final guess. I do not need to know your reasoning behind the answer. Just tell me the answer. If you do not know the answer, say that you do not know the answer.[/INST]
"""

human_msg = inst_template + "\nUser: {input}"

def get_clues(clues):
    output = ""
    for i, clue in enumerate(clues):
        output += f"CLUE-{i+1}: {clue}\n"
    return len(clues), output.strip()


with open("/home/t-sahuja/cultural_artifacts/clues/WB20.txt", "r") as f:
    clues = [s.strip() for s in f.readlines()]
    
num_clues, clues_string = get_clues(clues)


prompt_template_1 = PromptTemplate.from_template(sys_template)
partial_template = prompt_template_1.partial(cluelist=clues_string)    



# sys_prompt = prompt_template.format(cluelist=clues_string)


def chat_pipeline():
    llm = HuggingFacePipeline(pipeline=generate_text())
    # memory = ConversationBufferWindowMemory(
    #     memory_key="chat_history", k=5, return_messages=True, output_key="output"
    # )

    chatgpt_chain = LLMChain(
        llm=llm,
        prompt=partial_template,
        verbose=False,
        memory=ConversationBufferWindowMemory(k=2, memory_key='chat_history'),
        llm_kwargs={"max_length": 4096},
    )
    return chatgpt_chain
    #     tools = load_tools(["llm-math"], llm=llm)

    #     agent = initialize_agent(
    #         agent="chat-conversational-react-description",
    #         tools=tools,
    #         llm=llm,
    #         verbose=True,
    #         early_stopping_method="generate",
    #         memory=memory,
    #     )
    #     new_prompt = agent.agent.create_prompt(
    #     system_message=sys_prompt,
    #     tools=tools
    # )
    #     agent.agent.llm_chain.prompt = new_prompt
    #     agent.agent.llm_chain.prompt.messages[2].prompt.template = human_msg
    return agent


if __name__ == "__main__":
    # print(prompt)
    # decode_output("Create a course structure for Database Management Systems")
    decode_output(prompt)
