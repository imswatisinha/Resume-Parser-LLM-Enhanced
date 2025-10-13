from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st
import json

# Helper: try to extract a JSON object from noisy model output
def _extract_json_block(text: str):
    """Extract first JSON object found in text by matching outermost braces.
    Returns parsed JSON or raises json.JSONDecodeError.
    """
    try:
        # quick attempt
        return json.loads(text)
    except Exception:
        # fallback: find first '{' and last '}' and try to parse that slice
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            candidate = text[start:end+1]
            return json.loads(candidate)
        raise

# Import alternative AI providers
try:
    from .gemini_parser import GeminiParser
except ImportError:
    GeminiParser = None
    
try:
    from .huggingface_parser import HuggingFaceParser
except ImportError:
    HuggingFaceParser = None

# Load .env file
load_dotenv()

def get_openai_client():
    """Initialize and return OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.error(
            "❌ ERROR: Missing OpenAI API key. Please create a `.env` file and add:\n"
            "OPENAI_API_KEY=your_api_key_here"
        )
        return None
    
    return OpenAI(api_key=api_key)

def parse_resume_text(text):
    """
    Sends resume text to the LLM and returns extracted structured data.
    
    Args:
        text (str): Raw resume text
        
    Returns:
        dict: Structured resume data
    """
    client = get_openai_client()
    if not client:
        return {"error": "OpenAI client not available"}
    
    # List of models to try (in order of preference)
    models_to_try = [
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
        "gpt-4",
        "gpt-4-turbo"
    ]
    
    prompt = f"""
You are an expert resume analyzer. Carefully parse the resume below and produce a **concise, plain-language summary**. 

Instructions:

1. Go section by section: **Education, Experience, Projects, Skills, Certifications**. Include all entries, even if multiple items exist.
2. For **Education**: summarize degrees, institutions, and years (if available).
3. For **Experience**: summarize companies, roles, durations, and key responsibilities or achievements.
4. For **Projects**: summarize project names, descriptions, and technologies used.
5. For **Skills**: list all technologies, tools, programming languages, frameworks, and methodologies explicitly mentioned.
6. For **Certifications**: list all certifications.
7. After summarizing, suggest **one or more suitable job roles** for the candidate (e.g., Software Developer, Frontend Developer, Data Scientist, AI Engineer, Full Stack Developer) based on the resume content.
8. Use **plain readable sentences or bullet points**. Avoid technical formatting or JSON.
9. Only summarize what is explicitly present in the resume.

Resume text:
{text}
"""

    # Try each model until one works
    for model in models_to_try:
        try:
            st.write(f"🤖 Trying model: {model}")
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
        
            # Try to parse as JSON, fallback to text if it fails
            result = response.choices[0].message.content
            # Try direct JSON parse, then try to extract JSON block if noisy
            try:
                parsed_result = json.loads(result)
                st.success(f"✅ Successfully parsed with model: {model}")
                return parsed_result
            except Exception:
                try:
                    parsed_result = _extract_json_block(result)
                    st.success(f"✅ Successfully parsed JSON block from model: {model}")
                    return parsed_result
                except Exception:
                    st.success(f"✅ Got response from model: {model} (raw format)")
                    return {"raw_output": result}
                
        except Exception as e:
            st.warning(f"⚠️ Model {model} failed: {str(e)}")
            continue  # Try next model
    
    # If OpenAI models failed, try alternative AI providers
    st.info("🔄 Trying alternative AI providers...")
    
    # Try Google Gemini (Free)
    if GeminiParser:
        try:
            st.write("🚀 Trying Google Gemini (Free)...")
            gemini_parser = GeminiParser()
            if gemini_parser.is_available():
                gemini_result = gemini_parser.parse_resume(text)
                if "error" not in gemini_result:
                    st.success("✅ Successfully parsed with Google Gemini!")
                    return gemini_result
                else:
                    st.warning(f"⚠️ Gemini failed: {gemini_result['error']}")
            else:
                st.info("ℹ️ Google Gemini API key not configured")
        except Exception as e:
            st.warning(f"⚠️ Gemini error: {str(e)}")
    
    # Try HuggingFace (Free)
    if HuggingFaceParser:
        try:
            st.write("🤗 Trying HuggingFace (Free)...")
            hf_parser = HuggingFaceParser()
            if hf_parser.is_available():
                hf_result = hf_parser.parse_resume(text)
                if "error" not in hf_result:
                    st.success("✅ Successfully parsed with HuggingFace!")
                    return hf_result
                else:
                    st.warning(f"⚠️ HuggingFace failed: {hf_result['error']}")
            else:
                st.info("ℹ️ HuggingFace API key not configured")
        except Exception as e:
            st.warning(f"⚠️ HuggingFace error: {str(e)}")
    
    # Final fallback to offline parsing
    st.warning("🤖 All AI services unavailable. Switching to offline parser...")
    
    try:
        from .offline_parser import parse_resume_offline
        offline_result = parse_resume_offline(text)
        offline_result["fallback_reason"] = "all_ai_providers_failed"
        return offline_result
    except ImportError:
        return {"error": "All AI providers failed and offline parser not available. Please configure at least one AI service."}

def format_resume_display(parsed_data):
    """
    Format parsed resume data for better display in Streamlit.
    
    Args:
        parsed_data (dict): Parsed resume data
        
    Returns:
        None: Displays formatted data in Streamlit
    """
    if "error" in parsed_data:
        st.error(parsed_data["error"])
        return
    
    if "raw_output" in parsed_data:
        st.warning("Could not parse as structured JSON. Raw output:")
        st.text(parsed_data["raw_output"])
        return
    
    # Check if this is offline parsing
    if parsed_data.get("parsing_method") == "offline_basic":
        from .offline_parser import format_offline_results
        return format_offline_results(parsed_data)
    
    # Show AI provider info
    ai_provider = parsed_data.get("ai_provider", "openai")
    model = parsed_data.get("model", "unknown")
    
    provider_emojis = {
        "openai": "🤖",
        "google_gemini": "🚀", 
        "huggingface": "🤗"
    }
    
    emoji = provider_emojis.get(ai_provider, "🤖")
    st.info(f"{emoji} Parsed using: {ai_provider.replace('_', ' ').title()} ({model})")
    
    # Display structured data
    if parsed_data.get("name"):
        st.subheader(f"👤 {parsed_data['name']}")
    
    # Contact Information
    col1, col2 = st.columns(2)
    with col1:
        if parsed_data.get("email"):
            st.write(f"📧 **Email:** {parsed_data['email']}")
    with col2:
        if parsed_data.get("phone"):
            st.write(f"📱 **Phone:** {parsed_data['phone']}")
    
    # Education
    if parsed_data.get("education"):
        st.subheader("🎓 Education")
        for edu in parsed_data["education"]:
            st.write(f"**{edu.get('degree', 'N/A')}** - {edu.get('institution', 'N/A')}")
            if edu.get("year"):
                st.write(f"Year: {edu['year']}")
            if edu.get("gpa"):
                st.write(f"GPA: {edu['gpa']}")
            st.write("---")
    
    # Experience
    if parsed_data.get("experience"):
        st.subheader("💼 Experience")
        for exp in parsed_data["experience"]:
            st.write(f"**{exp.get('role', 'N/A')}** at {exp.get('company', 'N/A')}")
            if exp.get("duration"):
                st.write(f"Duration: {exp['duration']}")
            if exp.get("description"):
                st.write(f"Description: {exp['description']}")
            st.write("---")
    
    # Skills
    if parsed_data.get("skills"):
        st.subheader("🛠️ Skills")
        st.write(", ".join(parsed_data["skills"]))
    
    # Projects
    if parsed_data.get("projects"):
        st.subheader("🚀 Projects")
        for proj in parsed_data["projects"]:
            st.write(f"**{proj.get('name', 'N/A')}**")
            if proj.get("description"):
                st.write(proj["description"])
            if proj.get("technologies"):
                st.write(f"Technologies: {', '.join(proj['technologies'])}")
            st.write("---")
    
    # Certifications
    if parsed_data.get("certifications"):
        st.subheader("🏆 Certifications")
        for cert in parsed_data["certifications"]:
            st.write(f"• {cert}")

def show_ai_service_status():
    """Show status of available AI services in sidebar"""
    
    st.sidebar.header("🤖 AI Services Status")
    
    # OpenAI Status
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        st.sidebar.write("🤖 **OpenAI**: ⚠️ Quota issues")
    else:
        st.sidebar.write("🤖 **OpenAI**: ❌ Not configured")
    
    # Google Gemini Status
    if GeminiParser:
        gemini_parser = GeminiParser()
        if gemini_parser.is_available():
            st.sidebar.write("🚀 **Google Gemini**: ✅ Available (Free)")
        else:
            st.sidebar.write("🚀 **Google Gemini**: ❌ Not configured")
    else:
        st.sidebar.write("🚀 **Google Gemini**: ❌ Not installed")
    
    # HuggingFace Status  
    if HuggingFaceParser:
        hf_parser = HuggingFaceParser()
        if hf_parser.is_available():
            st.sidebar.write("🤗 **HuggingFace**: ✅ Available (Free)")
        else:
            st.sidebar.write("🤗 **HuggingFace**: ❌ Not configured")
    else:
        st.sidebar.write("🤗 **HuggingFace**: ❌ Not installed")
    
    # Offline Parser
    st.sidebar.write("💻 **Offline Parser**: ✅ Always available")
    
    return True