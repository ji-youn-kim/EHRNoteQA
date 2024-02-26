# Local Model
CUDA_VISIBLE_DEVICES=0 python ../generate.py \
--ckpt_dir [Folder path to target model for evaluation] \
--model_name Llama-2-7b-chat-hf \
--input_path [Folder path to the processed EHRNoteQA data] \
--file_name EHRNoteQA_processed.jsonl \
--save_path [Folder path to save target model generated output]

# GPT
python ../generate.py \
--ckpt_dir "" \
--model_name gpt-4-1106-preview \
--input_path [Folder path to the processed EHRNoteQA data] \
--file_name EHRNoteQA_processed.jsonl \
--save_path [Folder path to save target model generated output]