from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
import pandas as pd
import io
from schema import CriteriaResponse
from helper import Helper
from criteria_extractor import GeminiCriteriaExtractor
from resume_scorer import GeminiResumeScorer


app = FastAPI()
Helper.create_all_locations()
critera_getter = GeminiCriteriaExtractor()
scorer = GeminiResumeScorer()


@app.post(
    "/extract-criteria",
    response_model=CriteriaResponse,
    summary="Extract hiring criteria from a job description PDF/DOCX",
    description="Uploads a job description PDF/DOCX and extracts key hiring criteria.",
)
def extract_criteria(file: UploadFile = File(...)):
    """
    ### Example Input:
    - A PDF/DOCX file containing a job description.

    ### Example Output:
    ```json
    {
      "criteria": [
        "Must have certification XYZ",
        "5+ years of experience in Python development",
        "Strong background in Machine Learning"
      ]
    }
    ```
    """

    if (not file.filename.endswith(".pdf")) and (not file.filename.endswith(".docx")):

        raise HTTPException(
            status_code=400, detail="Only PDF or docx files are supported"
        )

    file_path = Helper.save_job_doc(file)
    response = critera_getter.extract(file_path)
    criteria = response.get("criteria", [])
    return CriteriaResponse(criteria=criteria)


@app.post(
    "/score-resumes",
    response_class=StreamingResponse,
    summary="Score resumes based on extracted criteria",
    description="Uploads multiple resumes and scores them against provided criteria, returning a CSV file.",
)
def score_resumes(
    criteria: List[str] = Form(...),
    files: List[UploadFile] = File(...),
):
    """
    ### Example Input:
    ```json
    {
      "criteria": [
        "Must have certification XYZ",
        "5+ years of experience in Python development",
        "Strong background in Machine Learning"
      ],
      "files": [
        "<uploaded_resume_1.pdf>",
        "<uploaded_resume_2.docx>",
        "<uploaded_resume_3.pdf>"
      ]
    }
    ```

    ### Example Output:
    A CSV file with the following format:
    ```
    Candidate Name, file name , Certification XYZ, Python Experience, Machine Learning, Total Score
    John Doe, john.pdf ,5, 4, 4, 13
    Jane Smith,jane.pdf ,4, 3, 5, 12
    Alan Brown,alan.pdf, 3, 5, 4, 12
    ```
    """
    file_paths = []
    for file in files:
        file_paths.append(Helper.save_resume_doc(file))
    result = scorer.scoring_pipeline(criteria=criteria, file_paths=file_paths)
    print("completed scoring...!")
    df = pd.DataFrame(result)
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=resume_scores.csv"},
    )
