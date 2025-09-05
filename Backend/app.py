import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load Hugging Face token from environment variable
HF_TOKEN = os.environ.get("HF_TOKEN")
MODEL_NAME = "google/flan-t5-small"

# Load model & tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_auth_token=HF_TOKEN)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, use_auth_token=HF_TOKEN)
generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

# FastAPI app
app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to your frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    user_input = data.get("text", "")
    output = generator(user_input, max_length=100, num_return_sequences=1)
    return {"response": output[0]["generated_text"]}

# ✅ For local testing only
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
