import streamlit as st
import requests

# 1. Page Configuration - Ekdum Professional Look
st.set_page_config(page_title="AI ATS Resume Optimizer", page_icon="📄", layout="wide")

st.title("🎯 AI-Powered ATS Resume Analyzer & Optimizer")
st.markdown("""
    ### Check your resume compatibility against any Job Description instantly!
    This system uses advanced AI to analyze your resume, calculate an ATS match score, extract missing keywords, and provide actionable formatting feedback.
""")

st.markdown("---")

# 2. Layout Structure
col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Upload Your Resume")
    # Universal file uploader text
    uploaded_file = st.file_uploader("Upload your Resume in PDF format:", type=["pdf"])
    st.caption("ℹ️ Only standard PDF files are supported.")

with col2:
    st.subheader("💼 Paste Job Description (JD)")
    # Universal placeholder text - Koi bhi role ab fit baitega
    jd_input = st.text_area(
        "Paste the complete job description here:", 
        height=250, 
        placeholder="Paste requirements, responsibilities, and skills expected for the role here..."
    )

st.markdown("---")

# Docker container networking ke liye change
BACKEND_URL = "http://backend:8000/analyze"

# 4. Action Button & Processing
if st.button("🚀 Analyze Resume & Calculate Match Score", use_container_width=True):
    if not uploaded_file or not jd_input.strip():
        st.warning("⚠️ Please provide both your Resume PDF and the Job Description to proceed!")
    else:
        with st.spinner("Analyzing your profile matching with the Job Description... Please wait."):
            try:
                # Binary stream structure for PDF multipart upload
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                payload = {"job_description": jd_input}
                
                response = requests.post(BACKEND_URL, data=payload, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("🎯 Analysis Completed Successfully!")
                    
                    # Score display engine
                    score = result["match_percentage"]
                    if score >= 75:
                        st.balloons()
                        st.metric(label="📊 ATS Match Score", value=f"{score}%", delta="Excellent Fit")
                    elif score >= 50:
                        st.metric(label="📊 ATS Match Score", value=f"{score}%", delta="Good Potential, Needs Optimization", delta_color="off")
                    else:
                        st.metric(label="📊 ATS Match Score", value=f"{score}%", delta="Low Match, High Optimization Required", delta_color="inverse")
                    
                    st.markdown("---")
                    
                    # Keywords display
                    k1, k2 = st.columns(2)
                    with k1:
                        st.subheader("✅ Matched Keywords")
                        if result["matched_keywords"]:
                            for kw in result["matched_keywords"]: 
                                st.success(f"• {kw}")
                        else:
                            st.write("No matching keywords found.")
                            
                    with k2:
                        st.subheader("⚠️ Missing Keywords (Add These)")
                        if result["missing_keywords"]:
                            for kw in result["missing_keywords"]: 
                                st.error(f"• {kw}")
                        else:
                            st.write("Awesome! No major missing keywords.")

                    st.markdown("---")
                    
                    # Formatting Feedback
                    st.subheader("📋 Formatting & Layout Feedback")
                    st.info(result["formatting_feedback"])
                    
                    # Actionable tips
                    st.subheader("💡 Actionable Tips to Rank Higher")
                    for tip in result["improvement_tips"]: 
                        st.write(f"➡️ {tip}")
                else:
                    st.error(f"Backend Error ({response.status_code}): {response.text}")
                        
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the backend server. Make sure your FastAPI server is running on port 8000!")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {str(e)}")