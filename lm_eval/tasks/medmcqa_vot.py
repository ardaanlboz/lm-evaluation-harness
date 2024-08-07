from lm_eval.base import MultipleChoiceTask

"""
CoT Prompts are implemented from the "Gemini Goes to Med School: Exploring the Capabilities of Multimodal Large Language Models on Medical Challenge Problems & Hallucinations": https://arxiv.org/pdf/2402.07023.pdf
"""

class medmcqa_vot(MultipleChoiceTask):
    VERSION = 0
    DATASET_PATH = "augtoma/medmcqa"
    DATASET_NAME = None

    def has_training_docs(self):
        return True

    def has_validation_docs(self):
        return False

    def has_test_docs(self):
        return True

    def training_docs(self):
        return map(self._process_doc, self.dataset["train"])

    def validation_docs(self):
        return []

    def test_docs(self):
        return map(self._process_doc, self.dataset["test"])

    def _process_doc(self, doc):
        return {
            "query": doc["question"] + "\n" + \
                    "".join([f" ({k}) {v}" if i else f"({k}) {v}" \
                    for i, (k, v) in enumerate(doc["options"].items())]),
            "choices": list(doc["options"].values()),
            "gold": ord(doc["answer_idx"])-ord("A"),
        }

    def doc_to_text(self, doc):
        options = doc['choices']
        formatted_options = '\n'.join([f"{chr(65+i)}. {option}" for i, option in enumerate(options)])

        return f"The following is a multiple choice question about medical knowledge. Verify the accuracy of the provided answer by comparing it against the given options and summarizing the reasoning step-by-step after creating premises.\nUse deductive verification to ensure each step is logically valid, based on the premises.\nOutput the verified option from the four options as the final answer.\n{doc['query']}\nOptions:\n{formatted_options}\nAnswer:"