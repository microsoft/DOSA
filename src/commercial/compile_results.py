import os
from typing import Dict, List

import pandas as pd
from dotenv import load_dotenv
from langchain import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from timeout_decorator import timeout

from const import STATE_CLUES_NOTES_DICT

from src.commercial.inference_gpt import gpt_chat_pipeline
from src.commercial.templates import SYS_GPT_TEMPLATE, INST_GPT_TEMPLATE
import warnings

warnings.filterwarnings("ignore")

load_dotenv()


def predict_guess(agent, inst_template):
    return agent.predict(input=inst_template)


def get_outputs(
    df: pd.DataFrame,
    conversation_buffer: ConversationBufferMemory,
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

        agent = gpt_chat_pipeline(
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
    conversation_buffer: ConversationBufferMemory,
    inst_prompt: PromptTemplate,
    sys_prompt: str,
    llm: AzureChatOpenAI,
):
    for state_name, val in STATE_CLUES_NOTES_DICT.items():
        inst_template = inst_prompt.format(state=state_name)
        curr_path = os.path.join(output_dir, state_name)
        if not os.path.exists(curr_path):
            os.makedirs(curr_path)
        clue_path = val[0]
        notes_path = val[1] if len(val) > 1 else None

        #         print("Getting results for {key}ate")
        print(f"getting results for {state_name} state")
        conversation_buffer.clear()
        df_clues = pd.read_csv(clue_path)

        print(f"Running clues eval for {state_name} state")
        clues_result_path = os.path.join(curr_path, "eval_clues.csv")
        if not os.path.exists(clues_result_path):
            df_clues_eval = get_outputs(
                df_clues, conversation_buffer, inst_template, llm, sys_prompt
            )
            df_clues_eval.to_csv(clues_result_path, index=False)
        else:
            print(f"Clue eval results already exist for {state_name} state")

        if notes_path:
            conversation_buffer.clear()
            df_notes = pd.read_csv(notes_path)
            df_notes_eval = pd.DataFrame(
                columns=["guess1", "guess2", "ground_truth", "clues"]
            )
            notes_result_path = os.path.join(curr_path, "eval_notes.csv")
            if not os.path.exists(notes_result_path):
                print(f"Running notes eval for {state_name} state")
                df_notes_eval = get_outputs(
                    df_notes, conversation_buffer, inst_template, llm, sys_prompt
                )
                df_notes_eval.to_csv(notes_result_path, index=False)
            else:
                print(f"Notes eval results already exist for {state_name} state")


def main():
    conversation_buffer = ConversationBufferMemory(
        ai_prefix="Agent", memory_key="chat_history"
    )
    inst_template = PromptTemplate(
        input_variables=["state"], template=INST_GPT_TEMPLATE
    )

    model_name = "gpt-4"
    llm = AzureChatOpenAI(
        model=model_name,
        openai_api_key=os.environ["OPENAI_API_KEY"],
        openai_api_base=os.environ["OPENAI_END_POINT"],
        openai_api_type=os.environ["OPENAI_API_TYPE"],
        openai_api_version=os.environ["OPENAI_API_VERSION"],
        deployment_name=model_name,
        temperature=0,
    )
    # llm = HuggingFacePipeline(pipeline=generate_text("tiiuae/falcon-7b-instruct"))
    # llm = HuggingFaceHub(
    #     huggingfacehub_api_token=os.environ["HF_TOKEN"],
    #     repo_id="tiiuae/falcon-7b-instruct",
    #     model_kwargs={"temperature": 0.1, "max_new_tokens": 500},
    # )
    compile_results(
        STATE_CLUES_NOTES_DICT=STATE_CLUES_NOTES_DICT,
        output_dir="/home/t-sahuja/cultural_artifacts/results/commercial/gpt_4",
        conversation_buffer=conversation_buffer,
        inst_prompt=inst_template,
        sys_prompt=SYS_GPT_TEMPLATE,
        llm=llm,
    )


if __name__ == "__main__":
    main()
