from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
from bs4 import BeautifulSoup

app = FastAPI()

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(mem):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)

class HealRequest(BaseModel):
    locator: str
    dom: str

class Requirement(BaseModel):
    text: str

@app.get("/")
def health():
    return {"status": "AI Automation API running"}

# ---------------- SELF HEAL ----------------

@app.post("/heal")
def heal(req: HealRequest):

    memory = load_memory()

    # 1️⃣ Check learned memory first
    if req.locator in memory:
        return {"locator": memory[req.locator], "source": "memory"}

    soup = BeautifulSoup(req.dom, "html.parser")

    # 2️⃣ Smart DOM based healing
    if "user" in req.locator.lower():
        healed = soup.find("input", {"id": "username"})
        if healed:
            new = "#username"

    elif "pass" in req.locator.lower():
        healed = soup.find("input", {"id": "password"})
        if healed:
            new = "#password"

    else:
        new = "button[type='submit']"

    # 3️⃣ Learn it
    memory[req.locator] = new
    save_memory(memory)

    return {"locator": new, "source": "ai"}

# ---------------- TEST GENERATOR ----------------

@app.post("/generate-tests")
def generate_tests(req: Requirement):

    feature = f"""
Feature: Auto generated

Scenario: Positive flow
  Given user opens application
  When user performs {req.text}
  Then expected result should occur

Scenario: Negative flow
  Given user opens application
  When user performs invalid {req.text}
  Then error should be shown
"""

    return {"feature": feature.strip()}

# ---------------- PAGE OBJECT GENERATOR ----------------

@app.post("/generate-pom")
def generate_pom(req: HealRequest):

    soup = BeautifulSoup(req.dom, "html.parser")

    fields = soup.find_all("input")

    methods = ""

    for f in fields:
        fid = f.get("id")
        if fid:
            methods += f"""
    public void enter{fid.capitalize()}(String value){{
        SmartLocator.find(page,"#{fid}").fill(value);
    }}
"""

    pom = f"""
public class AutoPage {{

    Page page;

    public AutoPage(Page page){{
        this.page = page;
    }}

{methods}
}}
"""

    return {"pageObject": pom.strip()}
