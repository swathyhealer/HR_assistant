from google import genai
from google.genai import types
from gemini_schema import KeyRankingCriteria
import os

gemini_api_key = os.getenv("gemini_api_key")

if not gemini_api_key:
    raise ValueError("API_KEY is not set in environment variables")


class GeminiCriteriaExtractor:
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
        self.temperature = 0
        self.response_mime_type = "application/json"
        self.response_schema = KeyRankingCriteria
        self.system_instruction = """
You are an AI assistant specialized in analyzing job descriptions to extract key ranking criteria. Your goal is to identify and extract the most important requirements that employers use to evaluate candidates.

Instructions:
1. Extract only clear ranking criteria — these are the essential qualifications, experiences, and skills that affect a candidate’s suitability.
2. Ignore generic statements such as company culture, team dynamics, or vague soft skills (e.g., "good communication skills" unless explicitly ranked).
3. Focus on measurable attributes like:
    a. Required years of experience in a specific field or technology
    b. Must-have certifications
    c. Essential programming languages, tools, or frameworks
    d. Education level or degree requirements
    e. Domain-specific expertise (e.g., "Experience in financial modeling" or "Background in NLP")
4. Please remove duplicated skills and rephrase the criteria into a shorter sentences without losing information.
"""

    def extract(self, file_path):
        file_upload = self.client.files.upload(file=file_path)
        print("Job description file uploaded successfully !!!")
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[file_upload, "summarize resume"],
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
