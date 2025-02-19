from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
import pdfplumber
import docx
import pandas as pd
import io
from schema import CriteriaResponse
from helper import Helper

app = FastAPI()


@app.post(
    "/extract-criteria",
    response_model=CriteriaResponse,
    summary="Extract hiring criteria from a job description PDF",
    description="Uploads a job description PDF and extracts key hiring criteria.",
)
async def extract_criteria(file: UploadFile = File(...)):
    """
    ### Example Input:
    - A PDF file containing a job description.

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

    if file.filename.endswith(".pdf"):
        text = Helper.extract_text_from_pdf(file)
    elif file.filename.endswith(".docx"):
        text = Helper.extract_text_from_docx(file)
    else:

        raise HTTPException(
            status_code=400, detail="Only PDF or docx files are supported"
        )
    text = Helper.extract_text_from_pdf(file)
    criteria = Helper.parse_job_description(text)
    # return {"criteria": criteria}
    return CriteriaResponse(criteria=criteria)


@app.post(
    "/score-resumes",
    response_class=StreamingResponse,
    summary="Score resumes based on extracted criteria",
    description="Uploads multiple resumes and scores them against provided criteria, returning a CSV file.",
)
async def score_resumes(
    criteria: List[str] = Form(..., title="Add Criteria"),
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
    Candidate Name, Certification XYZ, Python Experience, Machine Learning, Total Score
    John Doe, 5, 4, 4, 13
    Jane Smith, 4, 3, 5, 12
    Alan Brown, 3, 5, 4, 12
    ```
    """
    scores = []
    for file in files:
        if file.filename.endswith(".pdf"):
            text = Helper.extract_text_from_pdf(file)
        elif file.filename.endswith(".docx"):
            text = Helper.extract_text_from_docx(file)
        else:
            continue

        candidate_name = file.filename.split(".")[0]
        criteria_scores = {c: text.lower().count(c.lower()) for c in criteria}
        total_score = sum(criteria_scores.values())
        scores.append(
            {
                "Candidate Name": candidate_name,
                **criteria_scores,
                "Total Score": total_score,
            }
        )

    df = pd.DataFrame(scores)
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),  # Convert CSV to iterable stream
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=resume_scores.csv"},
    )
