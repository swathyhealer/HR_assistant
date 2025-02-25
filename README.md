#  HR Assistant

HR Assistant is a powerful tool designed to extract key criteria from job descriptions and score resumes based on those criteria. This application utilizes FastAPI and Gemini API to streamline the hiring process efficiently.

##  Setup Instructions

Follow the steps below to set up and run the HR Assistant on your system.

###  Prerequisites
Ensure you have the following installed:
- Python (>=3.8)
- Pipenv

---

###  Installation Guide

#### **1️.  Create and Activate Pipenv Environment**
```sh
pipenv install -r requirements.txt
pipenv shell
```

#### **2️. Set Up Environment Variable**
You need to store your Gemini API key as an environment variable.

**For Linux & macOS:**
```sh
export GEMINI_API_KEY="your_secret_api_key"
```

**For Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_secret_api_key"
```

---

###  Running the Application
Start the FastAPI server with:
```sh
uvicorn app:app --reload
```

Once the server is running, you can access the interactive API documentation here:
[Swagger UI](http://127.0.0.1:8000/docs)

---

###  Notes
- If you face any dependency issues, try reinstalling the environment:
  ```sh
  pipenv --rm
  pipenv install -r requirements.txt
  ```
- Make sure your API key is correct before running the application.
- You can modify the FastAPI settings (e.g., host and port) in the `uvicorn` command.

---


###  API Endpoints

####  Extract Ranking Criteria from Job Description

**API Endpoint:**
```
POST /extract-criteria
```

**Input Payload Example (Multipart Form-Data):**
```json
{
  "file": "<uploaded_job_description.pdf>"
}
```

**Output Payload Example:**
```json
{
  "criteria": [
    "Must have certification XYZ",
    "5+ years of experience in Python development",
    "Strong background in Machine Learning"
  ]
}
```

---

####  Score Resumes Against Extracted Criteria

**API Endpoint:**
```
POST /score-resumes
```

**Input Payload Example (Multipart Form-Data):**
```json
{
  "criteria": [
    "Must have certification XYZ",
    "5+ years of experience in Python development",
    "Strong background in Machine Learning"
  ],
  "files": [
    "<uploaded_resume_1.pdf>",
    "<uploaded_resume_2.pdf>",
    "<uploaded_resume_3.pdf>"
  ]
}
```

**Output Payload Example (Excel or CSV Sheet):**
```
Candidate Name  Certification XYZ  Python Experience  Machine Learning  Total Score
John Doe        5                  4                  4                13
Jane Smith      4                  3                  5                12
Alan Brown      3                  5                  4                12
```

---
---

###  Sample Test Data
To test the application, see sample test data under the folder:
```
sample_test_data/
```

---

###  Contribution Guidelines
We welcome contributions to improve **HR Assistant**! Follow these steps to contribute:

1. **Fork the Repository** - Click the fork button to create a copy of this repository on your GitHub account.
2. **Clone Your Fork** - Download your forked repository:
   ```sh
   git clone git@github.com:swathyhealer/HR_assistant.git
   ```
3. **Create a New Branch** - Name it based on the feature or bug fix:
   ```sh
   git checkout -b feature-new-functionality
   ```
4. **Make Changes & Commit** - Ensure your changes follow best practices and commit with a descriptive message:
   ```sh
   git commit -m "Added new feature: ..."
   ```
5. **Push to Your Fork** - Upload your changes to GitHub:
   ```sh
   git push origin feature-new-functionality
   ```
6. **Create a Pull Request** - Go to the original repository, open a PR, and provide a clear description of your changes.



---


