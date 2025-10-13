import streamlit as st
import os
from utils.pdf_parser import extract_text_from_pdf
from utils.llm_parser import parse_resume_text, format_resume_display
from utils.ollama_parser import integrate_ollama_parser, OllamaParser
from utils.rag_retriever import create_ollama_rag_interface, display_ollama_resume_insights

# Page configuration
st.set_page_config(
    page_title="Resume Parser LLM",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

def main():
    # Header
    st.title("📄 Resume Parser using Local & Cloud AI")
    st.markdown("Upload a resume PDF and get structured information extracted using AI - Choose between local Ollama or cloud services")
    
    # Sidebar
    with st.sidebar:
        # AI Service Selection
        st.header("🤖 Choose AI Service")
        
        ai_service = st.radio(
            "Select parsing method:",
            [
                "🦙 Ollama (Local AI - FREE)",
                "🔑 Cloud APIs (OpenAI, Gemini, etc.)",
                "📄 Offline Parser (Basic text extraction)"
            ],
            help="Choose your preferred AI service for resume parsing"
        )
        
        # Initialize selected service
        if ai_service.startswith("🦙"):
            ollama_ready = integrate_ollama_parser()
            if not ollama_ready:
                st.error("⚠️ Ollama not ready. Please follow setup instructions above.")
        else:
            # Show other AI service status for cloud APIs
            from utils.llm_parser import show_ai_service_status
            show_ai_service_status()
            
            # Setup instructions for free cloud AI services
            try:
                from utils.gemini_parser import setup_gemini_instructions
                setup_gemini_instructions()
            except ImportError:
                pass
                
            try:
                from utils.huggingface_parser import setup_huggingface_instructions  
                setup_huggingface_instructions()
            except ImportError:
                pass
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("📁 Upload Resume")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file", 
            type=["pdf"],
            help="Upload a resume in PDF format"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Display file info
            file_size = uploaded_file.size / 1024  # KB
            st.write(f"**File size:** {file_size:.1f} KB")
            
            # Extract and parse button
            if st.button("🚀 Extract & Parse Resume", type="primary"):
                with st.spinner("Processing resume..."):
                    # Step 1: Extract text from PDF (supports multi-page)
                    with st.status("Extracting text from PDF...", expanded=False) as status:
                        combined_text, pages = extract_text_from_pdf(uploaded_file)
                        if combined_text or (pages and len(pages) > 0):
                            st.write(f"✅ Extracted {len(combined_text)} characters from {len(pages)} page(s)")
                            status.update(label="Text extraction complete!", state="complete")
                        else:
                            st.error("Failed to extract text from PDF")
                            return
                    
                    # Step 2: Parse based on selected AI service
                    with st.status("Parsing with AI...", expanded=False) as status:
                        
                        if ai_service.startswith("🦙 Ollama") and 'ollama_parser' in st.session_state:
                            # Use Ollama local AI
                            st.info(f"🦙 Using Ollama model: {st.session_state.ollama_model}")
                            parser = st.session_state.ollama_parser
                            parsed_data = parser.parse_resume(combined_text, st.session_state.ollama_model)
                            
                            if "error" in parsed_data and parsed_data.get("setup_required"):
                                st.error("Please install an Ollama model first. See sidebar for instructions.")
                                return
                                
                        elif ai_service.startswith("🔑 Cloud APIs"):
                            # Use cloud APIs (existing functionality)
                            parsed_data = parse_resume_text(combined_text)
                            
                        else:
                            # Use offline parser
                            from utils.offline_parser import parse_resume_offline
                            parsed_data = parse_resume_offline(combined_text)
                        
                        status.update(label="AI parsing complete!", state="complete")
                    
                    # Store results in session state
                    st.session_state.parsed_data = parsed_data
                    st.session_state.raw_text = combined_text
                    st.session_state.pages = pages
                    st.session_state.ai_service_used = ai_service
    
    with col2:
        st.header("📊 Parsed Information")
        
        if 'parsed_data' in st.session_state:
            # Display results
            format_resume_display(st.session_state.parsed_data)
            
            # Raw text section (expandable)
            with st.expander("📝 View Raw Extracted Text"):
                pages = st.session_state.get('pages', [])
                if pages:
                    page_index = st.selectbox("Select page to view:", list(range(1, len(pages) + 1)))
                    st.text_area(
                        f"Raw text - Page {page_index}",
                        value=pages[page_index - 1] or "",
                        height=300,
                        disabled=True
                    )
                    if st.checkbox("Show combined text", value=False):
                        st.text_area(
                            "Combined text:",
                            value=st.session_state.raw_text,
                            height=300,
                            disabled=True
                        )
                else:
                    st.text_area(
                        "Raw text from PDF:",
                        value=st.session_state.raw_text,
                        height=300,
                        disabled=True
                    )
            
            # Download structured data
            st.download_button(
                label="💾 Download Parsed Data (JSON)",
                data=str(st.session_state.parsed_data),
                file_name=f"parsed_resume_{uploaded_file.name.replace('.pdf', '.json')}",
                mime="application/json"
            )
            
            # If using Ollama, show advanced Q&A section
            if (st.session_state.get('ai_service_used', '').startswith("🦙 Ollama") and 
                'ollama_rag' in st.session_state):
                
                st.divider()
                st.header("💬 Advanced Resume Analysis")
                st.write("Ask detailed questions about the resume using local AI.")
                
                # Question input
                question = st.text_area(
                    "Enter your question:",
                    placeholder="e.g., What are the candidate's key strengths? How many years of Python experience do they have? What makes this candidate suitable for a senior developer role?",
                    height=80
                )
                
                if st.button("🤖 Get AI Analysis", type="secondary"):
                    if question:
                        with st.spinner("Generating AI analysis..."):
                            try:
                                response = st.session_state.ollama_rag.answer_question(
                                    question, st.session_state.raw_text
                                )
                                st.success("**AI Analysis:**")
                                st.write(response)
                            except Exception as e:
                                st.error(f"Error generating response: {str(e)}")
                    else:
                        st.warning("Please enter a question.")
        else:
            st.info("👆 Upload a resume PDF to see parsed information here")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ using Streamlit • Supports Local Ollama AI, Cloud APIs & Offline Parsing | "
        "[View Source Code](https://github.com/your-repo)"
    )

if __name__ == "__main__":
    # Load custom CSS if available
    if os.path.exists("assets/style.css"):
        load_css()
    
    main()