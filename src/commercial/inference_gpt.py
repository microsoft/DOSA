import warnings
import openai
from dotenv import load_dotenv
from utils import load_openai_env_variables
# from tenacity import (
#     retry,
#     stop_after_attempt,
#     wait_random_exponential,
# )  # for exponential backoff

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
def gpt3x_completion(sys_prompt: str,inst_prompt, model: str, **model_params):
    
    try:
        response = openai.ChatCompletion.create(
                    engine=model,
                    messages = [
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": inst_prompt}
                    ],
                    temperature=model_params.get("temperature", 0),
                )
    except (openai.error.APIConnectionError, openai.error.RateLimitError) as e:
        warnings.warn(
                "Couldn't generate response, returning empty string as response"
            )
        return ""
    output = response["choices"][0]["message"]["content"].strip()
    return output 


if __name__ == "__main__":
    output = gpt3x_completion("you are an experienced travel agent.", "give me an itinerary for a trip to iceland for 10 days", "gpt-4")
    print(output)
