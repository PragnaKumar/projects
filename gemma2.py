import streamlit as st
import json
import re
import ollama
import time
from rouge import Rouge

# -- common functions --
# (copy these into mistral file)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@st.cache_data
def load_json_file(path):
    with open(path, "r") as file:
        return json.load(file)

def construct_prompt(examples, query):
    prompt = "Use the following examples to help answer the final question.\n\n"
    for example in examples[:3]:
        prompt += f"Context: {example['context']}\nQ: {example['query']}\nA: {example['answer']}\n\n"
    prompt += f"Q: {query}\nA:"
    return prompt

def get_model_response(model_name, prompt):
    start_time = time.time()
    response = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
    end_time = time.time()
    model_response = response["message"]["content"]
    return model_response, (end_time - start_time)

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

# -- evaluation function --

def evaluate_gemma():
    st.title("🔍 Gemma Evaluation - Automatic Q/A Metrics")
    technique_choice = st.selectbox("Choose Technique:", ["ICL", "Fine-Tuned"])

    icl_examples = load_json_file(r"C:\Users\rrk\OneDrive\Desktop\sem-end-projects\ML\datasets\examples.json")
    test_examples = load_json_file(r"C:\Users\rrk\OneDrive\Desktop\sem-end-projects\ML\datasets\test.json")

    st.write("### Testing queries from test dataset...")

    y_true_texts = []
    y_pred_texts = []
    response_times = []

    for test_example in test_examples:
        query = test_example["query"]

        if technique_choice == "ICL":
            examples = icl_examples
            prompt = construct_prompt(examples, query)
            model_name = "gemma2:2b"
        else:
            prompt = query
            model_name = "gemma-finetune"

        model_response, response_time = get_model_response(model_name, prompt)

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

    st.subheader("📊 Evaluation Metrics")

    final_f1 = token_f1(y_true_texts, y_pred_texts)
    st.write(f"**Token-level F1 Score:** {final_f1:.4f}")

    rouge = Rouge()
    scores = rouge.get_scores(y_pred_texts, y_true_texts, avg=True)
    rouge_l_f = scores["rouge-l"]["f"]
    st.write(f"**ROUGE-L F1 Score:** {rouge_l_f:.4f}")

    avg_response_time = sum(response_times) / len(response_times)
    st.write(f"**Average Response Time:** {avg_response_time:.2f} seconds")

