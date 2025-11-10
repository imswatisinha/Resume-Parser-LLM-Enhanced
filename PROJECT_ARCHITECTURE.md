# 🏗️ Resume Parser LLM - Complete System Architecture

## 📋 High-Level Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           RESUME PARSER LLM SYSTEM                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐             │
│  │   FRONTEND      │    │   PROCESSING    │    │   AI ENGINE     │             │
│  │   (Streamlit)   │◄──►│   PIPELINE      │◄──►│   (Ollama)      │             │
│  │                 │    │                 │    │                 │             │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘             │
│           │                       │                       │                     │
│           │                       ▼                       │                     │
│           │              ┌─────────────────┐              │                     │
│           │              │  VECTOR STORES  │              │                     │
│           │              │  Pinecone/Local │              │                     │
│           │              └─────────────────┘              │                     │
│           │                       │                       │                     │
│           └───────────────────────┼───────────────────────┘                     │
│                                   ▼                                             │
│                          ┌─────────────────┐                                   │
│                          │  CLASSIFICATION │                                   │
│                          │     ENGINE      │                                   │
│                          └─────────────────┘                                   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Layer-by-Layer Architecture Analysis

### **1. Presentation Layer (Frontend)**

```
┌─────────────────────────────────────────────┐
│              STREAMLIT UI LAYER             │
├─────────────────────────────────────────────┤
│                                             │
│  📱 app.py (Main Application)               │
│  ├── 🎨 CSS Styling (assets/style.css)     │
│  ├── 📊 Multi-column Layout                │
│  ├── 🔄 Real-time Progress Indicators       │
│  ├── 📤 File Upload Interface               │
│  └── 🎛️ Configuration Sidebar              │
│                                             │
│  Key Features:                              │
│  • Drag & Drop PDF Upload                  │
│  • Model Selection Interface               │
│  • Real-time Processing Status             │
│  • Interactive Results Display             │
│  • Error Handling & Recovery               │
└─────────────────────────────────────────────┘
```

**Technologies Used:**
- **Streamlit**: Web framework for rapid ML app development
- **HTML/CSS**: Custom styling for professional UI
- **Session State Management**: Maintains user data across interactions

---

### **2. Document Processing Pipeline**

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCUMENT PROCESSING LAYER                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📄 PDF Parser (utils/pdf_parser.py)                          │
│  ├── PyMuPDF (fitz) - High-performance PDF processing         │
│  ├── Multi-page text extraction                               │
│  ├── Layout preservation                                       │
│  └── Metadata extraction                                       │
│                                                                 │
│  🧩 Document Chunker (utils/document_chunker.py)              │
│  ├── Section-based chunking (Experience, Education, etc.)     │
│  ├── Sliding window chunking with overlap                     │
│  ├── Page-based chunking                                      │
│  └── Semantic boundary detection                              │
│                                                                 │
│  🔍 Keyword Classifier (utils/keyword_classifier.py)          │
│  ├── 500+ predefined keywords across 9 categories            │
│  ├── Pattern matching with confidence scoring                │
│  ├── Technology subcategory detection                        │
│  └── Industry classification                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow:**
```
PDF Upload → Text Extraction → Intelligent Chunking → Classification → AI Processing
```

---

### **3. AI Processing Engine**

```
┌─────────────────────────────────────────────────────────────────┐
│                       AI PROCESSING LAYER                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🦙 Ollama Integration (utils/ollama_parser.py)                │
│  ├── Local LLM Server Communication                           │
│  ├── Multiple Model Support                                   │
│  ├── Memory Management                                         │
│  └── Error Recovery & Fallback                                │
│                                                                 │
│  🧠 Intelligent Model Selection (utils/llm_parser.py)         │
│  ├── Document complexity analysis                             │
│  ├── System resource monitoring                               │
│  ├── Automatic model selection                                │
│  └── Progressive fallback system                              │
│                                                                 │
│  Model Hierarchy:                                              │
│  ┌─────────────┬─────────┬──────────┬─────────────┐            │
│  │   Model     │  Size   │   RAM    │    Use Case │            │
│  ├─────────────┼─────────┼──────────┼─────────────┤            │
│  │ gemma2:2b   │  1.6GB  │   3GB    │ Fast/Light  │            │
│  │ phi3:mini   │  2.2GB  │   6GB    │ Balanced    │            │
│  │ llama3.2:3b │  2.0GB  │   6GB    │ Quality     │            │
│  │ llama3.1:8b │  4.7GB  │  12GB    │ Complex     │            │
│  └─────────────┴─────────┴──────────┴─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

**Intelligence Features:**
- **Memory-Aware Selection**: Prevents system crashes
- **Automatic Fallback**: Tries smaller models if memory insufficient
- **Real-time Monitoring**: Tracks processing status and errors

---

### **4. Vector Database & RAG System**

```
┌─────────────────────────────────────────────────────────────────┐
│                    VECTOR STORAGE LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🌲 Pinecone Vector Store (utils/pinecone_vector_store.py)     │
│  ├── Cloud-based persistent storage                           │
│  ├── Serverless architecture                                  │
│  ├── Real-time vector indexing                                │
│  └── Scalable similarity search                               │
│                                                                 │
│  🧠 In-Memory Vector Store (utils/rag_retriever.py)           │
│  ├── Fast temporary storage                                   │
│  ├── Sentence transformers embeddings                        │
│  ├── Immediate availability                                   │
│  └── No external dependencies                                 │
│                                                                 │
│  📚 RAG Pipeline:                                              │
│  Document → Chunks → Embeddings → Vector Store → Similarity Search │
└─────────────────────────────────────────────────────────────────┘
```

**Dual Architecture Benefits:**
- **Development**: Fast in-memory processing
- **Production**: Persistent Pinecone storage
- **Hybrid**: Seamless switching based on needs

---

### **5. Data Processing Flow**

```
┌─────────────────────────────────────────────────────────────────┐
│                      DATA FLOW ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input: PDF Resume                                              │
│     │                                                           │
│     ▼                                                           │
│  📄 PDF Parser (PyMuPDF)                                       │
│     ├── Extract text per page                                  │
│     └── Combine into single document                           │
│     │                                                           │
│     ▼                                                           │
│  📊 Document Analysis                                           │
│     ├── Character count, complexity scoring                    │
│     ├── Content type detection (code, tables, etc.)           │
│     └── Technical term density                                 │
│     │                                                           │
│     ▼                                                           │
│  🧠 Intelligent Model Selection                                │
│     ├── Analyze system resources                               │
│     ├── Match document complexity to model capability          │
│     └── Select optimal model with memory safety               │
│     │                                                           │
│     ▼                                                           │
│  🧩 Document Chunking                                          │
│     ├── Section-based: Experience, Education, Skills          │
│     ├── Sliding window: Overlapping context preservation      │
│     └── Page-based: Maintain document structure               │
│     │                                                           │
│     ▼                                                           │
│  🤖 AI Processing (Ollama)                                     │
│     ├── JSON structure extraction                              │
│     ├── Field mapping and validation                          │
│     └── Error handling and recovery                           │
│     │                                                           │
│     ▼                                                           │
│  🔍 Enhanced Classification                                     │
│     ├── Keyword extraction (500+ terms)                       │
│     ├── Category scoring and confidence                       │
│     └── Technology subcategory detection                      │
│     │                                                           │
│     ▼                                                           │
│  📋 Structured JSON Output                                     │
│     ├── Personal information                                   │
│     ├── Experience with specific field structure              │
│     ├── Skills categorization                                 │
│     ├── Education details                                     │
│     ├── Classification tags and keywords                      │
│     └── Confidence metrics                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

### **6. Component Integration Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPONENT RELATIONSHIPS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  app.py (Main Orchestrator)                                    │
│     │                                                           │
│     ├── utils/pdf_parser.py ─────────► Text Extraction         │
│     │                                                           │
│     ├── utils/document_chunker.py ───► Intelligent Chunking    │
│     │                                                           │
│     ├── utils/llm_parser.py ────────► AI Processing Control    │
│     │    │                                                     │
│     │    └── utils/ollama_parser.py ──► Local LLM Integration  │
│     │                                                           │
│     ├── utils/keyword_classifier.py ─► Classification Engine   │
│     │                                                           │
│     ├── utils/rag_retriever.py ─────► Q&A and Retrieval       │
│     │                                                           │
│     └── utils/pinecone_vector_store.py ──► Persistent Storage  │
│                                                                 │
│  Configuration Files:                                           │
│     ├── requirements.txt ────────────► Dependency Management   │
│     ├── .env / .env.example ─────────► Environment Config     │
│     └── assets/style.css ────────────► UI Styling             │
└─────────────────────────────────────────────────────────────────┘
```

---

### **7. System States and Session Management**

```
┌─────────────────────────────────────────────────────────────────┐
│                     SESSION STATE MANAGEMENT                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Streamlit Session State Variables:                             │
│                                                                 │
│  🔧 System Configuration:                                       │
│     ├── ollama_parser: OllamaParser instance                  │
│     ├── ollama_model: Selected model name                     │
│     └── ollama_rag: RAG retriever instance                    │
│                                                                 │
│  📄 Document Data:                                              │
│     ├── parsed_data: AI-processed resume structure            │
│     ├── raw_text: Original extracted text                     │
│     ├── pages: Per-page text breakdown                        │
│     └── chunks: Document chunks for processing                │
│                                                                 │
│  🎛️ Processing Configuration:                                  │
│     ├── chunking_strategy: Selected chunking method           │
│     ├── vector_db_option: Storage choice (local/cloud)       │
│     └── pinecone_qa_ready: Q&A system status                 │
│                                                                 │
│  🔍 Analysis Results:                                           │
│     ├── classification_tags: Industry/role categories         │
│     ├── keywords_extracted: Skill and domain keywords         │
│     └── confidence_scores: Classification confidence          │
└─────────────────────────────────────────────────────────────────┘
```

---

### **8. Error Handling and Recovery Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                    ERROR HANDLING SYSTEM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🛡️ Multi-Level Error Protection:                              │
│                                                                 │
│  Level 1: Input Validation                                     │
│     ├── PDF file type verification                             │
│     ├── File size limits                                       │
│     └── Content validation                                     │
│                                                                 │
│  Level 2: Resource Management                                  │
│     ├── Memory usage monitoring                                │
│     ├── Model availability checking                            │
│     └── System resource validation                             │
│                                                                 │
│  Level 3: Processing Fallbacks                                │
│     ├── Automatic model downgrading on memory errors          │
│     ├── Progressive retry with smaller models                 │
│     └── Graceful degradation of features                      │
│                                                                 │
│  Level 4: User Experience                                      │
│     ├── Clear error messages with solutions                   │
│     ├── Recovery suggestions and quick fixes                  │
│     └── Progress tracking during recovery                     │
│                                                                 │
│  🔄 Recovery Mechanisms:                                        │
│     Memory Error → Fallback to smaller model                  │
│     Timeout Error → Suggest document splitting                │
│     Model Error → Try alternative model                       │
│     Network Error → Switch to local processing only           │
└─────────────────────────────────────────────────────────────────┘
```

---

### **9. Security and Privacy Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                     SECURITY ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🔒 Privacy-First Design:                                       │
│                                                                 │
│  Local Processing Layer:                                        │
│     ├── All AI processing happens locally via Ollama          │
│     ├── No data transmitted to external APIs                  │
│     ├── Complete control over data lifecycle                  │
│     └── GDPR/HIPAA compliance ready                           │
│                                                                 │
│  Data Protection:                                               │
│     ├── Temporary file cleanup after processing               │
│     ├── No persistent storage of sensitive data               │
│     ├── Environment variable encryption for API keys          │
│     └── Input sanitization and validation                     │
│                                                                 │
│  Access Control:                                                │
│     ├── File type restrictions (PDF only)                     │
│     ├── Size limitations to prevent DoS                       │
│     ├── Resource usage monitoring                             │
│     └── Error message sanitization                            │
│                                                                 │
│  Optional Cloud Integration:                                    │
│     ├── Pinecone: Only embeddings stored, not raw text       │
│     ├── Encrypted transmission for vector data                │
│     └── User-controlled cloud/local choice                    │
└─────────────────────────────────────────────────────────────────┘
```

---

### **10. Scalability and Deployment Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                   DEPLOYMENT ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🏠 Local Development:                                          │
│     ├── Virtual environment isolation                          │
│     ├── Local Ollama server                                   │
│     ├── In-memory vector processing                           │
│     └── Streamlit development server                          │
│                                                                 │
│  ☁️ Cloud Deployment Options:                                  │
│                                                                 │
│  Option 1: Streamlit Cloud                                     │
│     ├── Easy deployment with Git integration                  │
│     ├── Automatic scaling and SSL                             │
│     ├── Requires cloud-based Ollama alternative              │
│     └── Good for demos and prototypes                         │
│                                                                 │
│  Option 2: Docker Container                                    │
│     ├── Complete environment packaging                        │
│     ├── Ollama + Streamlit in single container               │
│     ├── Portable across cloud providers                      │
│     └── Scalable with container orchestration                │
│                                                                 │
│  Option 3: Enterprise Deployment                              │
│     ├── Kubernetes cluster with auto-scaling                 │
│     ├── Multiple Ollama instances for load balancing         │
│     ├── Separate vector database cluster                     │
│     └── Load balancer for high availability                  │
│                                                                 │
│  🔧 Infrastructure Requirements:                                │
│     Minimum: 4GB RAM, 2CPU, 10GB Storage                     │
│     Recommended: 8GB RAM, 4CPU, 20GB Storage                 │
│     Enterprise: 16GB+ RAM, 8CPU+, 100GB+ Storage             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 **Architecture Strengths**

### **1. Modular Design** 🧩
- Each component has single responsibility
- Easy to maintain and extend
- Components can be replaced independently
- Clean interfaces between layers

### **2. Intelligent Processing** 🧠
- Automatic model selection based on document complexity
- Memory-aware resource management
- Progressive fallback for reliability
- Real-time adaptation to system capabilities

### **3. Privacy-Focused** 🔒
- Local AI processing (no data leaves system)
- Optional cloud integration for scalability
- User-controlled privacy settings
- Compliance-ready architecture

### **4. Scalable Foundation** 📈
- Supports both local and cloud deployment
- Microservices-ready component structure
- Horizontal scaling capabilities
- Load balancing and high availability options

### **5. User Experience** ✨
- Real-time progress tracking
- Intelligent error recovery
- Clear feedback and guidance
- Professional, intuitive interface

This architecture represents a modern, privacy-first approach to AI-powered document processing, combining the latest advances in local LLM technology with robust engineering practices for reliability and scalability.