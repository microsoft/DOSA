from torch import cuda, bfloat16
from dotenv import load_dotenv
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    AutoConfig,
    StoppingCriteria,
    StoppingCriteriaList,
    pipeline,
)

import os

load_dotenv()

model_id = "meta-llama/Llama-2-13b-chat-hf"

device = f"cuda:{cuda.current_device()}" if cuda.is_available() else "cpu"

# begin initializing HF items, you need an access token
hf_auth = os.getenv("HF_TOKEN")
model_config = AutoConfig.from_pretrained(model_id, use_auth_token=hf_auth)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    config=model_config,
    device_map="auto",
    use_auth_token=hf_auth,
)

tokenizer = AutoTokenizer.from_pretrained(model_id, use_auth_token=hf_auth)

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
        task="text-generation",
        # we pass model parameters here too
        stopping_criteria=stopping_criteria,  # without this model rambles during chat
        temperature=0.1,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
        max_new_tokens=2048,  # max number of tokens to generate in the output
        repetition_penalty=1.1,  # without this output begins repeating
    )




def decode_output(pr):
    model_inputs = tokenizer(pr, return_tensors="pt").to("cuda:0")
    input_ids = model_inputs["input_ids"]
    output = model.generate(**model_inputs, temperature=0.1)
    return tokenizer.decode(output[0, input_ids.shape[1] :], skip_special_tokens=True)


if __name__ == "__main__":
    pass
