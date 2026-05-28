#  AI-Powered ATS Resume Optimizer

An intelligent, AI-driven application designed to analyze and optimize resumes against job descriptions, providing instant keyword matching and actionable feedback to improve ATS scores and job application success.

 **Live Demo:** [Click here to view the live project on AWS](http://43.205.253.214:8501)

##  Tech Stack
* **Frontend:** Streamlit
* **Backend:** FastAPI, Python
* **AI Engine:** Generative AI (Google Gemini)
* **DevOps & Cloud:** Docker, Docker Compose, AWS EC2

##  Key Features
* **Real-time Resume Parsing:** Instantly extracts and evaluates content from uploaded resumes.
* **Job Description Matching:** Compares resume keywords against target job descriptions to identify missing skills and gaps.
* **AI-Driven Recommendations:** Provides actionable, AI-generated suggestions to enhance resume visibility and ATS compatibility.
* **Cloud Deployed:** Fully containerized with Docker and hosted securely on an AWS EC2 instance.

##  Local Setup
1. Clone the repository to your local machine :
   git clone https://github.com/adarsh-tiwari29/ai-ats-optimizer

2. Add your `.env` file with `GEMINI_API_KEY`.
    GEMINI_API_KEY = your_api_key_here

3. Run `docker compose up --build -d`.
    docker compose up --build -d

4. Access the app locally at http://43.205.253.214:8501.