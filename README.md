# 🔍 Codebase Q&A with Proof

A RAG-powered web application that lets you upload a codebase and ask questions about it. Get answers with file paths, line references, and actual code snippets as proof.

## 🌟 Features

- **Upload Options**: Upload ZIP files or provide GitHub repository URLs
- **Smart Indexing**: Automatic code parsing, chunking, and vector storage
- **Intelligent Q&A**: Ask questions and get context-aware answers
- **Source Attribution**: Every answer includes file paths and code snippets
- **Chat History**: Last 10 Q&A pairs saved in session
- **Health Monitoring**: Real-time status of LLM, Embeddings, and Database
- **Safety Limits**: 
  - Max codebase size: 100MB
  - Max files: 1000
  - Max individual file size: 1MB

## 🛠️ Tech Stack

- **Frontend/Backend**: Streamlit
- **LLM**: Google Gemini Pro (via langchain-google-genai)
- **Vector Database**: Pinecone (serverless)
- **Orchestration**: LangChain
- **Embeddings**: Google Generative AI Embeddings (768 dimensions)

## 📋 Prerequisites

1. **Python 3.9+**
2. **Google Gemini API Key**: [Get it here](https://makersuite.google.com/app/apikey)
3. **Pinecone API Key**: [Get it here](https://app.pinecone.io/)
4. **Git** (for GitHub repository cloning)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd codebase-qa-app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
GOOGLE_API_KEY=your_google_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

### Step 1: Index Your Codebase

1. Go to the **"Upload & Index"** tab
2. Choose one of two options:
   - **Upload ZIP**: Select a ZIP file containing your code
   - **GitHub URL**: Paste a GitHub repository URL
3. Click the **"Index"** button
4. Wait for the indexing process to complete (you'll see progress indicators)

### Step 2: Ask Questions

1. Go to the **"Ask Questions"** tab
2. Type your question in the chat input
3. View the answer along with:
   - Direct answer from the AI
   - Source files used
   - Actual code snippets

### Example Questions

- "What does the authentication system do?"
- "How is error handling implemented?"
- "Explain the database connection setup"
- "What API endpoints are available?"
- "Show me how the payment processing works"

## 🎯 Supported File Types

- Python (`.py`)
- JavaScript (`.js`, `.jsx`)
- TypeScript (`.ts`, `.tsx`)
- Java (`.java`)
- C/C++ (`.c`, `.cpp`, `.h`)
- C# (`.cs`)
- Ruby (`.rb`)
- Go (`.go`)
- Rust (`.rs`)
- PHP (`.php`)
- Markdown (`.md`)
- Text (`.txt`)
- JSON (`.json`)
- YAML (`.yaml`, `.yml`)

## 🚫 Ignored Directories

The following directories are automatically skipped:
- `node_modules`
- `.git`
- `__pycache__`
- `venv`
- `env`
- `.next`
- `dist`
- `build`

## 🌐 Deployment

### Deploy to Render

1. **Create a Render account**: [render.com](https://render.com)

2. **Create a new Web Service**:
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

3. **Add Environment Variables**:
   - `GOOGLE_API_KEY`: Your Google Gemini API key
   - `PINECONE_API_KEY`: Your Pinecone API key

4. **Deploy**: Click "Create Web Service"

### Deploy to Railway

1. **Create a Railway account**: [railway.app](https://railway.app)

2. **New Project from GitHub**:
   - Connect your repository
   - Railway auto-detects Python and Streamlit

3. **Add Environment Variables** in the Variables tab:
   - `GOOGLE_API_KEY`
   - `PINECONE_API_KEY`

4. **Custom Start Command** (if needed):
   ```
   streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

### Deploy to Streamlit Community Cloud

1. **Push to GitHub**
2. **Go to**: [share.streamlit.io](https://share.streamlit.io)
3. **Deploy**: Select your repository
4. **Add Secrets** in Advanced Settings:
   ```toml
   GOOGLE_API_KEY = "your_key"
   PINECONE_API_KEY = "your_key"
   ```

## 🔧 Configuration

You can adjust limits in `app.py`:

```python
MAX_CODEBASE_SIZE_MB = 100  # Maximum codebase size
MAX_FILES = 1000             # Maximum number of files
MAX_FILE_SIZE_MB = 1         # Maximum individual file size
```

## 🐛 Troubleshooting

### "GOOGLE_API_KEY not found"
- Ensure `.env` file exists with the correct key
- For deployment, add as environment variable in platform settings

### "Git clone failed"
- Check if the repository is public
- Verify the URL is correct
- Large repositories may timeout (5-minute limit)

### "No supported code files found"
- Check if your codebase contains supported file types
- Verify files aren't in ignored directories

### "Codebase too large"
- Reduce the size below 100MB
- Or increase `MAX_CODEBASE_SIZE_MB` in `app.py`

## 📝 Project Structure

```
codebase-qa-app/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your API keys (not committed)
├── README.md             # This file
├── AI_NOTES.md           # AI development notes
├── ABOUTME.md            # Developer information
└── PROMPTS_USED.md       # Prompts used in development
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Vector storage by [Pinecone](https://www.pinecone.io/)
- Orchestrated with [LangChain](https://www.langchain.com/)

## 📧 Support

For questions or issues, please open an issue on GitHub or contact the developer.

---

**Made with ❤️ using AI assistance**
