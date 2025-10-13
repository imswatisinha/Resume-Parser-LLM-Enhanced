"""
Google Gemini Integration for Resume Parsing
Free Alternative to OpenAI GPT models
"""

import os
import json
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class GeminiParser:
    """Google Gemini API integration for resume parsing"""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
    def is_available(self):
        """Check if Gemini API is available"""
        return bool(self.api_key)
    
    def parse_resume(self, text):
        """Parse resume using Google Gemini API"""
        
        if not self.is_available():
            return {"error": "Google Gemini API key not found. Add GOOGLE_GEMINI_API_KEY to your .env file"}
        
        try:
            import requests
            
            prompt = f"""
            Extract the following information from this resume and return it as a JSON object:
            
            {{
                "name": "Full Name",
                "email": "email@example.com", 
                "phone": "phone number",
                "education": [
                    {{
                        "degree": "Degree Name",
                        "institution": "University/College",
                        "year": "Graduation Year"
                    }}
                ],
                "experience": [
                    {{
                        "company": "Company Name",
                        "role": "Job Title", 
                        "duration": "Start - End Date",
                        "description": "Key responsibilities"
                    }}
                ],
                "skills": ["skill1", "skill2", "skill3"],
                "projects": [
                    {{
                        "name": "Project Name",
                        "description": "Project Description"
                    }}
                ],
                "certifications": ["certification1", "certification2"]
            }}
            
            Resume text:
            {text}
            
            Return only valid JSON. If information is not found, use null or empty array.
            """
            
            url = f"{self.base_url}/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 2048
                }
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                if 'candidates' in result and len(result['candidates']) > 0:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    
                    # Try to parse as JSON
                    try:
                        # Clean the response (remove markdown formatting if present)
                        content = content.strip()
                        if content.startswith('```json'):
                            content = content[7:]
                        if content.endswith('```'):
                            content = content[:-3]
                        content = content.strip()
                        
                        parsed_data = json.loads(content)
                        parsed_data["ai_provider"] = "google_gemini"
                        parsed_data["model"] = "gemini-1.5-flash"
                        return parsed_data
                        
                    except json.JSONDecodeError:
                        return {
                            "raw_output": content,
                            "ai_provider": "google_gemini",
                            "model": "gemini-1.5-flash"
                        }
                else:
                    return {"error": "No response from Gemini API"}
            else:
                return {"error": f"Gemini API error: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"error": f"Gemini parsing failed: {str(e)}"}

def setup_gemini_instructions():
    """Display instructions for setting up Google Gemini API"""
    
    st.sidebar.header("🔧 Setup Google Gemini (Free)")
    
    with st.sidebar.expander("📋 How to get FREE Gemini API Key"):
        st.markdown("""
        **Step 1:** Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
        
        **Step 2:** Sign in with your Google account
        
        **Step 3:** Click "Create API Key"
        
        **Step 4:** Copy the API key
        
        **Step 5:** Add to your `.env` file:
        ```
        GOOGLE_GEMINI_API_KEY=your_api_key_here
        ```
        
        **✅ Benefits:**
        - Completely FREE 
        - No credit card required
        - 1,500 requests per day
        - No expiration
        """)
    
    # Check if API key is configured
    gemini_parser = GeminiParser()
    if gemini_parser.is_available():
        st.sidebar.success("✅ Gemini API configured!")
        return True
    else:
        st.sidebar.warning("⚠️ Gemini API not configured")
        return False

# Test function
def test_gemini_connection():
    """Test Google Gemini API connection"""
    
    parser = GeminiParser()
    
    if not parser.is_available():
        return {
            "status": "error",
            "message": "Gemini API key not found"
        }
    
    # Test with simple text
    test_text = """
    John Doe
    john.doe@email.com
    (555) 123-4567
    
    Software Engineer at Tech Corp
    Bachelor's in Computer Science from State University
    Skills: Python, JavaScript, React
    """
    
    try:
        result = parser.parse_resume(test_text)
        
        if "error" in result:
            return {
                "status": "error",
                "message": result["error"]
            }
        else:
            return {
                "status": "success",
                "message": "Gemini API working correctly!",
                "sample_result": result
            }
            
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Test failed: {str(e)}"
        }

if __name__ == "__main__":
    # Test Gemini connection
    result = test_gemini_connection()
    print(f"Gemini Test: {result}")