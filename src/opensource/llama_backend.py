from torch import cuda
from dotenv import load_dotenv
import torch
import warnings

warnings.filterwarnings("ignore")

from transformers import (
    AutoTokenizer,
    AutoConfig,
    StoppingCriteria,
    StoppingCriteriaList,
    AutoModelForCausalLM,
    pipeline,
)

import os

load_dotenv()

# model_id = "meta-llama/Llama-2-13b-chat-hf"
# model_id = "ichitaka/falcon-40b-instruct-8bit"

device = f"cuda:{cuda.current_device()}" if cuda.is_available() else "cpu"


# begin initializing HF items, you need an access token


def get_model_tokenizer(model_id, hf_token=os.getenv("HF_TOKEN")):
    model_config = AutoConfig.from_pretrained(
        model_id, use_auth_token=hf_token, trust_remote_code=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        trust_remote_code=True,
        config=model_config,
        device_map="auto",
        use_auth_token=hf_token,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_id, use_auth_token=hf_token, return_token_type_ids=False
    )
    return model, tokenizer


class StopOnTokens(StoppingCriteria):
    def __init__(self, stop_token_ids):
        self.stop_token_ids = stop_token_ids

    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> bool:
        input_ids = input_ids.to(device)
        for stop_ids in self.stop_token_ids:
            if torch.eq(input_ids[0][-len(stop_ids) :], stop_ids).all():
                return True
        return False


def generate_text(
    model_id: str, temperature=0.1, repetition_penalty=1.1, do_sample=False
):
    model, tokenizer = get_model_tokenizer(model_id=model_id)
    stop_list = ["\nHuman:", "\n```\n"]

    stop_token_ids = [tokenizer(x)["input_ids"] for x in stop_list]
    stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]
    stop_on_tokens = StopOnTokens(stop_token_ids)
    stopping_criteria = StoppingCriteriaList([stop_on_tokens])
    return pipeline(
        model=model,
        eos_token_id=tokenizer.eos_token_id,
        tokenizer=tokenizer,
        return_full_text=True,  # langchain expects the full text
        # task="text2text-generation",
        task="text-generation",
        trust_remote_code=True,
        # we pass model parameters here too
        stopping_criteria=stopping_criteria,  # without this model rambles during chat
        temperature=temperature,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
        max_new_tokens=500,  # max number of tokens to generate in the output
        repetition_penalty=repetition_penalty,  # without this output begins repeating
        do_sample=do_sample,
        torch_dtype=torch.bfloat16,
    )


def decode_output(model, tokenizer, pr):
    model.eval()
    model_inputs = tokenizer(pr, return_tensors="pt", return_token_type_ids=False).to(
        "cuda:0"
    )
    input_ids = model_inputs["input_ids"]
    output = model.generate(**model_inputs, do_sample=False, max_length=2048)
    # return (tokenizer.decode(output[0], skip_special_tokens=True))
    return tokenizer.decode(output[0, input_ids.shape[1] :], skip_special_tokens=True)


temp_template = """
You are an agent who is well versed with the cultures of the world. You are playing a game of taboo with another agent who is also well- versed with the cultures of the world. You can only make two guesses to correctly guess this social artifact and you cannot ask any clarification questions. Social artifacts are objects that helps us connect and stay associated with the culture. These objects are known and have a significance to most people who consider themselves as a part of that culture and serve as way of identifying ourselves with the culture and the people in that culture. Your clues are:
CLUE-1: A handicraft form to make household furniture like table and chair
CLUE-2: The material is very flexible and cheap to manifacture.
User: Name the object on the basis of the above clues from Assam. After your guess, I will let you know if you are correct or not. Just tell me the answer and nothing else. If you do not know the answer, say that you do not know the answer. Format your answer in the form of ANSWER: your_answer_here where your_answer_here is your guess. Do not deviate from this answer format.
Assistant:
""".strip()


if __name__ == "__main__":
    model, tokenizer = get_model_tokenizer(model_id="tiiuae/falcon-7b-instruct")
    ans = decode_output(model, tokenizer, temp_template)
    print(ans)
