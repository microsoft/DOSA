from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def chat_pipeline(llm, clue_list: str, prompt_text: str, conversation_buffer=None):
    if conversation_buffer is None:
        raise ValueError(
            "Please provide a conversation buffer object for the LLMChain to work"
        )

    prompt_template = PromptTemplate.from_template(prompt_text)
    prompt_template = prompt_template.partial(cluelist=clue_list)
    llama_chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        verbose=False,
        memory=conversation_buffer,
        llm_kwargs={"max_length": 4096},
    )
    return llama_chain


if __name__ == "__main__":
    pass
