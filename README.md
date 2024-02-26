# EHRNoteQA: A Patient-Specific Question Answering Benchmark for Evaluating Large Language Models in Clinical Settings

<p align="center">
  <img src="https://github.com/ji-youn-kim/EHRNoteQA/blob/master/resources/figure1.png?raw=true" width="400"/>
</p>

## Dataset
The EHRNoteQA dataset will soon be accessible on Physionet. We will update this space with a direct link once it is available. \
To get started, download the following:
1. The EHRNoteQA dataset.
2. The discharge.csv.gz file from [MIMIC-IV-Note v2.2](https://physionet.org/content/mimic-iv-note/2.2/).
<p align="center">
  <img src="https://github.com/ji-youn-kim/EHRNoteQA/blob/master/resources/figure2.png?raw=true" width="100%" height="auto">
  <br>
  <div align="center">Overview of EHRNoteQA Data Generation Pipeline</div>
</p>

## Preparing the Data
You may preprocess the inputs as below. (located in scripts/preprocess.sh)
```
python ../src/preprocessing/preprocess.py \
--ehrnoteqa [Folder path containing 'EHRNoteQA.jsonl' file] \
--mimiciv [Folder path containing 'discharge.csv.gz' file from MIMIC-IV database] \
--output [Folder path to save the preprocessed EHRNoteQA dataset]
```
This script will link MIMIC-IV notes with the EHRNoteQA dataset and preprocess the MIMIC-IV notes by removing unnecessary whitespace and adding relevant metadata.

## Generating Model Outputs
If you are generating outputs using GPT, set the environment variables as below.\
You must use HIPAA-compliant platforms such as Azure.
```
export AZURE_OPENAI_ENDPOINT=[Your Endpoint]
export AZURE_OPENAI_KEY=[Your Key]
export AZURE_API_VERSION=[Your API Version]
```

You may generate model outputs of the EHRNoteQA dataset as below. (located in scripts/generate.sh)
```
# Using Local Model
CUDA_VISIBLE_DEVICES=0 python ../src/generation/generate.py \
--ckpt_dir [Folder path to target model for evaluation] \
--model_name Llama-2-7b-chat-hf \
--input_path [Folder path to the processed EHRNoteQA data] \
--file_name EHRNoteQA_processed.jsonl \
--save_path [Folder path to save target model generated output]

# Using GPT
python ../src/generation/generate.py \
--ckpt_dir "" \
--model_name gpt-4-1106-preview \
--input_path [Folder path to the processed EHRNoteQA data] \
--file_name EHRNoteQA_processed.jsonl \
--save_path [Folder path to save target model generated output]
```
Adjust the model and file names according to the target evaluation model and the processed EHRNoteQA file.

## Model Evaluation
Set the environment variables as previously described if not already done.\
You must use HIPAA-compliant platforms such as Azure.
```
export AZURE_OPENAI_ENDPOINT=[Your Azure Openai Endpoint]
export AZURE_OPENAI_KEY=[Your Azure Openai Key]
export AZURE_API_VERSION=[Youre Azure API Version]
```
Evaluate the model outputs generated from our EHRNoteQA dataset using GPT as below. (located in scripts/evaluate.sh)
```
python ../src/evaluation/evaluate.py \
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

## Code References
https://github.com/lm-sys/FastChat


