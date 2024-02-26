PROMPT_DICT = {
	"generate": {
			"gpt": (
				"Discharge Summary :\n"
				"{note}\n\n"
				"Question : {question}\n"
				"Choices :\n"
				"A. {choice_a}\n"
				"B. {choice_b}\n"
				"C. {choice_c}\n"
				"D. {choice_d}\n"
				"E. {choice_e}\n\n"
				"Answer :"
			),
			"llama-2-chat": (
				"[INST] <<SYS>>\n"
				"You are a helpful, respectful and honest assistant.\n"
				"<</SYS>>\n\n"
				"Discharge Summary :\n"
				"{note}\n\n"
				"Question : {question}\n"
				"Choices :\n"
				"A. {choice_a}\n"
				"B. {choice_b}\n"
				"C. {choice_c}\n"
				"D. {choice_d}\n"
				"E. {choice_e}\n\n"
				"Answer : "
				"[/INST]"
			),
		},
	"evaluate": {
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

	}


def get_prompt(model_name, type):
	print(model_name)
	if "gpt" in model_name:
		return PROMPT_DICT[type]["gpt"]
	elif model_name in ["Llama-2-70b-chat-hf", "Llama-2-13b-chat-hf", "Llama-2-7b-chat-hf"]:
		return PROMPT_DICT[type]["llama-2-chat"]
