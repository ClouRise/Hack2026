from pydantic import BaseModel
from typing import List


class AnswersRequest(BaseModel):
    answers: List[str]


class ChatResponse(BaseModel):
    result: str