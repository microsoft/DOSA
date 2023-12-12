import os
from typing import Dict, List

import pandas as pd
from dotenv import load_dotenv
from langchain import HuggingFaceHub
from langchain.llms import HuggingFacePipeline
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from timeout_decorator import timeout

from const import STATE_CLUES_NOTES_DICT
from src.opensource.llama_backend import generate_text
from src.opensource.llama_frontend import chat_pipeline
from src.opensource.templates import (
    INST_FALCON_TEMPLATE,
    INST_LLAMA_TEMPLATE,
    SYS_FALCON_TEMPLATE,
    SYS_LLAMA_TEMPLATE,
)

load_dotenv()


# @timeout(60)  # Set a timeout of 60 seconds (adjust as needed)
def predict_guess(agent, inst_template):
    return agent.predict(human_input=inst_template)


def get_outputs(
    df: pd.DataFrame,
    conversation_buffer: ConversationBufferWindowMemory,
    inst_template: str,
    llm,
    sys_template: str,
) -> pd.DataFrame:
    df_eval = pd.DataFrame(columns=["guess1", "guess2", "ground_truth", "clues"])
    df = df[
        df["artifact"].notna()
    ]  # remove those instances for those we do not have the artifact name
    for i, row in df.iterrows():
        print(f"artifact--{i}---")
        clues = row["clues"].strip().split("\n")
        artifact = row["artifact"].lower().strip()
        output = ""
        for j, clue in enumerate(clues):
            output += f"CLUE-{j+1}: {clue.strip()}\n"
        fin_clues = output.strip()

        agent = chat_pipeline(
            llm=llm,
            clue_list=fin_clues,
            prompt_text=sys_template,
            conversation_buffer=conversation_buffer,
        )
        try:
            guess1 = predict_guess(agent, inst_template)
        except Exception as e:
            print(e)
            print(f"This example passed out: {artifact}, skipping")
            continue

        guess1 = (
            guess1.split(":")[1].strip().lower()
            if len(guess1.split(":")) > 1
            else guess1.strip()
        )
        if artifact in guess1:
            df_eval = df_eval.append(
                {
                    "guess1": guess1,
                    "guess2": "NA",
                    "ground_truth": artifact,
                    "clues": '\n'.join(clues),
                },
                ignore_index=True,
            )
            conversation_buffer.clear()
            continue
        else:
            try:
                guess2 = predict_guess(
                    agent,
                    inst_template="Your first guess is not correct. While making your second guess, please stick to the format as ANSWER: your_answer_here",
                )
            except TimeoutError:
                print(f"Timeout error for this, skipping")
                continue
            # guess2 = agent.predict(
            #     human_input="Your first guess is not correct. While making your second guess, please stick to the format as ANSWER: your_answer_here"
            # )
            guess2 = (
                guess2.split(":")[1].strip().lower()
                if len(guess2.split(":")) > 1
                else guess2.strip()
            )
            df_eval = df_eval.append(
                {
                    "guess1": guess1,
                    "guess2": guess2,
                    "ground_truth": artifact,
                    "clues": '\n'.join(clues),
                },
                ignore_index=True,
            )
        conversation_buffer.clear()
    return df_eval


def compile_results(
    STATE_CLUES_NOTES_DICT: Dict[str, List[str]],
    output_dir: str,
    conversation_buffer: ConversationBufferWindowMemory,
    inst_prompt: str,
    sys_template: str,
    llm: HuggingFacePipeline,
):
    for key, val in STATE_CLUES_NOTES_DICT.items():
        inst_template = inst_prompt.format(state=key)
        curr_path = os.path.join(output_dir, key)
        if not os.path.exists(curr_path):
            os.makedirs(curr_path)

        clue_path = val[0]
        notes_path = val[1] if len(val) > 1 else None

        #         print("Getting results for {key}ate")
        print(f"getting results for {key} state")
        conversation_buffer.clear()
        df_clues = pd.read_csv(clue_path)

        print(f"Running clues eval for {key} state")
        clues_result_path = os.path.join(curr_path, "eval_original_artifacts.csv")
        if not os.path.exists(clues_result_path):
            df_clues_eval = get_outputs(
                df_clues, conversation_buffer, inst_template, llm, sys_template
            )
            df_clues_eval.to_csv(clues_result_path, index=False)
        else:
            print(f"Clue eval results already exist for {key} state")

        if notes_path:
            conversation_buffer.clear()
            df_notes = pd.read_csv(notes_path)
            df_notes_eval = pd.DataFrame(
                columns=["guess1", "guess2", "ground_truth", "clues"]
            )
            notes_result_path = os.path.join(curr_path, "eval_expanded_artifacts.csv")
            if not os.path.exists(notes_result_path):
                print(f"Running notes eval for {key} state")
                df_notes_eval = get_outputs(
                    df_notes, conversation_buffer, inst_template, llm, sys_template
                )
                df_notes_eval.to_csv(notes_result_path, index=False)
            else:
                print(f"Notes eval results already exist for {key} state")


def main():
    conversation_buffer = ConversationBufferWindowMemory(k=2, memory_key="chat_history")
    inst_template = PromptTemplate.from_template(INST_FALCON_TEMPLATE)
    # llm = HuggingFacePipeline(pipeline=generate_text("meta-llama/Llama-2-13b-chat-hf"))
    llm = HuggingFacePipeline(pipeline=generate_text("tiiuae/falcon-7b-instruct"))
    # llm = HuggingFaceHub(
    #     huggingfacehub_api_token=os.environ["HF_TOKEN"],
    #     repo_id="tiiuae/falcon-7b-instruct",
    #     model_kwargs={"temperature": 0.1, "max_new_tokens": 500, "do_sample": False},
    # )
    compile_results(
        STATE_CLUES_NOTES_DICT=STATE_CLUES_NOTES_DICT,
        output_dir="/home/t-sahuja/cultural_artifacts/results/opensource/falcon_7b",
        conversation_buffer=conversation_buffer,
        inst_prompt=inst_template,
        sys_template=SYS_FALCON_TEMPLATE,
        llm=llm,
    )


if __name__ == "__main__":
    main()
