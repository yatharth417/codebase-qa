# Codebase Q&A with Proof

A RAG-based web application that allows you to upload codebases (ZIP or GitHub) and ask questions about them. Get intelligent answers with source attribution - every answer includes file paths and actual code snippets as proof.

## 🚀 Live Demo

**[Live App on Railway](https://web-production-9a70b.up.railway.app/)** ← Replace with your actual Railway URL

## ✨ Features

- **Multiple Upload Options**: Upload ZIP files or clone from GitHub URLs
- **Smart Code Indexing**: Automatic parsing, chunking, and vector storage
- **Intelligent Q&A**: Ask natural language questions about your codebase
- **Source Attribution**: Every answer includes file paths and code snippets as proof
- **Service Health Monitoring**: Real-time status of LLM, Embeddings, and Vector Database
- **Chat History**: Saves last 10 Q&A pairs in session
- **Multi-Language Support**: Python, JavaScript, TypeScript, Java, C++, Go, Rust, PHP, and more

## 🏗️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: Groq (Llama 3.3 70B Versatile)
- **Embeddings**: Google Generative AI (models/gemini-embedding-001)
- **Vector Database**: Chroma (local persistence)
- **Orchestration**: LangChain
- **Text Processing**: RecursiveCharacterTextSplitter

## 🎯 Why These Technologies?

### Groq (LLM)
- ⚡ **Speed**: ~300 tokens/sec inference
- 💰 **Cost**: Free tier with 14,400 requests/day
- 🎯 **Quality**: Llama 3.3 70B excellent for code understanding
- 🔒 **Reliability**: Stable API with good uptime

### Google Generative AI (Embeddings)
- 🎯 **Quality**: 768-dimensional embeddings
- 💰 **Cost**: Free tier with 1500 requests/day
- 🔗 **Integration**: Native LangChain support

### Chroma (Vector DB)
- 🚀 **Simplicity**: No external service needed
- 💾 **Persistence**: Local file storage
- 🔗 **Compatibility**: Built-in LangChain integration
- 💰 **Cost**: Completely free

## 📋 Requirements

- Python 3.11
- API Keys:
  - [Groq API Key](https://console.groq.com/keys)
  - [Google API Key](https://aistudio.google.com/apikey)

## 🛠️ Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yatharth417/codebase-qa.git
cd codebase-qa
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📖 How to Use

### Step 1: Check Service Status
Open the app and verify all services show 🟢 Connected in the sidebar:
- LLM (Groq)
- Embeddings (Google Gemini)
- Vector DB (Chroma)

### Step 2: Upload & Index Your Codebase

**Option A: Upload ZIP**
1. Navigate to "Upload & Index" tab
2. Choose a ZIP file (max 100MB)
3. Click "Index from ZIP"
4. Wait for indexing to complete

**Option B: GitHub URL**
1. Navigate to "Upload & Index" tab
2. Enter GitHub repository URL
3. Click "Index from GitHub"
4. Wait for cloning and indexing

### Step 3: Ask Questions

1. Go to "Ask Questions" tab
2. Type your question in the chat input
3. View answer with source attribution
4. Expand "View sources" to see actual code snippets

## 💬 Example Questions

```
"Where is authentication handled?"
"How do retries work in this codebase?"
"Explain the database connection logic"
"What API endpoints are defined?"
"Show me the error handling implementation"
"How is user data validated?"
"Where are environment variables used?"
```

## 🔧 Configuration

### Limits (configured in `app.py`)

```python
MAX_CODEBASE_SIZE_MB = 100   # Maximum codebase size
MAX_FILES = 50                # Maximum files to index
MAX_FILE_SIZE_MB = 0.5        # Maximum individual file size
```

### Supported File Types

`.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.java`, `.cpp`, `.c`, `.h`, `.cs`, `.rb`, `.go`, `.rs`, `.php`, `.md`, `.txt`, `.json`, `.yaml`, `.yml`

### Ignored Directories

`node_modules`, `.git`, `__pycache__`, `venv`, `env`, `.next`, `dist`, `build`

## 🏆 Features Implemented

✅ ZIP file upload  
✅ GitHub repository cloning  
✅ Automatic code indexing with progress tracking  
✅ RAG-based Q&A with source retrieval  
✅ Source attribution (file paths + code snippets)  
✅ Real-time service health monitoring  
✅ Session-based chat history (last 10 Q&As)  
✅ Multi-language code support (15+ languages)  
✅ Error handling for edge cases  
✅ File size and count limits  

## 📁 Project Structure

```
codebase-qa/
├── app.py                   # Main Streamlit application
├── requirements.txt         # Python dependencies
├── runtime.txt             # Python version specification
├── Procfile                # Deployment configuration
├── railway.json            # Railway-specific settings
├── .env                    # Environment variables (not committed)
├── .gitignore             # Git ignore rules
├── chroma_db/             # Vector database storage
├── README.md              # This file
├── AI_NOTES.md           # AI development documentation
├── ABOUTME.md            # Developer information
└── PROMPTS_USED.md       # Development prompts log
```

## 🔒 Security

- ✅ No API keys in code
- ✅ `.env` file excluded from git
- ✅ Input validation for uploads
- ✅ File type restrictions
- ✅ Size limits enforced

## 🧪 Testing

Tested scenarios:
- ✅ ZIP upload with various codebases
- ✅ GitHub cloning with public repositories
- ✅ Q&A with different question types
- ✅ Source snippet display accuracy
- ✅ Service health indicators
- ✅ Error handling for invalid inputs

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Groq](https://groq.com/)
- Embeddings by [Google Generative AI](https://ai.google.dev/)
- Vector storage by [Chroma](https://www.trychroma.com/)
- Orchestrated with [LangChain](https://www.langchain.com/)

## 👤 Developer

See [ABOUTME.md](ABOUTME.md) for developer information.

## 📄 License

MIT License

---

**Built as part of a technical assessment - February 2026**
