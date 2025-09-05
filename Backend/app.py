from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.llms import HuggingFacePipeline
from fastapi.middleware.cors import CORSMiddleware
import os

HF_TOKEN = os.environ.get("HF_TOKEN")

app = FastAPI(title="Shathik GPT Backend")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace '*' with your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face token

MODEL_NAME = "google/flan-t5-small"

# Load model & tokenizer once at startup
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_auth_token=HF_TOKEN)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, use_auth_token=HF_TOKEN)
generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
llm = HuggingFacePipeline(pipeline=generator)

# Request model
class Prompt(BaseModel):
    text: str

@app.post("/generate")
def generate(prompt: Prompt):
    output = llm(prompt.text)
    return {"generated_text": output}

# Optional root endpoint
@app.get("/")
def read_root():
    return {"message": "CatGPT backend is live!"}
