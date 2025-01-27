from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from g4f.client import Client
import asyncio
import nest_asyncio

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

app = FastAPI()

# Set the model name here
MODEL_NAME = "claude-3.5-sonnet"

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate/")
async def generate_response(request: PromptRequest):
    client = Client()
    try:
        # Create the completion in a way that works with asyncio
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": request.prompt}],
            )
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

