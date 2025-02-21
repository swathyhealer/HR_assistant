import os
from locations import Location


class Helper:

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
