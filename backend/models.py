from datetime import date as Date
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)

class Food(StrictModel):
    name: str = Field(min_length=1, max_length=200)
    quantity: float | None = Field(default=None, gt=0, le=100000)
    unit: str | None = Field(default=None, max_length=80)

class Workout(StrictModel):
    name: str = Field(min_length=1, max_length=200)
    duration_minutes: float | None = Field(default=None, gt=0, le=1440)

class Extraction(StrictModel):
    intent: Literal['meal_log', 'workout_log', 'history', 'unknown']
    foods: list[Food] = Field(default_factory=list, max_length=20)
    workouts: list[Workout] = Field(default_factory=list, max_length=20)
    date: Date | None = None
    end_date: Date | None = None

class Message(StrictModel):
    text: str = Field(min_length=1, max_length=4000)

class Turn(Message):
    version: int = Field(ge=0)

class Start(StrictModel):
    mode: Literal['baseline', 'llm'] = 'baseline'

class Selection(StrictModel):
    version: int = Field(ge=0)
    food_index: int = Field(ge=0)
    fdc_id: int = Field(gt=0)
    grams: float | None = Field(default=None, gt=0, le=100000)
    portion_id: int | None = None
    portion_count: float | None = Field(default=None, gt=0, le=10000)

class Confirm(StrictModel):
    version: int = Field(ge=0)
