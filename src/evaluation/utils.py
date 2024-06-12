PROMPT_DICT = {
	"openended" : (
		"Your task is to evaluate the provided model output in response to a specific question associated with the given discharge summaries. "
		"By using the correct answer also provided, you must score the answer as 0 or 1, based on the following scoring instructions.\n"
		"Scoring Instructions:\n"
		"1. Assign 1 point if the answer is correct.\n"
		"2. Assign 0 points if the answer is either incorrect, or if it falsely claims there is no answer when one exists according to the discharge summaries.\n\n"
		"- Discharge Summaries:\n{note}\n\n"
		"- Question: {question}\n\n"
		"- Correct Answer: {correct_answer}\n\n"
		"- Model Output:\n\n"
		"{output}\n\n"
		"Output format:\n"
		"Score: {{score}}\n"
		"Reasoning: {{explanation}}\n"
		"(Note: In your response please replace {{score}} with the numerical score of 0 or 1, and provide a brief reasoning for the assigned score based on the evaluation criteria.)"
	),
	"multichoice": (
		"Your task is to evaluate the provided model output by determining whether it matches the correct answer from the multiple-choice options provided. "
		"The model output is correct and should be met with a \"yes\" if it accurately reflects the content of the correct answer choice, not necessarily its exact wording. "
		"If the content of the model output aligns with the correct answer choice, despite any additional details or varied phrasing, you are to respond \"yes\". "
		"Should the model output diverge in meaning or substance from the correct answer—whether by selecting an alternative choice or providing a response not aligning with any provided options—a response of \"no\" is necessary.\n\n"
		"Model Output:\n"
		"{output}\n\n"
		"Answer Choices:\n"
		"{choices}\n\n"
		"Correct Answer:\n"
		"{answer}\n\n"
		"With the given information, do you conclude that the model output substantively matches the correct answer provided? "
		"Respond solely with \"yes\" or \"no\"."
	)
}


def get_prompt(eval_method):
	print(eval_method)
	return PROMPT_DICT[eval_method]