"""
Offline Resume Parser - Basic text extraction without AI
For use when OpenAI quota is insufficient
"""

import re
import json
from datetime import datetime

def parse_resume_offline(text):
    """
    Parse resume using basic text processing instead of AI.
    This is a fallback when OpenAI quota is insufficient.
    """
    
    result = {
        "name": None,
        "email": None, 
        "phone": None,
        "education": [],
        "experience": [],
        "skills": [],
        "projects": [],
        "certifications": [],
        "parsing_method": "offline_basic",
        "timestamp": datetime.now().isoformat()
    }
    
    lines = text.split('\n')
    text_lower = text.lower()
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        result["email"] = emails[0]
    
    # Extract phone numbers
    phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
    phones = re.findall(phone_pattern, text)
    if phones:
        result["phone"] = ''.join(phones[0])
    
    # Extract name (basic heuristic - first line that's not email/phone)
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        if len(line) > 3 and len(line) < 50:
            # Skip if it contains email, phone, or common resume words
            if not any(x in line.lower() for x in ['@', 'resume', 'cv', 'curriculum', 'phone', 'email']):
                if not re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', line):
                    result["name"] = line
                    break
    
    # Extract skills (look for common skill keywords)
    skill_keywords = [
        'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'html', 'css',
        'machine learning', 'data science', 'aws', 'docker', 'kubernetes',
        'git', 'github', 'agile', 'scrum', 'tensorflow', 'pytorch',
        'excel', 'powerbi', 'tableau', 'mongodb', 'postgresql'
    ]
    
    found_skills = []
    for skill in skill_keywords:
        if skill in text_lower:
            found_skills.append(skill.title())
    
    result["skills"] = list(set(found_skills))  # Remove duplicates
    
    # Extract education (basic pattern matching)
    education_keywords = ['university', 'college', 'bachelor', 'master', 'phd', 'degree', 'diploma']
    education_lines = []
    
    for line in lines:
        if any(keyword in line.lower() for keyword in education_keywords):
            education_lines.append(line.strip())
    
    if education_lines:
        result["education"] = [{"raw_text": line} for line in education_lines[:3]]
    
    # Extract experience (look for company/date patterns)
    experience_patterns = [
        r'\b(19|20)\d{2}\s*[-–—]\s*(19|20)\d{2}|\b(19|20)\d{2}\s*[-–—]\s*present',
        r'\b\w+\s+\d{4}\s*[-–—]\s*\w+\s+\d{4}',
    ]
    
    experience_lines = []
    for line in lines:
        for pattern in experience_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                experience_lines.append(line.strip())
                break
    
    if experience_lines:
        result["experience"] = [{"raw_text": line} for line in experience_lines[:5]]
    
    return result

def format_offline_results(parsed_data):
    """Format offline parsing results for display"""
    
    import streamlit as st
    
    st.warning("⚠️ Using Offline Parser (OpenAI quota insufficient)")
    st.info("💡 This is a basic text extraction. For AI-powered parsing, please add credits to your OpenAI account.")
    
    # Display extracted information
    if parsed_data.get("name"):
        st.subheader(f"👤 {parsed_data['name']}")
    
    # Contact info
    col1, col2 = st.columns(2)
    with col1:
        if parsed_data.get("email"):
            st.write(f"📧 **Email:** {parsed_data['email']}")
    with col2:
        if parsed_data.get("phone"):
            st.write(f"📱 **Phone:** {parsed_data['phone']}")
    
    # Skills
    if parsed_data.get("skills"):
        st.subheader("🛠️ Detected Skills")
        st.write(", ".join(parsed_data["skills"]))
    
    # Education
    if parsed_data.get("education"):
        st.subheader("🎓 Education (Raw Extraction)")
        for edu in parsed_data["education"]:
            st.write(f"• {edu.get('raw_text', 'N/A')}")
    
    # Experience
    if parsed_data.get("experience"):
        st.subheader("💼 Experience (Raw Extraction)")
        for exp in parsed_data["experience"]:
            st.write(f"• {exp.get('raw_text', 'N/A')}")
    
    # Parsing info
    st.markdown("---")
    st.caption(f"Parsing Method: {parsed_data.get('parsing_method', 'unknown')} | "
               f"Time: {parsed_data.get('timestamp', 'unknown')}")
    
    return parsed_data