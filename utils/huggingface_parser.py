"""
Hugging Face Integration for Resume Parsing  
Free Alternative using open-source models
"""

import os
import json
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class HuggingFaceParser:
    """Hugging Face API integration for resume parsing"""
    
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.base_url = "https://api-inference.huggingface.co/models"
        
        # List of free models to try
        self.models = [
            "microsoft/DialoGPT-large",
            "google/flan-t5-large", 
            "mistralai/Mistral-7B-Instruct-v0.1",
            "HuggingFaceH4/zephyr-7b-beta"
        ]
        
    def is_available(self):
        """Check if HuggingFace API is available"""
        return bool(self.api_key)
    
    def parse_resume_with_model(self, text, model_name):
        """Parse resume using specific HuggingFace model"""
        
        try:
            import requests
            
            # Simplified prompt for open-source models
            prompt = f"""
            Extract key information from this resume:
            
            Resume: {text[:1000]}  # Limit text length for free models
            
            Please extract:
            - Name
            - Email  
            - Phone
            - Skills
            - Education
            - Experience
            
            Format as simple text.
            """
            
            url = f"{self.base_url}/{model_name}"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 300,
                    "temperature": 0.1
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    
                    # Basic parsing of the generated text
                    parsed_info = self._extract_from_text(generated_text, text)
                    parsed_info["ai_provider"] = "huggingface"
                    parsed_info["model"] = model_name
                    
                    return parsed_info
                else:
                    return {"error": f"Unexpected response format from {model_name}"}
            else:
                return {"error": f"HuggingFace API error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Model {model_name} failed: {str(e)}"}
    
    def _extract_from_text(self, generated_text, original_text):
        """Extract structured data from generated text and original resume"""
        
        import re
        
        result = {
            "name": None,
            "email": None,
            "phone": None, 
            "education": [],
            "experience": [],
            "skills": [],
            "projects": [],
            "certifications": []
        }
        
        # Combine both texts for extraction
        full_text = f"{original_text}\n{generated_text}"
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, full_text)
        if emails:
            result["email"] = emails[0]
        
        # Extract phone
        phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phones = re.findall(phone_pattern, full_text)
        if phones:
            result["phone"] = ''.join(phones[0])
        
        # Extract skills (common keywords)
        skill_keywords = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'html', 'css',
            'machine learning', 'data science', 'aws', 'docker', 'git'
        ]
        
        found_skills = []
        for skill in skill_keywords:
            if skill.lower() in full_text.lower():
                found_skills.append(skill.title())
        
        result["skills"] = found_skills[:10]  # Limit to 10 skills
        
        # Try to extract name (first meaningful line)
        lines = original_text.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 2 and len(line) < 50:
                if not any(x in line.lower() for x in ['@', 'resume', 'cv', 'phone', 'email']):
                    result["name"] = line
                    break
        
        # Add raw AI output for reference
        result["ai_analysis"] = generated_text[:200] + "..." if len(generated_text) > 200 else generated_text
        
        return result
    
    def parse_resume(self, text):
        """Parse resume trying multiple HuggingFace models"""
        
        if not self.is_available():
            return {"error": "HuggingFace API key not found. Add HUGGINGFACE_API_KEY to your .env file"}
        
        # Try each model until one works
        for model in self.models:
            st.write(f"🤖 Trying HuggingFace model: {model}")
            
            result = self.parse_resume_with_model(text, model)
            
            if "error" not in result:
                st.success(f"✅ Successfully parsed with {model}")
                return result
            else:
                st.warning(f"⚠️ Model {model} failed: {result['error']}")
        
        return {"error": "All HuggingFace models failed"}

def setup_huggingface_instructions():
    """Display instructions for setting up HuggingFace API"""
    
    st.sidebar.header("🤗 Setup HuggingFace (Free)")
    
    with st.sidebar.expander("📋 How to get FREE HuggingFace API Key"):
        st.markdown("""
        **Step 1:** Go to [HuggingFace](https://huggingface.co/join)
        
        **Step 2:** Create free account
        
        **Step 3:** Go to [Settings > Access Tokens](https://huggingface.co/settings/tokens)
        
        **Step 4:** Click "New token" → Create "Read" token
        
        **Step 5:** Copy the token
        
        **Step 6:** Add to your `.env` file:
        ```
        HUGGINGFACE_API_KEY=hf_your_token_here
        ```
        
        **✅ Benefits:**
        - Completely FREE forever
        - 1000 requests per hour  
        - No credit card required
        - Open source models
        
        **⚠️ Limitations:**
        - Lower accuracy than GPT
        - Slower responses
        - Less structured output
        """)
    
    # Check if API key is configured
    hf_parser = HuggingFaceParser()
    if hf_parser.is_available():
        st.sidebar.success("✅ HuggingFace API configured!")
        return True
    else:
        st.sidebar.warning("⚠️ HuggingFace API not configured")
        return False

def test_huggingface_connection():
    """Test HuggingFace API connection"""
    
    parser = HuggingFaceParser()
    
    if not parser.is_available():
        return {
            "status": "error",
            "message": "HuggingFace API key not found"
        }
    
    # Test with simple text
    test_text = """
    Jane Smith
    jane.smith@email.com
    (555) 987-6543
    
    Data Scientist at AI Company
    Master's in Statistics from Tech University
    Skills: Python, Machine Learning, SQL, Pandas
    """
    
    try:
        # Test just the first model
        result = parser.parse_resume_with_model(test_text, parser.models[0])
        
        if "error" in result:
            return {
                "status": "error",
                "message": result["error"]
            }
        else:
            return {
                "status": "success",
                "message": "HuggingFace API working!",
                "sample_result": result
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Test failed: {str(e)}"
        }

if __name__ == "__main__":
    # Test HuggingFace connection
    result = test_huggingface_connection()
    print(f"HuggingFace Test: {result}")