from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class HealRequest(BaseModel):
    locator: str
    dom: str

@app.get("/")
def health():
    return {"status": "AI API running"}

@app.post("/heal")
def heal(req: HealRequest):
    # simple demo logic (replace with smarter later)
    if "user" in req.locator.lower():
        return {"locator": "#username"}
    if "pass" in req.locator.lower():
        return {"locator": "#password"}
    return {"locator": "button[type='submit']"}
