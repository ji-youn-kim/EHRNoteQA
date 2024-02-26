import os, sys
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import fire, time
from pathlib import Path
from utils import get_prompt
sys.path.append(str(Path(__file__).resolve().parent.parent))

def main(
	ckpt_dir: str, # "Folder path to target model for evaluation. You may put an empty string when evaluating gpt series models."
	model_name: str, # "Name of target model for evaluation."
	input_path: str, # "Folder path to the processed EHRNoteQA data."
	file_name: str, # "Name of the processed EHRNoteQA file."
	save_path: str, # "Folder path to save target model generated output. "
):
	
	if "gpt" in model_name:
		from gpt.gpt_setup import generate_prompt, make_answer_gpt
		
	else:
		tokenizer = AutoTokenizer.from_pretrained(
			os.path.join(ckpt_dir, model_name),
			cache_dir=os.path.join(ckpt_dir, model_name),
			trust_remote_code=True,
			local_files_only=True
		)

		if "A6000" in torch.cuda.get_device_name():
			max_memory = {i: "48GiB" for i in range(torch.cuda.device_count())}
		elif "3090" in torch.cuda.get_device_name():
			max_memory = {i: "24GiB" for i in range(torch.cuda.device_count())}

		model = AutoModelForCausalLM.from_pretrained(
			os.path.join(ckpt_dir, model_name),
			cache_dir=os.path.join(ckpt_dir, model_name),
			local_files_only=True,
			device_map="auto",
			trust_remote_code=True,
			torch_dtype=torch.bfloat16,
			max_memory=max_memory
		)

	data = pd.read_json(os.path.join(input_path, file_name), lines=True)

	if model_name not in data:
		data[model_name] = None

	count = 0
	for idx, row in data.iterrows(): 
		start_time = time.time()
		
		num_notes = int(row['num_notes'])
		note = ""
		
		for i in range(num_notes):
			note = note + f"[note {i+1} start]\n" + row[f"note_{i+1}"] + f"\n[note {i+1} end]"
			if i < num_notes -1:
				note = note + "\n\n"
    
		sample = {"note": note, "question": row["question"], "choice_a": row["choice_A"], "choice_b": row["choice_B"],
                    "choice_c": row["choice_C"], "choice_d": row["choice_D"], "choice_e": row["choice_E"]}
	
		text = get_prompt(model_name).format_map(sample)

		if "gpt" in model_name:
			message = generate_prompt(text)
			result = make_answer_gpt(message, model_name, 15)
		else:
			tokens = tokenizer.encode(text, return_tensors="pt").to("cuda")

			output = model.generate(
				tokens,
				max_new_tokens=600,
				temperature=0,
				do_sample=False,
				eos_token_id=tokenizer.eos_token_id,
				use_cache=True
			)
		
			result = tokenizer.decode(output[0][tokens.size(1):], skip_special_tokens=True).strip()

		print(f"{count+1}/{len(data)}")
		print(sample["question"])
		print(result)
		print("--- %s seconds ---" % round(time.time() - start_time, 1))
		count +=1

		data.at[idx, model_name] = result
		data.to_csv(os.path.join(save_path, f'ours_{model_name}_{file_name.split(".")[0]}.csv'), index=False)


if __name__ == "__main__":
	fire.Fire(main)
