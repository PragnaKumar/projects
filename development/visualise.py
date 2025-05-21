import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Assuming classification reports are already computed and stored
# Example structure:
# reports = {
#     "LLaMA": llama_report,
#     "Gemma2": gemma_report,
#     "Mistral": mistral_report
# }

def visualize_evaluation_metrics(reports):
    # Extract precision, recall, and f1-score for "macro avg" (can also choose "weighted avg" if needed)
    metrics_data = []

    for model_name, report in reports.items():
        metrics_data.append({
            "Model": model_name,
            "Precision": report["precision"],
            "Recall": report["recall"],
            "Response Time": report["response_time"]
        })

    df_metrics = pd.DataFrame(metrics_data)

    st.subheader("Model Performance Comparison")

    # Melt the dataframe for easier plotting
    df_melted = df_metrics.melt(id_vars="Model", var_name="Metric", value_name="Score")

    # Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Metric", y="Score", hue="Model", data=df_melted)
    plt.ylim(0, 1)
    plt.title("Precision, Recall, and F1-Score Comparison Across Models")
    plt.ylabel("Score")
    plt.xlabel("Metric")
    plt.legend(title="Model", loc="lower right")
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    st.pyplot(plt)
