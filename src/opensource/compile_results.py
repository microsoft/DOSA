from utils import get_clues, generate_abs_path
from src.opensource.llama_frontend import chat_pipeline
from src.opensource.llama_backend import generate_text
import pandas as pd
import os
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.llms import HuggingFacePipeline
from src.opensource.templates import (
    SYS_FALCON_TEMPLATE,
    INST_FALCON_TEMPLATE,
    SYS_LLAMA_TEMPLATE,
    INST_LLAMA_TEMPLATE,
)
from const import STATE_CLUES_NOTES_DICT


def get_outputs(
    df: pd.DataFrame,
    conversation_buffer,
    inst_template: str,
    llm,
    sys_template: str,
) -> pd.DataFrame:
    df_eval = pd.DataFrame(columns=["guess1", "guess2", "ground_truth", "clues"])
    df = df[df['artifact'].notna()] # remove those instances for those we do not have the artifact name
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
        guess1 = agent.predict(human_input=inst_template)
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
                    "clues": row["clues"].strip(),
                },
                ignore_index=True,
            )
            conversation_buffer.clear()
            continue
        else:
            guess2 = agent.predict(
                human_input="Your first guess is not correct. While making your second guess, please stick to the format as ANSWER: your_answer_here"
            )
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
                    "clues": row["clues"].strip(),
                },
                ignore_index=True,
            )
        conversation_buffer.clear()
    return df_eval


def compile_results(
    STATE_CLUES_NOTES_DICT,
    output_dir,
    conversation_buffer,
    inst_template,
    sys_template,
    llm,
):
    for key, val in STATE_CLUES_NOTES_DICT.items():
        inst_template = inst_template.format(state=key)
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
        clues_result_path = os.path.join(curr_path, "eval_clues.csv")
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
            notes_result_path = os.path.join(curr_path, "eval_notes.csv")
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
    llm = HuggingFacePipeline(pipeline=generate_text("ichitaka/falcon-40b-instruct-8bit"))
    compile_results(
        STATE_CLUES_NOTES_DICT=STATE_CLUES_NOTES_DICT,
        output_dir="/home/t-sahuja/cultural_artifacts/results/opensource/falcon",
        conversation_buffer=conversation_buffer,
        inst_template=inst_template,
        sys_template=SYS_FALCON_TEMPLATE,
        llm=llm,
    )


if __name__ == "__main__":
    main()
