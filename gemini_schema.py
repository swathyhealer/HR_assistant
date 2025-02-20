from pydantic import BaseModel
from typing import List


class KeyRankingCriteria(BaseModel):

    criteria: List[str]


class CandidateScore(BaseModel):
    candidate_name: str
    critera: list[str]
    scores: list[float]
    total_score: float
