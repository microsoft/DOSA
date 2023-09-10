from dotenv import load_dotenv
import os
import google.generativeai as palm

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

load_dotenv()


palm.configure(api_key=os.getenv('PALM_API_TOKEN'))

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def palm_completion(sys_prompt):
    response = palm.chat(context=sys_prompt, temperature=0.1)
    return response

