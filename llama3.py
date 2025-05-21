import streamlit as st
import json
import re
import ollama
import time
from sklearn.metrics import f1_score
from rouge import Rouge

# --------------------------------------
# Utility Functions
# --------------------------------------

# Text cleaning function
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)  # remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()  # remove extra spaces
    return text

# Load datasets
def load_icl_dataset(filename=r"C:\Users\rrk\OneDrive\Desktop\sem-end-projects\ML\datasets\examples.json"):
    with open(filename, "r") as file:
        return json.load(file)

def load_ft_dataset(path=r"C:\Users\rrk\OneDrive\Desktop\sem-end-projects\ML\datasets\finetuning_vs_icl.jsonl"):
    data = []
    with open(path, "r") as f:
        for line in f:
            data.append(json.loads(line))
    return data

def load_test_dataset(filename=r"C:\Users\rrk\OneDrive\Desktop\sem-end-projects\ML\datasets\test.json"):
    with open(filename, "r") as file:
        return json.load(file)

# Construct ICL or FT prompts
def construct_prompt(examples, query):
    prompt = "Use the following examples to help answer the final question.\n\n"
    for example in examples[:3]:  # use first 3 examples
        if "context" in example and "query" in example and "answer" in example:
            prompt += f"Context: {example['context']}\n"
            prompt += f"Q: {example['query']}\n"
            prompt += f"A: {example['answer']}\n\n"
        elif "instruction" in example and "output" in example:
            prompt += f"Instruction: {example['instruction']}\n"
            prompt += f"Response: {example['output']}\n\n"
    prompt += f"Q: {query}\nA:"
    return prompt

# Get model response
def get_model_response(model_name, prompt):
    start_time = time.time()
    response = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
    end_time = time.time()

    response_time = end_time - start_time
    model_response = response["message"]["content"]
    return model_response, response_time

# --------------------------------------
# Main Evaluation Function
# --------------------------------------

def evaluate_llama():
    st.title("🔍 LLaMA3.2 Evaluation - Automatic Q/A Metrics")

    technique_choice = st.selectbox("Choose Technique:", ["ICL", "Fine-Tuned"])

    # Load datasets
    icl_examples = load_icl_dataset()
    ft_examples = load_ft_dataset()
    test_examples = load_test_dataset()

    # Model selection
    if technique_choice == "ICL":
        examples = icl_examples
        model_name = "llama3.2:1b"
    else:
        examples = ft_examples
        model_name = "llama3.2-finetune"

    st.write("### Testing all queries from test dataset...")

    y_true_texts = []
    y_pred_texts = []
    response_times = []

    for test_example in test_examples:
        query = test_example["query"]

        # Construct prompt using examples
        prompt = construct_prompt(examples, query)

        # Get model response
        model_response, response_time = get_model_response(model_name, prompt)

        # Clean both
        cleaned_pred = clean_text(model_response)
        cleaned_true = clean_text(test_example["answer"])

        y_true_texts.append(cleaned_true)
        y_pred_texts.append(cleaned_pred)
        response_times.append(response_time)

        st.write(f"**Query:** {query}")
        st.write(f"**Ground Truth:** {cleaned_true}")
        st.write(f"**Model Prediction:** {cleaned_pred}")
        st.write(f"⏱️ **Response Time:** {response_time:.2f} seconds")
        st.write("---")

    # --------------------------------------
    # Evaluation
    # --------------------------------------

    st.subheader("📊 Evaluation Metrics")

    # 1. Token-level F1 Score
    def token_f1(y_true, y_pred):
        f1_scores = []
        for true_ans, pred_ans in zip(y_true, y_pred):
            true_tokens = true_ans.split()
            pred_tokens = pred_ans.split()

            common = set(true_tokens) & set(pred_tokens)
            if len(common) == 0:
                f1_scores.append(0)
            else:
                precision = len(common) / len(pred_tokens)
                recall = len(common) / len(true_tokens)
                f1 = 2 * (precision * recall) / (precision + recall)
                f1_scores.append(f1)
        return sum(f1_scores) / len(f1_scores)

    final_f1 = token_f1(y_true_texts, y_pred_texts)
    st.write(f"**Token-level F1 Score:** {final_f1:.4f}")

    # 2. ROUGE-L Score
    rouge = Rouge()
    scores = rouge.get_scores(y_pred_texts, y_true_texts, avg=True)
    rouge_l_f = scores["rouge-l"]["f"]
    st.write(f"**ROUGE-L F1 Score:** {rouge_l_f:.4f}")

    # 3. Average Response Time
    avg_response_time = sum(response_times) / len(response_times)
    st.write(f"**Average Response Time:** {avg_response_time:.2f} seconds")
