# 🤖 Resume Parser LLM - Enhanced Edition

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-green.svg)](https://ollama.ai)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> **Privacy-First AI Resume Parser** with intelligent model selection, modular architecture, and local LLM processing. Transform resumes into structured data without compromising privacy or breaking the bank.

## 🎯 What Makes This Special?

### **🔒 Privacy-First Architecture**
- **100% Local Processing**: Your resumes never leave your machine
- **No Cloud APIs**: Zero data transmitted to external services
- **Secure by Design**: Proper secret management and input validation

### **🧠 Intelligent AI Processing** 
- **Multi-Model Support**: Llama3.2, Phi3, Gemma2, Llama3.1
- **Smart Model Selection**: Automatically chooses optimal model based on document complexity
- **Fallback Mechanisms**: Graceful handling of memory constraints and errors

### **🏗️ Production-Ready Architecture**
- **Modular Services**: 13+ specialized services with clear responsibilities
- **Type Safety**: Pydantic models with comprehensive validation
- **Comprehensive Logging**: Structured logging with performance monitoring
- **Error Handling**: User-friendly error messages with actionable suggestions

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+ installed
- Git for cloning the repository

### **1. Clone & Setup**
```bash
git clone https://github.com/imswatisinha/Resume-Parser-LLM-Enhanced.git
cd Resume-Parser-LLM-Enhanced
pip install -r requirements.txt
```

### **2. Install & Configure Ollama**
```bash
# Install Ollama (visit ollama.ai for platform-specific instructions)
# Then pull the AI models:
ollama pull llama3.2:3b
ollama pull phi3:mini
ollama pull gemma2:2b

# Start Ollama service
ollama serve
```

### **3. Configure Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings (Pinecone API key optional)
# PINECONE_API_KEY=your_key_here  # Optional for vector storage
```

### **4. Run the Application**
```bash
# Use the convenient batch script (Windows)
./run_app.bat

# Or run directly
streamlit run app_new.py
```

### **5. Start Parsing! 🎉**
- Open http://localhost:8501
- Upload a resume (PDF, DOCX, TXT)
- Watch AI intelligently process and structure the data
- Export results or ask questions about the content

---

## 📋 Features Overview

### **🤖 AI-Powered Extraction**
- **Contact Information**: Names, emails, phone numbers, addresses
- **Professional Experience**: Job titles, companies, dates, descriptions  
- **Education**: Degrees, institutions, graduation dates, GPAs
- **Skills & Technologies**: Programming languages, frameworks, tools
- **Projects & Achievements**: Personal projects, awards, certifications

### **📊 Intelligent Processing**
- **Document Complexity Analysis**: Automatic assessment of document structure
- **Model Optimization**: Chooses fastest model capable of handling the document
- **Memory Management**: Intelligent handling of large documents
- **Progress Tracking**: Real-time feedback during processing

### **🔍 Advanced Capabilities**
- **Vector Embeddings**: Semantic search and similarity matching
- **RAG Integration**: Ask questions about processed resumes
- **Batch Processing**: Handle multiple documents efficiently
- **Export Options**: JSON, CSV, structured formats

---

## 🏗️ Architecture Deep Dive

### **Service-Oriented Design**
```
📁 config/                 # Type-safe configuration management
├── settings.py            # Environment-specific configurations

📁 core/                   # Core infrastructure services  
├── exceptions.py          # Custom exception hierarchy
├── logging_system.py      # Structured logging & monitoring
└── security.py           # Security management & validation

📁 services/               # Business logic services
├── model_service.py       # AI model selection & management
├── parsing_service.py     # Resume parsing coordination
├── document_service.py    # Document processing & extraction
├── rag_service.py         # Vector operations & similarity search
└── orchestrator.py        # Workflow coordination

📁 models/                 # Data models & validation
└── domain_models.py       # Pydantic models with validation

📁 ui/                     # User interface services
└── ui_service.py          # Streamlit component management
```

### **Technology Stack**

| Component | Technology | Why This Choice |
|-----------|------------|-----------------|
| **Frontend** | Streamlit | Python-native, ML-optimized widgets, rapid development |
| **AI Engine** | Ollama + Local LLMs | Privacy-first, cost-effective, offline capability |
| **Document Processing** | PyMuPDF | Fastest PDF processing, excellent text extraction |
| **Vector Storage** | Pinecone | Managed scaling, sub-millisecond search |
| **Embeddings** | Sentence-Transformers | Specialized for document similarity |
| **Validation** | Pydantic | Runtime validation, automatic serialization |
| **Configuration** | Python-dotenv | Secure environment management |

---

## 📊 Performance & Scalability

### **Model Selection Intelligence**
```python
# Automatic model selection based on document characteristics
Document Size < 2K chars     → phi3:mini      (fastest)
Document Size 2K-10K chars   → llama3.2:3b   (balanced)
Document Size > 10K chars    → llama3.1:8b   (highest quality)
Technical Content Detected   → llama3.1:8b   (specialized)
```

### **Performance Benchmarks**
- **Small Resume (1-2 pages)**: ~5-15 seconds
- **Large Resume (3+ pages)**: ~15-45 seconds  
- **Technical Resume**: ~10-30 seconds
- **Batch Processing**: ~2-5 resumes per minute

### **Resource Requirements**
- **RAM**: 4GB minimum, 8GB+ recommended
- **Storage**: 2GB for models, 1GB for application
- **CPU**: Modern multi-core processor recommended

---

## 🔧 Configuration & Customization

### **Environment Variables**
```bash
# Core AI Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=30
OLLAMA_DEFAULT_MODEL=llama3.2:3b

# Vector Storage (Optional)
PINECONE_API_KEY=your_key_here
PINECONE_ENVIRONMENT=us-west1-gcp  
PINECONE_INDEX_NAME=resume-parser

# Processing Configuration
CHUNK_SIZE=500
CHUNK_OVERLAP=50
SIMILARITY_THRESHOLD=0.7
MAX_RESULTS=5

# UI Configuration
STREAMLIT_THEME=light
ENABLE_EXPANDERS=true
SHOW_DETAILED_ANALYSIS=true
```

---

## 🛠️ Troubleshooting

### **Common Issues**

#### **"Ollama not available"**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# Start Ollama service
ollama serve

# Verify models are installed
ollama list
```

#### **"torch dependency error"**
```bash
# Use the provided fix
export STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
streamlit run app_new.py --server.fileWatcherType=none

# Or use the batch script
./run_app.bat
```

#### **"Pinecone API key not configured"**
```bash
# Pinecone is optional - you can run without it
# For full vector search capabilities, get a free API key at pinecone.io
echo "PINECONE_API_KEY=your_key_here" >> .env
```

---

## 📚 Documentation

### **Comprehensive Guides**
- 📖 [**Technology Analysis**](TECHNOLOGY_ANALYSIS.md) - Deep dive into technology choices
- 📊 [**Project Analysis**](PROJECT_ANALYSIS_SUMMARY.md) - Complete project overview
- 🏗️ [**Architecture Guide**](CODEBASE_COMPLEXITY_ANALYSIS.md) - Technical architecture details
- 🔒 [**Security Report**](SECURITY_INCIDENT_REPORT.md) - Security improvements and best practices
- ⚡ [**Performance Tips**](PERFORMANCE_TIPS.md) - Optimization strategies
- 🔧 [**Setup Guides**](PINECONE_SETUP.md) - Detailed setup instructions

---

## 🔮 Roadmap & Future Enhancements

### **Next Release (v2.0)**
- 🚀 **FastAPI Backend**: RESTful API for integration
- 📱 **Mobile App**: React Native/Flutter mobile interface  
- 🔄 **Real-time Processing**: WebSocket-based live updates
- 📊 **Analytics Dashboard**: Processing metrics and insights

### **Future Versions**
- 🤖 **Custom Model Training**: Fine-tune models for specific industries
- 🌐 **Multi-language Support**: Process resumes in multiple languages
- 🔗 **ATS Integration**: Direct integration with Applicant Tracking Systems
- 🧪 **A/B Testing**: Compare parsing accuracy across models

---

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for details.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**🎉 Transform Your Resume Processing Today! 🎉**

**Privacy-First • Cost-Effective • Production-Ready**

[🚀 Get Started](#-quick-start) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>