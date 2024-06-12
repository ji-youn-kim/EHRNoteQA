import os, sys
import pandas as pd
from tqdm import tqdm
import fire, time
from pathlib import Path
from utils import get_prompt
sys.path.append(str(Path(__file__).resolve().parent.parent))


def main(
    gpt_type: str, # "GPT model type to evaluate a target model output."
    model_name: str, # "Name of target model to evaluate."
    eval_method: str, # "Evaluation method (open_ended or multi_choice)"
    input_path: str, # "Folder path to target model generated output in which to evaluate."
    file_name: str, # "File name of target model generated output in which to evaluate."
    save_path: str, # "Folder path to save GPT evaluated result of target model output."
):
    
    from gpt.gpt_setup import generate_prompt, make_answer_gpt
    
    df = pd.read_csv(os.path.join(input_path, file_name))
    eval_col = f"{model_name}_gpt4_eval"
    df[eval_col] = None

    for index, row in tqdm(df.iterrows()):

        output = row[model_name]

        if eval_method == "openended":
            question, num_notes = row["question"], int(row["num_notes"])
            answer = row[f"choice_{row['answer']}"]
            note = ""
            for i in range(num_notes):
                note = note + f"[note {i+1} start]\n" + row[f"note_{i+1}"] + f"\n[note {i+1} end]"
                if i < num_notes -1:
                    note = note + "\n\n"
            sample = {"question": question, "note": note, "correct_answer": answer, "output": output}
        elif eval_method == "multichoice":
            choices = f"A. {row['choice_A']}\nB. {row['choice_B']}\nC. {row['choice_C']}\nD. {row['choice_D']}\nE. {row['choice_E']}"
            answer_letter = row["answer"]
            answer = answer_letter + ". " + row[f"choice_{answer_letter}"]
            sample = {"output": output, "choices": choices, "answer": answer}

        text = get_prompt(eval_method).format_map(sample)

        message = generate_prompt(text)
        result = make_answer_gpt(message, gpt_type, 15).strip()
        
        print(f"{index}/{len(df)}")
        print(result)
        print("================")
        print(output)
        print("================")
        print(answer)

        df.at[index, eval_col] = result
        df.to_csv(os.path.join(save_path, file_name), index=False)
        time.sleep(0.15)


if __name__ == "__main__":
	fire.Fire(main)
    