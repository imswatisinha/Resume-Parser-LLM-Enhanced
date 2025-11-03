# 📄 AI Document Processing Assistant

## 🎯 Overview
A simplified document processing application that uses:
- **Ollama/Llama** for local AI processing
- **Pinecone** for vector storage and retrieval  
- **Streamlit** for clean, intuitive interface

## ✨ Features
- **Simple Upload**: Just drag & drop documents (PDF, DOCX, TXT)
- **Smart Processing**: Automatic chunking and embedding generation
- **Ask Questions**: Natural language Q&A about your documents
- **Persistent Storage**: Documents stored in Pinecone cloud database
- **No API Keys Required from Users**: Configure once in .env file

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Ollama
```bash
# Install and start Ollama
ollama serve

# Pull the required model
ollama pull llama3.2:3b
```

### 3. Configure Environment
Update `.env` file with your Pinecone API key:
```env
PINECONE_API_KEY=your_actual_api_key_here
```
Get your free API key at [pinecone.io](https://pinecone.io)

### 4. Run the App
```bash
streamlit run app.py
```

## 🎮 Usage

### Upload Documents
1. Go to the **"📤 Upload Documents"** tab
2. Drag & drop or browse for your files
3. Click **"🔄 Process Documents"**

### Ask Questions  
1. Go to the **"❓ Ask Questions"** tab
2. Type your question about the uploaded documents
3. Get AI-powered answers with source references

## 🔧 Configuration

The app automatically loads settings from `.env`:
- `PINECONE_API_KEY`: Your Pinecone API key (required)
- `PINECONE_ENVIRONMENT`: Pinecone region (default: us-east-1) 
- `PINECONE_INDEX_NAME`: Index name (default: ai-documents)
- `OLLAMA_MODEL`: AI model (default: llama3.2:3b)

## 🆘 Troubleshooting

**"Pinecone API key not configured"**
- Update your `.env` file with a valid Pinecone API key

**"Ollama connection failed"**
- Make sure Ollama is running: `ollama serve`
- Check if the model is available: `ollama list`

**App won't start**
- Check all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version compatibility (3.8+)

## 📁 Project Structure
```
├── app.py                 # Main Streamlit application
├── utils/
│   ├── pinecone_vector_store.py    # Pinecone integration
│   ├── document_chunker.py         # Document processing  
│   └── llm_parser.py              # Ollama integration
├── .env                   # Environment configuration
└── requirements.txt       # Python dependencies
```

## 🔒 Privacy & Benefits
- **Local AI Processing**: Your documents never leave your machine for AI processing
- **Persistent Storage**: Store documents in Pinecone for long-term access
- **No Repeated Setup**: Configure API key once, use seamlessly
- **Cost Effective**: Only pay for Pinecone storage, Ollama is free

---
🎉 **Ready to process documents with AI!**