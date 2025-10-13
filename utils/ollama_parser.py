"""
Ollama Integration for Resume Parsing
Local AI processing without API keys or internet requirements
"""

import requests
import json
import streamlit as st
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

class OllamaParser:
    """Local AI resume parser using Ollama."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.available_models = []
        self.check_connection()
    
    def check_connection(self) -> bool:
        """Check if Ollama is running and get available models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models_data = response.json()
                self.available_models = [model['name'] for model in models_data.get('models', [])]
                return True
            return False
        except Exception as e:
            return False
    
    def is_available(self) -> bool:
        """Check if Ollama service is available."""
        return len(self.available_models) > 0
    
    def get_recommended_models(self) -> List[str]:
        """Get list of recommended models for resume parsing."""
        recommended = [
            "llama3.2:3b",      # Latest, fast, good quality
            "llama3.1:8b",      # High quality, needs more RAM  
            "llama2:7b",        # Stable, widely used
            "mistral:7b",       # Fast and efficient
            "phi3:mini",        # Microsoft, very fast
            "gemma2:2b",        # Google, lightweight
        ]
        
        # Return only models that are available
        available_recommended = [model for model in recommended if model in self.available_models]
        
        # If no recommended models, return first few available
        if not available_recommended and self.available_models:
            available_recommended = self.available_models[:3]
        
        return available_recommended
    
    def install_model(self, model_name: str) -> bool:
        """Install a model via Ollama API."""
        try:
            st.info(f"🔄 Installing {model_name}... This may take a few minutes.")
            
            # Create a progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                stream=True,
                timeout=600  # 10 minutes timeout
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if 'status' in data:
                                status_text.text(f"Status: {data['status']}")
                            if 'completed' in data and 'total' in data:
                                progress = data['completed'] / data['total']
                                progress_bar.progress(progress)
                        except:
                            continue
                
                progress_bar.progress(1.0)
                status_text.text("✅ Installation complete!")
                self.check_connection()  # Refresh available models
                return True
            
            return False
            
        except Exception as e:
            st.error(f"Failed to install {model_name}: {str(e)}")
            return False
    
    def parse_resume(self, resume_text: str, model: str = None) -> Dict[str, Any]:
        """Parse resume using Ollama model."""
        
        if not self.available_models:
            return {
                "error": "No Ollama models available. Please install a model first.",
                "setup_required": True
            }
        
        # Use first available model if specified model not available
        if not model or model not in self.available_models:
            model = self.available_models[0]
        
        prompt = f"""
        You are an expert resume parser. Extract the following information from this resume and return ONLY a valid JSON object:

        {{
            "personal_info": {{
                "name": "Full name",
                "email": "email@example.com",
                "phone": "phone number",
                "location": "city, state/country",
                "linkedin": "LinkedIn URL if mentioned",
                "github": "GitHub URL if mentioned"
            }},
            "summary": "Professional summary in 2-3 sentences",
            "experience": [
                {{
                    "company": "Company name",
                    "position": "Job title", 
                    "duration": "Start - End dates",
                    "responsibilities": ["Key responsibility 1", "Key responsibility 2"],
                    "achievements": ["Achievement 1", "Achievement 2"]
                }}
            ],
            "education": [
                {{
                    "institution": "School/University name",
                    "degree": "Degree type and field",
                    "year": "Graduation year",
                    "gpa": "GPA if mentioned"
                }}
            ],
            "skills": {{
                "technical": ["Technical skill 1", "Technical skill 2"],
                "soft": ["Soft skill 1", "Soft skill 2"],
                "languages": ["Programming language 1", "Programming language 2"],
                "tools": ["Tool 1", "Tool 2"]
            }},
            "projects": [
                {{
                    "name": "Project name",
                    "description": "Brief description",
                    "technologies": ["Tech 1", "Tech 2"],
                    "url": "Project URL if mentioned"
                }}
            ],
            "certifications": ["Certification 1", "Certification 2"],
            "achievements": ["Achievement 1", "Achievement 2"],
            "languages": ["Language 1", "Language 2"]
        }}

        Resume text:
        {resume_text}

        Return only the JSON object, no additional text or formatting:
        """
        
        try:
            st.write(f"🦙 Processing with Ollama model: {model}")
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,  # Low temperature for consistent output
                        "top_p": 0.9,
                        "num_ctx": 4096,  # Context length
                        "stop": ["Human:", "Assistant:"]
                    }
                },
                timeout=180  # 3 minutes timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                
                # Try to extract JSON from response
                try:
                    # Find JSON in response (handle cases where model adds extra text)
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    
                    if json_start != -1 and json_end > json_start:
                        json_text = response_text[json_start:json_end]
                        parsed_data = json.loads(json_text)
                        parsed_data['_model_used'] = model
                        parsed_data['_source'] = 'ollama'
                        parsed_data['_timestamp'] = datetime.now().isoformat()
                        return parsed_data
                    else:
                        # If no valid JSON found, return structured fallback
                        return {
                            "error": "Could not extract valid JSON from model response",
                            "raw_response": response_text[:500],
                            "_model_used": model,
                            "_source": "ollama"
                        }
                        
                except json.JSONDecodeError as e:
                    return {
                        "error": f"JSON parsing failed: {str(e)}",
                        "raw_response": response_text[:500],
                        "_model_used": model,
                        "_source": "ollama"
                    }
            else:
                return {
                    "error": f"Ollama API error: {response.status_code}",
                    "message": response.text,
                    "_source": "ollama"
                }
                
        except requests.exceptions.Timeout:
            return {
                "error": "Request timed out. The model might be processing a large resume.",
                "_source": "ollama"
            }
        except Exception as e:
            return {
                "error": f"Unexpected error: {str(e)}",
                "_source": "ollama"
            }
    
    def generate_insights(self, resume_text: str, model: str = None) -> Dict[str, Any]:
        """Generate insights about the resume."""
        
        if not model and self.available_models:
            model = self.available_models[0]
        
        prompt = f"""
        Analyze this resume and provide insights. Return only a JSON object:

        {{
            "experience_summary": "2-3 sentences about work experience and career level",
            "skill_analysis": "Analysis of technical and soft skills, strengths and gaps",
            "career_progression": "How the career has developed over time",
            "strengths": "Key strengths and competitive advantages of the candidate",
            "recommendations": "2-3 specific suggestions for improvement",
            "experience_level": "Entry/Mid/Senior level assessment",
            "industry_fit": "Which industries or roles would be a good fit"
        }}

        Resume: {resume_text}
        
        Return only valid JSON:
        """
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_ctx": 2048
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_text = response_text[json_start:json_end]
                    insights = json.loads(json_text)
                    insights['_model_used'] = model
                    insights['_source'] = 'ollama'
                    return insights
            
            return {"error": "Could not generate insights", "_source": "ollama"}
            
        except Exception as e:
            return {"error": f"Failed to generate insights: {str(e)}", "_source": "ollama"}

def create_ollama_setup_guide():
    """Create Ollama setup guide in Streamlit."""
    
    st.sidebar.header("🦙 Ollama Local AI")
    
    # Check Ollama status first
    parser = OllamaParser()
    
    if parser.available_models:
        st.sidebar.success(f"✅ Ollama running with {len(parser.available_models)} models")
        
        # Model selection
        selected_model = st.sidebar.selectbox(
            "Select Model:",
            parser.available_models,
            help="Choose which local AI model to use"
        )
        
        # Model info
        with st.sidebar.expander("📊 Model Information"):
            for model in parser.available_models:
                st.sidebar.write(f"• {model}")
        
        return parser, selected_model
    else:
        st.sidebar.error("❌ Ollama not running or no models installed")
        
        with st.sidebar.expander("📋 Setup Instructions", expanded=True):
            st.markdown("""
            ### 🚀 Quick Setup:
            
            **1. Install Ollama:**
            - Windows: Download from [ollama.ai](https://ollama.ai/download)
            - Mac/Linux: `curl -fsSL https://ollama.ai/install.sh | sh`
            
            **2. Install a model:**
            ```bash
            ollama pull llama3.2:3b
            ```
            
            **3. Verify installation:**
            ```bash
            ollama list
            ```
            """)
        
        # Quick install buttons for recommended models
        st.sidebar.write("**Quick Install (if Ollama is running):**")
        recommended = ["llama3.2:3b", "phi3:mini", "gemma2:2b"]
        
        for model in recommended:
            if st.sidebar.button(f"📥 Install {model}"):
                if parser.install_model(model):
                    st.success(f"✅ {model} installed!")
                    st.rerun()
        
        # Check connection button
        if st.sidebar.button("🔄 Check Connection"):
            st.rerun()
        
        return None, None

def integrate_ollama_parser():
    """Integrate Ollama into the main parsing flow."""
    
    parser, selected_model = create_ollama_setup_guide()
    
    if parser and selected_model:
        st.session_state.ollama_parser = parser
        st.session_state.ollama_model = selected_model
        return True
    
    return False

def test_ollama_connection():
    """Test Ollama connection and available models."""
    
    parser = OllamaParser()
    
    if parser.available_models:
        return {
            "status": "success",
            "message": f"Ollama running with {len(parser.available_models)} models",
            "models": parser.available_models
        }
    else:
        return {
            "status": "error",
            "message": "Ollama not available or no models installed",
            "models": []
        }

if __name__ == "__main__":
    # Test Ollama connection
    result = test_ollama_connection()
    print(f"Ollama Status: {result}")
    
    if result["status"] == "success":
        print("Available models:")
        for model in result["models"]:
            print(f"  - {model}")
    else:
        print("Setup required. Please install Ollama and pull a model.")