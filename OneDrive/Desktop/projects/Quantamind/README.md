# Finetuning using two different approaches on Llama3.2 large language model.
### Overiew

This project investigates two LLM Finetuning techniques—**LoRa PEFT** and **Prefix PEFT**—applied to Llama3.2 Large Language Models. The task is focused on **Question Answering (QA)** using a **Public Dataset - TAT-QA dataset by NExtplusplus**.

TAT-QA (Tabular And Textual dataset for Question Answering) contains 16,552 questions associated with 2,757 hybrid contexts from real-world financial reports.

### LoRa vs Prefix Finetuning Technique

**LoRA (Low-Rank Adaptation)**
LoRA is a parameter-efficient fine-tuning technique that injects trainable low-rank matrices into the weight matrices of a pretrained model (like a Transformer). Instead of updating all model weights, it learns a small number of parameters that adapt the model to a new task.

- How it works: Adds ΔW = A × B to frozen weights, where A and B are small matrices (low-rank).
- Efficiency: Very memory-efficient; only a small number of parameters are updated.
- Applicability: Can be used for a wide range of tasks and architectures.

**Prefix Tuning**
Prefix Tuning keeps the pretrained model completely frozen, and prepends a small sequence of task-specific continuous vectors (prefixes) to the attention keys and values at every layer.
- How it works: Trains only the prefix embeddings (like a soft prompt), not the model weights.
- Efficiency: Even lighter than LoRA in some cases; model remains unchanged.
- Applicability: Originally designed for NLP generation tasks.


### Contents of project
- *The datasets folder consists of the dataset used for finetuning. It includes a JSON format training set, which was converted to tatqa_output.pdf according to the given requirements. It also contains a test dataset for testing purposes.*
- *There are two folders which llama3.2-finetune-weights and llama3.2-prefix-tune which contains the finetuned models*
- *The jupyter notebook Quantamind.ipynb consists of Fine-tuning technique usinf PEFT LoRa and Prefix adapters.*
- *The files llama3.2-lora-finetune   llama3.2-prefix-finetune are the FT files converted to **gguf** format to run locally on Ollama.*


### Instructions
- To run the models on Ollama please refer to the git repo -> **"https://github.com/ollama/ollama"**
- Always use a ***virtual environment*** to run the application
    **To create environment in conda use:**
    ```bash
        conda create --name yourenvname
    ```

    **Activate your env using:**
    ```bash
         conda activate yourenvname
    ```
        

### Results

To evaluate the efficiency of the two fine-tuning methods, I tracked the training loss at steps 10 and 20 for both **LoRA** and **Prefix Tuning** approaches:

| Step | LoRA Loss | Prefix Tuning Loss |
|------|-----------|--------------------|
| 10   | **4.516** | 5.721              |
| 20   | **4.104** | 4.393              |

As observed, **LoRA consistently achieved lower training loss** compared to Prefix Tuning at both steps. Specifically:

- At step 10, LoRA had a **loss of 4.516**, while Prefix Tuning showed a higher loss of **5.721**.
- By step 20, LoRA further reduced the loss to **4.104**, whereas Prefix Tuning reached **4.393**.

These results suggest that **LoRA adapts faster** during early training stages and may lead to better convergence behavior.