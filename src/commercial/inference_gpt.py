import warnings
import openai
from dotenv import load_dotenv
from utils import load_openai_env_variables
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from src.commercial.templates import SYS_GPT_TEMPLATE, INST_GPT_TEMPLATE
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory

import os

from backoff import on_exception, expo

CHAT_MODELS = [
    "gpt-4",
    "gpt-35-turbo",
    "gpt-35-turbo-16k",
    "gpt-4-32k",
]


load_dotenv()
load_openai_env_variables()





@on_exception(expo, openai.error.RateLimitError)
def gpt_chat_pipeline(
    llm,
    clue_list: str,
    prompt_text: str,
    conversation_buffer=None,
    model_name: str = "gpt-35-turbo",
):
    if conversation_buffer is None:
        raise ValueError(
            "Please provide a conversation buffer object for the LLMChain to work"
        )

    llm = AzureChatOpenAI(
        engine=model_name,
        deployment_name=model_name,
        openai_api_key=os.environ["OPENAI_API_KEY"],
        openai_api_base=os.environ["OPENAI_END_POINT"],
        openai_api_type=os.environ["OPENAI_API_TYPE"],
        openai_api_version=os.environ["OPENAI_API_VERSION"],
        temperature=0,
    )

    prompt_template = PromptTemplate(input_variables=["cluelist", "chat_history", "input"], template=prompt_text)
    prompt_template = prompt_template.partial(cluelist=clue_list)

    gpt_chain = ConversationChain(
        llm=llm,
        prompt=prompt_template,
        verbose=False,
        memory=conversation_buffer,
    )
    # gpt_chain = LLMChain(
    #     llm=llm,
    #     prompt=prompt_template,
    #     verbose=False,
    #     memory=conversation_buffer,
    # )
    # ConversationBufferMemory(ai_prefix="Agent", memory_key="chat_history")
    return gpt_chain


    # output = gpt3x_completion("you are an experienced travel agent.", "give me an itinerary for a trip to iceland for 10 days", "gpt-4")
    # print(output)

if __name__ == "__main__":
    cluelist = 'CLUE-1: Quite a famous summer punjabi drink\nCLUE-2: It is made using curd'
    model_name = "gpt-4"
    llm = AzureChatOpenAI(
        engine=model_name,
        deployment_name=model_name,
        openai_api_key=os.environ["OPENAI_API_KEY"],
        openai_api_base=os.environ["OPENAI_END_POINT"],
        openai_api_type=os.environ["OPENAI_API_TYPE"],
        openai_api_version=os.environ["OPENAI_API_VERSION"],
        temperature=0,
    )
    agent = gpt_chat_pipeline(clue_list=cluelist, prompt=SYS_GPT_TEMPLATE)
    inst_prompt_template = PromptTemplate.from_template(INST_GPT_TEMPLATE)
    inst_input = inst_prompt_template.template.format(state="Punjab")
    ans = agent.predict(input=inst_input)
    tt = type(ans)
    print(tt)
