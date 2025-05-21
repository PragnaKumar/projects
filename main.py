import streamlit as st
from llama3 import evaluate_llama
from gemma2 import evaluate_gemma
from mistral import evaluate_mistral
from development.visualise import visualize_evaluation_metrics

# Streamlit config
st.set_page_config(page_title="LLM Evaluation Dashboard", layout="wide")
st.title("🔍 LLM Technique Evaluation Dashboard")

# Initialize session state
if "reports" not in st.session_state:
    st.session_state.reports = {}

start_button = st.button("Start Evaluation")

if start_button or "start_clicked" in st.session_state:
    st.session_state.start_clicked = True  # Save that they clicked Start

if "start_clicked" in st.session_state:
    st.sidebar.title("🔧 Select a Model")
    model_tabs = {
        "LLaMA3.2": "LLaMA3.2 Model Evaluation",
        "Gemma2": "Gemma2 Model Evaluation",
        "Mistral": "Mistral Model Evaluation"
    }
    selected_model = st.sidebar.selectbox("Choose a model to evaluate:", list(model_tabs.keys()))

    # New: Add a "Run Evaluation" button
    run_evaluation = st.sidebar.button("🚀 Run Evaluation")

    st.header("📚 About the Project")
    st.write("""
    This dashboard evaluates different Large Language Models (LLMs) using two techniques:

    - **In-Context Learning (ICL)**
    - **Fine-Tuning (FT)**

    The goal is to compare the performance of the models under both techniques.
    """)

    if run_evaluation:
        st.session_state.reports.clear()
        st.subheader(model_tabs[selected_model])

        try:
            if selected_model == "LLaMA3.2":
                llama_report = evaluate_llama()
                if llama_report:
                    st.session_state.reports["LLaMA3.2"] = llama_report

            elif selected_model == "Gemma2":
                gemma_report = evaluate_gemma()
                if gemma_report:
                    st.session_state.reports["Gemma2"] = gemma_report

            elif selected_model == "Mistral":
                mistral_report = evaluate_mistral()
                if mistral_report:
                    st.session_state.reports["Mistral"] = mistral_report

        except Exception as e:
            st.error(f"⚠️ Evaluation Error: {str(e)}")

        if st.session_state.reports:
            st.header("📊 Comparative Visualization of Evaluation Metrics")
            visualize_evaluation_metrics(st.session_state.reports)

else:
    st.write("Click the button to start the evaluation process!")
