from fastapi import UploadFile
from typing import List
import pdfplumber
import docx
import os
from locations import Location


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

    @staticmethod
    def save_job_doc(file):
        file_path = os.path.join(Location.JOB_DOC_LOCATION.value, file.filename)

        with open(file_path, "wb") as buffer:
            for chunk in iter(lambda: file.file.read(4096), b""):
                buffer.write(chunk)
        return file_path

    @staticmethod
    def save_resume_doc(file):
        file_path = os.path.join(Location.RESUME_DOC_LOCATION.value, file.filename)
        with open(file_path, "wb") as buffer:
            for chunk in iter(lambda: file.file.read(4096), b""):
                buffer.write(chunk)
        return file_path

    @staticmethod
    def create_all_locations():
        os.makedirs(
            Location.JOB_DOC_LOCATION.value, exist_ok=True
        )  # job description folder
        os.makedirs(Location.RESUME_DOC_LOCATION.value, exist_ok=True)  # resume folder
        print("created required folders...")
        return True
