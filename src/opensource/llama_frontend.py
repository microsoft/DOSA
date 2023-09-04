from src.opensource.llama_backend import generate_text
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import HuggingFacePipeline
from langchain.memory import ConversationBufferWindowMemory
from src.opensource.templates import SYS_LLAMA_TEMPLATE


def get_clues(clues):
    output = ""
    for i, clue in enumerate(clues):
        output += f"CLUE-{i+1}: {clue}\n"
    return len(clues), output.strip()


with open("/home/t-sahuja/cultural_artifacts/clues/WB20.txt", "r") as f:
    clues = [s.strip() for s in f.readlines()]

num_clues, clues_string = get_clues(clues)


prompt_template_1 = PromptTemplate.from_template(SYS_LLAMA_TEMPLATE)
partial_template = prompt_template_1.partial(cluelist=clues_string)


def chat_pipeline(prompt_text, partial_template=False):
    llm = HuggingFacePipeline(pipeline=generate_text())
    prompt_template = PromptTemplate.from_template(prompt_text)
    if partial_template:
        prompt_template = prompt_template.partial(cluelist=clues_string)
    
    chatgpt_chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        verbose=False,
        memory=ConversationBufferWindowMemory(k=2, memory_key="chat_history"),
        llm_kwargs={"max_length": 4096},
    )
    return chatgpt_chain


if __name__ == "__main__":
    pass
