from enum import Enum
import os


class Location(Enum):
    DATA_FOLDER = "data"
    JOB_DOC_FOLDER = "job_descriptions"
    RESUME_DOC_FOLDER = "resumes"
    JOB_DOC_LOCATION = os.path.join(DATA_FOLDER, JOB_DOC_FOLDER)
    RESUME_DOC_LOCATION = os.path.join(DATA_FOLDER, RESUME_DOC_FOLDER)
