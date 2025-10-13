# 📄 Resume Parser LLM

An intelligent resume parsing application that extracts structured information from PDF resumes using OpenAI's GPT-4 and Streamlit.

## ✨ Features

- **PDF Text Extraction**: Extract text from uploaded PDF resumes
- **AI-Powered Parsing**: Use GPT-4 to structure resume information
- **Interactive UI**: Clean, user-friendly Streamlit interface
- **Structured Output**: Get organized data (contact info, education, experience, skills, projects)
- **Advanced Q&A**: Ask questions about resumes using RAG (Retrieval Augmented Generation)
- **Resume Insights**: Generate AI-powered insights about candidates

## 🏗️ Project Structure

```
Resume_Parser_LLM/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── .env.example          # Environment variables template
├── # 📄 Resume Parser with Local & Cloud AI

A comprehensive resume parsing application that extracts structured information from PDF resumes using multiple AI providers including **local Ollama models**, cloud APIs, and offline parsing.

## 🌟 Features

- **🦙 Local AI Processing**: Use Ollama models for complete offline processing
- **☁️ Cloud AI Support**: OpenAI GPT-4, Google Gemini, HuggingFace models
- **📄 Offline Parsing**: Basic text extraction when no AI is available
- **🤖 Advanced Q&A**: Ask detailed questions about resumes using local RAG
- **📊 Structured Output**: Extract name, contact, experience, education, skills, projects
- **💾 Export Options**: Download parsed data as JSON
- **🔒 Privacy Focused**: Local processing keeps sensitive data on your machine

## 🚀 Quick Start

### Option 1: Local AI with Ollama (Recommended)

1. **Install Ollama**
   ```bash
   # Download from https://ollama.ai/download
   # Or via homebrew on macOS:
   brew install ollama
   ```

2. **Pull a model**
   ```bash
   ollama pull llama3.2:3b  # Lightweight model (2GB)
   # or
   ollama pull llama3.1:8b  # More capable model (4.7GB)
   ```

3. **Clone and setup**
   ```bash
   git clone <your-repo-url>
   cd Resume_Parser_LLM
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Test your setup**
   ```bash
   python test_setup.py
   ```

### Option 2: Cloud APIs

1. **Setup API keys** (create `.env` file):
   ```env
   OPENAI_API_KEY=your_openai_key
   GOOGLE_API_KEY=your_gemini_key
   HUGGINGFACE_API_TOKEN=your_hf_token
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run**
   ```bash
   streamlit run app.py
   ```

## 📋 Requirements

### Core Dependencies
```
streamlit>=1.28.0
PyMuPDF>=1.23.0
requests>=2.25.0
```

### For Local AI (Ollama)
```
sentence-transformers>=2.2.0
scikit-learn>=1.3.0
numpy>=1.21.0
```

### For Cloud APIs
```
openai>=1.0.0
google-generativeai>=0.3.0
```

## 🔧 Project Structure

```
Resume_Parser_LLM/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── test_setup.py         # Setup verification script
├── utils/
│   ├── pdf_parser.py     # PDF text extraction
│   ├── ollama_parser.py  # Local Ollama integration
│   ├── rag_retriever.py  # Advanced Q&A system
│   ├── llm_parser.py     # Multi-provider orchestration
│   ├── gemini_parser.py  # Google Gemini integration
│   ├── huggingface_parser.py  # HF models
│   └── offline_parser.py # Text-based fallback
├── data/
│   └── sample_resumes/   # Sample PDFs for testing
└── assets/
    └── style.css         # Custom styling
```

## 🎯 Usage Guide

### 1. Choose AI Service
- **🦙 Ollama (Local)**: Complete privacy, no API costs, requires setup
- **🔑 Cloud APIs**: High accuracy, requires API keys and internet
- **📄 Offline Parser**: Basic extraction, works without AI

### 2. Upload Resume
- Drag and drop PDF files
- Supports multi-page resumes
- Automatic text extraction

### 3. Parse and Analyze
- View structured information
- Download JSON data
- Ask questions with AI Q&A (Ollama only)

## 🔍 Advanced Features

### Local RAG System
When using Ollama, you get access to an advanced Q&A system:

```python
# Example questions you can ask:
"What are the candidate's key strengths?"
"How many years of Python experience do they have?"
"What makes this candidate suitable for a senior role?"
"Summarize their technical skills"
```

### Multi-Provider Fallback
The system automatically tries different AI providers:
1. Primary choice (Ollama/OpenAI/Gemini)
2. Secondary fallback options
3. Offline parsing as last resort

## 🛠️ Development

### Setup Development Environment
```bash
git clone <repo-url>
cd Resume_Parser_LLM
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Run Tests
```bash
python test_setup.py      # Test all components
streamlit run app.py      # Start development server
```

### Add New AI Provider
1. Create parser in `utils/your_provider_parser.py`
2. Implement `parse_resume(text)` function
3. Add to `llm_parser.py` provider list
4. Update `app.py` UI options

## 🔒 Privacy & Security

### Local Processing Benefits
- **No Data Transmission**: Resumes never leave your machine
- **No API Costs**: Free local processing with Ollama
- **Full Control**: Choose your preferred AI model
- **Offline Capable**: Works without internet connection

### Data Handling
- Temporary file processing only
- No permanent storage of sensitive data
- Optional export for user convenience

## 📚 Supported Models

### Ollama Models (Local)
- `llama3.2:3b` - Fast, lightweight (2GB)
- `llama3.1:8b` - Balanced performance (4.7GB)
- `llama3.1:70b` - Highest quality (40GB+)
- `mistral:7b` - Alternative option (4.1GB)

### Cloud Models
- OpenAI: GPT-4, GPT-3.5-turbo
- Google: Gemini Pro, Gemini Pro Vision
- HuggingFace: Various open-source models

## 🐛 Troubleshooting

### Ollama Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama service
ollama serve

# Pull a different model
ollama pull llama3.2:3b
```

### Common Errors
- **"Ollama not found"**: Install from https://ollama.ai/download
- **"No models available"**: Run `ollama pull llama3.2:3b`
- **"Connection refused"**: Start Ollama service
- **"Requirements missing"**: Run `pip install -r requirements.txt`

### Performance Tips
- Use smaller models (3b) for faster inference
- Enable GPU acceleration if available
- Close other applications to free memory

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for local AI inference
- [Streamlit](https://streamlit.io/) for the web framework
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing
- [sentence-transformers](https://www.sbert.net/) for embeddings

---

Built with ❤️ using Streamlit • Supports Local Ollama AI, Cloud APIs & Offline Parsing             # Project documentation
├── utils/
│   ├── __init__.py
│   ├── pdf_parser.py     # PDF text extraction
│   ├── llm_parser.py     # OpenAI integration & parsing
│   └── rag_retriever.py  # Advanced RAG functionality
├── assets/
│   └── style.css         # Custom Streamlit styling
├── data/
│   └── sample_resumes/   # Sample resumes for testing
└── uploads/              # Temporary file storage
```

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Resume_Parser_LLM
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_actual_api_key_here
```

### 4. Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📋 Usage

1. **Upload Resume**: Click "Choose a PDF file" to upload a resume
2. **Extract & Parse**: Click the "🚀 Extract & Parse Resume" button
3. **View Results**: See structured information displayed in an organized format
4. **Advanced Features**: 
   - Use the Q&A system to ask specific questions about the resume
   - Generate AI insights for deeper analysis
   - Download parsed data as JSON

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_ORG_ID`: OpenAI organization ID (optional)
- `OPENAI_MODEL`: Model to use (default: gpt-4-turbo)

### Customization
- Modify `assets/style.css` for custom styling
- Update parsing prompts in `utils/llm_parser.py`
- Add new features in the main `app.py` file

## 📦 Dependencies

- **Streamlit**: Web application framework
- **OpenAI**: GPT-4 API for text parsing
- **PyMuPDF**: PDF text extraction
- **LangChain**: Advanced RAG functionality (optional)
- **FAISS**: Vector similarity search
- **python-dotenv**: Environment variable management

## 🎯 Supported Resume Information

The parser extracts:
- **Personal Info**: Name, email, phone number
- **Education**: Degrees, institutions, graduation years, GPA
- **Experience**: Companies, roles, durations, descriptions
- **Skills**: Technical and soft skills
- **Projects**: Project names, descriptions, technologies
- **Certifications**: Professional certifications

## 🔍 Advanced Features

### RAG Q&A System
Ask natural language questions about resumes:
- "What programming languages does this candidate know?"
- "How many years of experience do they have?"
- "What are their key achievements?"

### AI Insights
Generate comprehensive insights:
- Experience summary and progression
- Skill analysis and recommendations
- Education relevance assessment
- Candidate strengths identification

## 🚨 Troubleshooting

### Common Issues

1. **Missing API Key Error**
   - Ensure you've created a `.env` file with your OpenAI API key
   - Check that the key is valid and has sufficient credits

2. **PDF Extraction Issues**
   - Ensure the PDF is not password-protected
   - Try with different PDF files to isolate the issue

3. **Import Errors**
   - Run `pip install -r requirements.txt` to ensure all dependencies are installed
   - Consider using a virtual environment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4 API
- Streamlit team for the amazing web framework
- PyMuPDF developers for PDF processing capabilities

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Open an issue on GitHub
3. Contact the maintainer

---

Built with ❤️ using Streamlit and OpenAI GPT-4