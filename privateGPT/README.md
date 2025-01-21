# PRIVATE GPT 
This is a private GPT project which can be run locally without any internet connection
To install follow the steps in the below link
--> https://github.com/ollama/ollama/tree/main/examples/langchain-python-rag-privategpt

Download the following files--

--> constants.py
--> ingest.py
--> privateGPT.py

Make sure that the python version is **<=3.10**

Use the **Makefile** to run the project

Add your pdfs in the *source_documents* folder.
Activate your environment using the below command:
```bash
    make activate
```

After adding your files, run the below command in your CLI
```bash
    make update
```

After updating your files, run the script using the below command
```bash
    make run
```

To check API use the following command
```bash
    make api
```


