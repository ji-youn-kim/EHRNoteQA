python ../src/evaluation/evaluate.py \
--gpt_type gpt-4-1106-preview \
--model_name Llama-2-7b-chat-hf \
--eval_method [Evaluation Method - choose from 'openended', 'multichoice'] \
--input_path [Folder path to target model generated output] \
--file_name ours_openended_Llama-2-7b-chat-hf_EHRNoteQA_processed.csv \
--save_path [Folder path to save GPT evaluated result of target model output]