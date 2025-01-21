import uvicorn
from fastapi import FastAPI 
from pydantic import BaseModel
from langchain_community.llms import Ollama


model_name = Ollama(model="llama2-uncensored")

class input_data(BaseModel):
    data : str

app = FastAPI()

@app.post("/prompt")
async def get_prompt(data: input_data):
    return model_name.invoke(data.data)


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8506)