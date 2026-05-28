from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import List
from google import genai
import os
import json
from pypdf import PdfReader
import io
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

# Wapas os.getenv se key safe tarike se uthao
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

class ATSAnalysisResult(BaseModel):
    match_percentage: int
    matched_keywords: List[str]
    missing_keywords: List[str]
    formatting_feedback: str
    improvement_tips: List[str]

@app.get("/")
def home():
    return {"status": "ATS Backend Upgraded Engine is active!"}

@app.post("/analyze", response_model=ATSAnalysisResult)
async def analyze_resume(
    job_description: str = Form(...), 
    file: UploadFile = File(...)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Bhai, sirf PDF file hi allowed hai!")

    try:
        pdf_bytes = await file.read()
        pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
        
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += page.extract_text() or ""
            
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="PDF se text read nahi ho paya.")

        prompt = f"""
        You are an advanced Applicant Tracking System (ATS) expert.
        Analyze the given Resume text against the provided Job Description (JD).
        
        Resume Content:
        {resume_text}
        
        Job Description Content:
        {job_description}
        
        Provide analysis STRICTLY as a single, valid JSON matching this schema:
        {{
            "match_percentage": 75,
            "matched_keywords": ["Python", "FastAPI"],
            "missing_keywords": ["Docker", "AWS"],
            "formatting_feedback": "Resume formatting looks good.",
            "improvement_tips": ["Add projects."]
        }}
        Return only the raw JSON string. Do not include markdown styling, no triple backticks, and no text before or after the JSON.
        """

        # 🤖 Naya Model Invoke karne ka tareeka
        response = client.models.generate_content(
            model='gemini-2.5-flash',  # 👈 Ekdum naya aur active model!
            contents=prompt,
        )
        
        raw_text = response.text.strip()
        
        # Safeguard: Agar fir bhi backticks aayein toh saaf karo
        if raw_text.startswith("```"):
            lines = raw_text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            raw_text = "\n".join(lines).strip()

        result_dict = json.loads(raw_text)
        return ATSAnalysisResult(**result_dict)

    except json.JSONDecodeError as json_err:
        print(f"❌ JSON Parsing Error: {str(json_err)} | Raw Text:\n{response.text}")
        raise HTTPException(status_code=500, detail="AI response properly JSON mein convert nahi ho paya.")
    except Exception as e:
        print(f"❌ System Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))