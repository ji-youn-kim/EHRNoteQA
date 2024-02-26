import os
import pandas as pd
import re
import fire


def transform_string(s):
    s = re.sub(r'(\n\s*|\s*\n)', '\n', s)
    s = re.sub(r'\s{2,}', ' ', s)
    s = s.strip()
    return s


def main(
    ehrnoteqa: str, # "Folder path containing 'EHRNoteQA.jsonl' file."
    mimiciv: str, # "Folder path containing 'discharge.csv.gz' file from MIMIC-IV database."
    output: str, # "Folder path to save the preprocessed EHRNoteQA dataset."
):

    if not os.path.exists(os.path.join(ehrnoteqa,"EHRNoteQA.jsonl")):
        raise FileNotFoundError(f"Folder {ehrnoteqa} does not have 'EHRNoteQA.jsonl' file.")
    
    if not os.path.exists(os.path.join(mimiciv,"discharge.csv.gz")):
        raise FileNotFoundError(f"Folder {mimiciv} does not have 'discharge.csv.gz' file.")

    print("Reading MIMIC-IV discharge summaries...")

    ehrnoteqa = pd.read_json(os.path.join(ehrnoteqa,"EHRNoteQA.jsonl"), lines = True)
    mimiciv = pd.read_csv(os.path.join(mimiciv,"discharge.csv.gz"), compression = "gzip")

    mimiciv_filtered = mimiciv[mimiciv["subject_id"].isin(ehrnoteqa["patient_id"].values)]
    mimiciv_filtered.sort_values(by='charttime', ascending=True, inplace=True)

    print("Done...")

    print("Processing MIMIC-IV discharge summary: Removing excessive white spaces and Adding Meta Information to the note...")


    mimiciv_filtered["new_text"] = mimiciv_filtered["text"].apply(lambda x : transform_string(x))
    mimiciv_filtered['new_text'] = "Patient ID : " + mimiciv_filtered['subject_id'].astype(str) + \
                "\nAdmission ID : " + mimiciv_filtered['hadm_id'].astype(str) + \
                "\nChartdate : " + mimiciv_filtered['charttime'].str[:10] + \
                "\n" + mimiciv_filtered['new_text']
    
    print("Done...")

    print("Adding discharge summary to 'EHRNoteQA.jsonl'...")

    for row in ehrnoteqa.iterrows():
        id = row[1]["patient_id"]
        tmp = mimiciv_filtered[mimiciv_filtered["subject_id"]==id]

        try:
            ehrnoteqa.loc[row[0],"note_1"] = tmp["new_text"].values[0]
        except:
            ehrnoteqa.loc[row[0],"note_1"] = ""

        try:
            ehrnoteqa.loc[row[0],"note_2"] = tmp["new_text"].values[1]
        except:
            ehrnoteqa.loc[row[0],"note_2"] = ""

        try:
            ehrnoteqa.loc[row[0],"note_3"] = tmp["new_text"].values[2]
        except:
            ehrnoteqa.loc[row[0],"note_3"] = ""

    print("Done...")

    print("Saving processed 'EHRNoteQA.jsonl...")

    ehrnoteqa.to_json(os.path.join(os.path.join(output,"EHRNoteQA_processed.jsonl")), orient='records', lines=True)

    print("Done...")


if __name__ =="__main__":
    fire.Fire(main)