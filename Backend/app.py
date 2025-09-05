import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.llms import HuggingFacePipeline

# Load Hugging Face token from environment variable
HF_TOKEN = os.environ.get("HF_TOKEN")
MODEL_NAME = "google/flan-t5-small"

# Load tokenizer & model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_auth_token=HF_TOKEN)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, use_auth_token=HF_TOKEN)

# Create pipeline and wrap with LangChain
generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
llm = HuggingFacePipeline(pipeline=generator)

# FastAPI app
app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    user_input = data.get("text", "")
    output = llm(user_input)   # LangChain call
    return {"response": output}

# ✅ Local dev entrypoint
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
