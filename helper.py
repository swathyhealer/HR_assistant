from fastapi import UploadFile
from typing import List
import pdfplumber
import docx


class Helper:

    @staticmethod
    def extract_text_from_pdf(file: UploadFile) -> str:
        with pdfplumber.open(file.file) as pdf:
            text = "\n".join(
                [page.extract_text() for page in pdf.pages if page.extract_text()]
            )
        return text

    @staticmethod
    def extract_text_from_docx(file: UploadFile) -> str:
        doc = docx.Document(file.file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    @staticmethod
    def parse_job_description(text: str) -> List[str]:
        criteria = []
        for line in text.split("\n"):
            if any(
                keyword in line.lower()
                for keyword in ["must", "experience", "strong", "required", "preferred"]
            ):
                criteria.append(line.strip())
        return criteria
