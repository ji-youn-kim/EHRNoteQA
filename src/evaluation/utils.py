PROMPT_DICT = {
		"gpt": (
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


def get_prompt(model_name):
	print(model_name)
	return PROMPT_DICT["gpt"]