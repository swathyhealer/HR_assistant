from google import genai
from google.genai import types
from gemini_schema import CandidateScore
import os


gemini_api_key = os.getenv("gemini_api_key")

if not gemini_api_key:
    raise ValueError("API_KEY is not set in environment variables")


class GeminiResumeScorer:
    def __init__(self):
        self.model_name = "gemini-2.0-flash"
        self.api_key = gemini_api_key
        self.client = genai.Client(api_key=gemini_api_key)
        self.safety_settings = [
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_ONLY_HIGH",
            ),
        ]
        self.seed = 5
        self.temperature = 0.1
        self.response_mime_type = "application/json"
        self.response_schema = CandidateScore
        self.system_instruction = """
You are an AI assistant specialized in  evaluating resume against job criteria. Resume should be scored based on the presence and relevance of each criterion using a 0-5 scale.

Instructions:

1. Extract text from each resume file.
2. Identify the candidate's name.
3. Analyze the extracted text for matches with each job criterion.
4. Assign scores based on relevance and presence.

"""

    def score_generator(self, criteria, resume_file_path):
        file_upload = self.client.files.upload(file=resume_file_path)
        print("resume file uploaded successfully")
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                file_upload,
                f"Evaluate given resume against given job criteria :\n {criteria}",
            ],
            config=types.GenerateContentConfig(
                temperature=self.temperature,
                seed=self.seed,
                safety_settings=self.safety_settings,
                response_mime_type=self.response_mime_type,
                response_schema=self.response_schema,
                system_instruction=self.system_instruction,
            ),
        )

        return dict(response.parsed)

    def scoring_pipeline(self, criteria, file_paths):
        result = []
        for file_path in file_paths:
            filename = os.path.basename(file_path)
            candidate_data = self.score_generator(
                criteria=criteria, resume_file_path=file_path
            )
            candidate_data["filename"] = filename
            for cri, score in zip(candidate_data["critera"], candidate_data["scores"]):
                candidate_data[cri] = score
            # make perfect order
            candidate_data["total score"] = candidate_data["total_score"]

            del candidate_data["critera"]
            del candidate_data["scores"]
            del candidate_data["total_score"]
            result.append(candidate_data)
        return result
