from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# ✅ Allow frontend at localhost:5173 to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust this if the frontend runs elsewhere
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# ✅ Request model for chat messages
class ChatRequest(BaseModel):
    message: str

# ✅ Root endpoint to check if the server is running
@app.get("/")
def read_root():
    return {"message": "Ollama FastAPI Server is running!"}

# ✅ Chat API to communicate with Ollama Phi-4
@app.post("/chat")
async def chat_with_ollama(request: ChatRequest):
    try:
        # Sending request to the locally running Ollama model
        ollama_response = requests.post(
            "http://localhost:11434/api/generate", 
            json={"model": "phi4", "prompt": request.message, "stream": False}
        )

        # Checking for a successful response
        if ollama_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to get a response from Ollama.")

        # Parsing response
        response_data = ollama_response.json()
        reply = response_data.get("response", "No response received from Ollama.")
        
        return {"reply": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")