# EHRNoteQA: A Patient-Specific Question Answering Benchmark for Evaluating Large Language Models in Clinical Settings

<div align="center">
  <img src="https://github.com/ji-youn-kim/EHRNoteQA/blob/master/resources/figure1.png?raw=true" width="400">
</div>

## Dataset
The EHRNoteQA dataset will soon be accessible on Physionet. We will update this space with a direct link once it's available. \
Download the (1) EHRNoteQA dataset, along with the (2) discharge.csv.gz file from [MIMIC-IV-Note v2.2](https://physionet.org/content/mimic-iv-note/2.2/).
<div align="center">
  <img src="https://github.com/ji-youn-kim/EHRNoteQA/blob/master/resources/figure2.png?raw=true" width="800">
  <br>
  <p>Overview of EHRNoteQA Data Generation Pipeline</p>
</div>

## Preparing the Data
You may preprocess the inputs as below. (located in run/preprocess.sh)
```
python ../preprocess.py \
--ehrnoteqa [Folder path containing 'EHRNoteQA.jsonl' file] \
--mimiciv [Folder path containing 'discharge.csv.gz' file from MIMIC-IV database] \
--output [Folder path to save the preprocessed EHRNoteQA dataset]
```
The code links the corresponding MIMIC-IV notes to the EHRNoteQA dataset, and preprocesses the MIMIC-IV notes by removing unnecessary whitespace and adding relevant metadata.

## Generating Model Outputs
You may generate the model output of our EHRNoteQA dataset as below. (located in run/generate.sh)
```
# Using Local Model
CUDA_VISIBLE_DEVICES=0 python ../generate.py \
--ckpt_dir [Folder path to target model for evaluation] \
--model_name Llama-2-7b-chat-hf \
--input_path [Folder path to the processed EHRNoteQA data] \
--file_name EHRNoteQA_processed.jsonl \
--save_path [Folder path to save target model generated output]

# Using GPT
python ../generate.py \
--ckpt_dir "" \
--model_name gpt-4-1106-preview \
--input_path [Folder path to the processed EHRNoteQA data] \
--file_name EHRNoteQA_processed.jsonl \
--save_path [Folder path to save target model generated output]
```
Adjust the model and file names according to the target evaluation model and the processed EHRNoteQA file.

## Model Evaluation
Evaluate the model outputs generated from our EHRNoteQA dataset using GPT-series-models as below. (located in run/evaluate.sh)
```
python ../evaluate.py \
--gpt_type gpt-4-1106-preview \
--model_name Llama-2-7b-chat-hf \
--input_path [Folder path to target model generated output] \
--file_name ours_Llama-2-7b-chat-hf_EHRNoteQA_processed.csv \
--save_path [Folder path to save GPT evaluated result of target model output]
```
Adjust the names for the GPT model used for evaluation (gpt type), the model whose output to be evaluated (model name), and the generated model output file (file name).

## Citation
```
This section will be updated upon acceptance.
```
