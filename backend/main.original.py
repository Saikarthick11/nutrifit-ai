
import re
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="NutriFit AI")

class Message(BaseModel):
    text: str

class Food(BaseModel):
    name: str
    quantity: int | None = None
    unit: str | None = None

class ExtractionResult(BaseModel):
    intent: str
    foods: list[Food]
    missing_fields: list[str]
    clarification_question: str | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/baseline/extract", response_model=ExtractionResult)
def baseline_extract(message: Message):
    pattern = (
        r"(?:(\d+)\s*(slices?\s+of\s+)? )?"
    )
    # A small baseline pattern for our initial test
    pattern = (
        r"(?:(\d+)\s*(slices?\s+of\s+)?)?"
        r"(toast|eggs?|bread)\b"
    )

    foods = []
    for match in re.finditer(pattern, message.text.lower()):
        number, unit, name = match.groups()
        foods.append(Food(
            name="eggs" if name == "egg" else name,
            quantity=int(number) if number else None,
            unit="slices" if unit else "count"
        ))

    missing = [
        f"quantity:{food.name}"
        for food in foods if food.quantity is None
    ]

    question = None
    if missing:
        name = missing[0].split(":")[1]
        question = f"How many {name} did you eat?"

    return ExtractionResult(
        intent="meal_log" if foods else "unknown",
        foods=foods,
        missing_fields=missing,
        clarification_question=question
    )
