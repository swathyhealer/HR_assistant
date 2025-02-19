from pydantic import BaseModel
from typing import List


class CriteriaResponse(BaseModel):
    criteria: List[str]
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "criteria": [
                        "Must have certification XYZ",
                        "5+ years of experience in Python development",
                        "Strong background in Machine Learning",
                    ]
                }
            ]
        }
    }
