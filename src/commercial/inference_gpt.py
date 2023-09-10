import warnings
import openai
from typing import List, Dict, Union
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

CHAT_MODELS = [
    "gpt-35-turbo-deployment",
    "gpt4_deployment",
    "gptturbo",
    "gpt-4",
    "gpt-35-turbo",
    "gpt-4-32k",
    "gpt-35-tunro",
]



@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gpt3x_completion(prompt: str, model: str, **model_params):

    if model in CHAT_MODELS:
        openai.api_version = "2023-03-15-preview"
    else:
        openai.api_version = "2022-12-01"
    
    try:
        response = openai.Completion.create(
                    engine=model,
                    prompt=prompt,
                    max_tokens=model_params.get("max_tokens", 20),
                    temperature=model_params.get("temperature", 1),
                    top_p=model_params.get("top_p", 1),
                )
    except (openai.error.APIConnectionError, openai.error.RateLimitError) as e:
        warnings.warn(
                "Couldn't generate response, returning empty string as response"
            )
        return ""

    output = response["choices"][0]["text"].strip().split("\n")[0]
    return output 
