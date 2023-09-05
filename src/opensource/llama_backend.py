from torch import cuda
from dotenv import load_dotenv
import torch
import warnings
warnings.filterwarnings("ignore")

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    AutoConfig,
    StoppingCriteria,
    StoppingCriteriaList,
    pipeline
)

import os

load_dotenv()

model_id = "meta-llama/Llama-2-13b-chat-hf"


device = f"cuda:{cuda.current_device()}" if cuda.is_available() else "cpu"



# begin initializing HF items, you need an access token

def get_model_tokenizer(model_id, hf_token=os.getenv("HF_TOKEN")):
    model_config = AutoConfig.from_pretrained(model_id, use_auth_token=hf_token)
    model = AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    config=model_config,
    device_map='auto',
    use_auth_token=hf_token,
)
    tokenizer = AutoTokenizer.from_pretrained(model_id, use_auth_token=hf_token)
    return model, tokenizer    


model, tokenizer = get_model_tokenizer(model_id=model_id)


stop_list = ["\nHuman:", "\n```\n"]

stop_token_ids = [tokenizer(x)["input_ids"] for x in stop_list]
stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]


class StopOnTokens(StoppingCriteria):
    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> bool:
        for stop_ids in stop_token_ids:
            if torch.eq(input_ids[0][-len(stop_ids) :], stop_ids).all():
                return True
        return False


stopping_criteria = StoppingCriteriaList([StopOnTokens()])



def generate_text():
    return pipeline(
        model=model,
        tokenizer=tokenizer,
        return_full_text=True,  # langchain expects the full text
        # task="text2text-generation",
        task="text-generation",
        # we pass model parameters here too
        stopping_criteria=stopping_criteria,  # without this model rambles during chat
        temperature=0.1,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
        max_new_tokens=4096,  # max number of tokens to generate in the output
        repetition_penalty=1.1,  # without this output begins repeating
        do_sample=True,
    )




def decode_output(model, tokenizer, pr):
    model.eval()
    model_inputs = tokenizer(pr, return_tensors="pt").to("cuda:0")
    input_ids = model_inputs["input_ids"]
    output = model.generate(**model_inputs, do_sample=False, max_length=2048)
    # return (tokenizer.decode(output[0], skip_special_tokens=True))
    return tokenizer.decode(output[0, input_ids.shape[1] :], skip_special_tokens=True)

if __name__ == "__main__":
    # ans = decode_output(model, tokenizer, temp_template)
    pipe = generate_text()
    # print(ans)

