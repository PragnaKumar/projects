# Total Time Out Summary
### Overview 
This is a basic dataframe project wherein it's main aim is to calculate the ***Total Out Duration Time and Total In Duration Time*** of employees in a company. This project is presented in a **Streamlit Application** where in you can upload an *excel* file and download the same after calculating the ***Total Out Duration Time and Total In Duration Time*** of employees.

### Contents of Project
- The main.py file contains the logic and Streamlit Application to view the project.
- The main.ipynb file or development folder can be used for any development purposes.
- The *excel* file is an example considered.

#### Command to run application

***CLI***
```bash
    streamlit run main.py --server.fileWatcherType none
``` 

### Instructions
- Make sure that your ***excel*** file is not corrupted.
- Make sure that your ***excel*** file has the headers in the following names 
    -> **DurationOut** *for calculating out duration time.*
    -> **Duration** *which is the total duration*
- Always use a ***virtual environment*** to run the application
    **To create environment in conda use:**
    ```bash
        conda create --name yourenvname
    ```
        
    **Activate your env using:**
    ```bash
         conda activate yourenvname
    ```
- When run, the website throws an error. No need to worry, just click on **Advanced** and **Ignore**.
    This will take you to the website.

