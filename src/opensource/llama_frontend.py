from src.opensource.llama_backend import generate_text
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import HuggingFacePipeline


def get_clues(clue_path):
    with open(clue_path, "r") as f:
        clues = [s.strip() for s in f.readlines()]
    output = ""
    for i, clue in enumerate(clues):
        output += f"CLUE-{i+1}: {clue}\n"
    return output.strip()


def chat_pipeline(clue_list: str, prompt_text: str, conversation_buffer=None):
    if conversation_buffer is None:
        raise ValueError(
            "Please provide a conversation buffer object for the LLMChain to work"
        )

    llm = HuggingFacePipeline(pipeline=generate_text())
    prompt_template = PromptTemplate.from_template(prompt_text)
    prompt_template = prompt_template.partial(cluelist=clue_list)

    chatgpt_chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        verbose=False,
        memory=conversation_buffer,
        llm_kwargs={"max_length": 4096},
    )
    return chatgpt_chain


if __name__ == "__main__":
    pass
