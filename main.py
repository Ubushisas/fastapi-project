from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from g4f.client import Client

app = FastAPI()

# Set the model name here
MODEL_NAME = "claude-3.5-sonnet"

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate/")
async def generate_response(request: PromptRequest):
    client = Client()
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": request.prompt}],
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

