# EHRNoteQA: An LLM Benchmark for Real-World Clinical Practice Using Discharge Summaries
## Overview
Discharge summaries in Electronic Health Records (EHRs) are crucial for clinical decision-making, but their length and complexity make information extraction challenging, especially when dealing with accumulated summaries across multiple patient admissions.
Large Language Models (LLMs) show promise in addressing this challenge by efficiently analyzing vast and complex data.
Existing benchmarks, however, fall short in properly evaluating LLMs' capabilities in this context, as they typically focus on single-note information or limited topics, failing to reflect the real-world inquiries required by clinicians.
To bridge this gap, we introduce EHRNoteQA, a novel benchmark built on the MIMIC-IV EHR, comprising 962 different QA pairs each linked to distinct patients' discharge summaries.
Every QA pair is initially generated using GPT-4 and then manually reviewed and refined by three clinicians to ensure clinical relevance.
EHRNoteQA includes questions that require information across multiple discharge summaries and covers eight diverse topics, mirroring the complexity and diversity of real clinical inquiries.
We offer EHRNoteQA in two formats: open-ended and multi-choice question answering, and propose a reliable evaluation method for each.
We evaluate 27 LLMs using EHRNoteQA and examine various factors affecting the model performance (*e.g., the length and number of discharge summaries*).
Furthermore, to validate EHRNoteQA as a reliable proxy for expert evaluations in clinical practice, we measure the correlation between the LLM performance on EHRNoteQA, and the LLM performance manually evaluated by clinicians.
Results show that LLM performance on EHRNoteQA have higher correlation with clinician-evaluated performance (Spearman: 0.78, Kendall: 0.62) compared to other benchmarks, demonstrating its practical relevance in evaluating LLMs in clinical settings.
EHRNoteQA will be publicly available to support further research and improve LLM evaluation in clinical practice.
- Paper link: [EHRNoteQA: An LLM Benchmark for Real-World Clinical Practice Using Discharge Summaries](https://arxiv.org/pdf/2402.16040.pdf)

## Requirements
```
# Create the conda environment
conda create -y -n EHRNoteQA python=3.10.4

# Activate the environment
source activate EHRNoteQA

# Install required packages
conda install -y pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch

pip install pandas==1.4.3 \
            openai==1.12.0 \
            transformers==4.31.0 \
            accelerate==0.21.0 \
            tqdm==4.65.0 \
            fire==0.5.0
```

## Dataset
The EHRNoteQA dataset is accessible on Physionet with your Physionet credentials. \
To get started, download the following:
1. The [EHRNoteQA dataset](https://doi.org/10.13026/acga-ht95).
2. The discharge.csv.gz file from [MIMIC-IV-Note v2.2](https://physionet.org/content/mimic-iv-note/2.2/).
<p align="center">
  <img src="https://github.com/ji-youn-kim/EHRNoteQA/blob/master/resources/figure1.png?raw=true" width="600"/>
  <br>
  <div align="center">Overview of EHRNoteQA Data Construction Process</div>
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
--eval_method [Evaluation Method - choose from 'openended', 'multichoice'] \
--input_path [Folder path to the processed EHRNoteQA data] \
--file_name EHRNoteQA_processed.jsonl \
--save_path [Folder path to save target model generated output]

# Using GPT
python ../src/generation/generate.py \
--ckpt_dir "" \
--model_name gpt-4-1106-preview \
--eval_method [Evaluation Method - choose from 'openended', 'multichoice'] \
--input_path [Folder path to the processed EHRNoteQA data] \
--file_name EHRNoteQA_processed.jsonl \
--save_path [Folder path to save target model generated output]
```
Adjust the model and file names according to the target evaluation model and the processed EHRNoteQA file.

## Model Evaluation
Set the environment variables as previously described if not already done.\
You must use HIPAA-compliant platforms such as Azure.
```
export AZURE_OPENAI_ENDPOINT=[Your Endpoint]
export AZURE_OPENAI_KEY=[Your Key]
export AZURE_API_VERSION=[Your API Version]
```
Use the following script to evaluate the model outputs generated from the EHRNoteQA dataset. (located in scripts/evaluate.sh)
```
python ../src/evaluation/evaluate.py \
--gpt_type gpt-4-1106-preview \
--model_name Llama-2-7b-chat-hf \
--eval_method [Evaluation Method - choose from 'openended', 'multichoice'] \
--input_path [Folder path to target model generated output] \
--file_name ours_Llama-2-7b-chat-hf_EHRNoteQA_processed.csv \
--save_path [Folder path to save GPT evaluated result of target model output]
```
Adjust the names for the GPT model used for evaluation (gpt type), the model whose output to be evaluated (model name), and the generated model output file (file name).

## Citation
```
@misc{kweon2024ehrnoteqa,
      title={EHRNoteQA: An LLM Benchmark for Real-World Clinical Practice Using Discharge Summaries}, 
      author={Sunjun Kweon and Jiyoun Kim and Heeyoung Kwak and Dongchul Cha and Hangyul Yoon and Kwanghyun Kim and Jeewon Yang and Seunghyun Won and Edward Choi},
      year={2024},
      eprint={2402.16040},
      archivePrefix={arXiv},
      primaryClass={id='cs.CL' full_name='Computation and Language' is_active=True alt_name='cmp-lg' in_archive='cs' is_general=False description='Covers natural language processing. Roughly includes material in ACM Subject Class I.2.7. Note that work on artificial languages (programming languages, logics, formal systems) that does not explicitly address natural-language issues broadly construed (natural-language processing, computational linguistics, speech, text retrieval, etc.) is not appropriate for this area.'}
}
```

## Code References
https://github.com/lm-sys/FastChat


