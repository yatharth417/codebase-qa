# Prompts Used in Development

This document records the prompts and conversations used with AI assistants during the development of this project.

## 🎯 Initial Project Prompt

**Date:** [Current Date]

**Prompt:**
```
Role: Expert Python Developer and AI Engineer. 
Task: Build a functional, deployable web application for "Codebase Q&A with Proof" within a 48-hour deadline.

Problem Statement: Build a web app where a user can upload a zip file of a codebase (or provide a public GitHub URL), ask questions about the code, and receive answers supported by file paths, line ranges, and the actual code snippets retrieved.

Technical Stack Requirements:
- Frontend/Backend Framework: Python Streamlit
- LLM Orchestration: LangChain
- LLM Provider: Google Gemini API
- Vector Database: Pinecone (serverless)
- Code Parsing: LangChain's GenericLoader or LanguageParser

[Full requirements detailed in initial specification]
```

**Clarifications Made:**
1. Vector DB: Pinecone (serverless)
2. GitHub Support: Clone repo temporarily
3. Deployment Target: Render/Railway compatible
4. File Limits: Max 100MB codebase, 1000 files max, 1MB per file

---

## 📝 Development Phase Prompts

### Phase 1: Project Structure

**Prompt:**
```
Create the basic project structure with:
- Main Streamlit app
- Requirements.txt with all dependencies
- .env.example for API keys
- Basic error handling
```

**Output:** Initial `app.py`, `requirements.txt`, `.env.example`

---

### Phase 2: Core RAG Pipeline

**Prompt:**
```
Implement the RAG pipeline with:
1. File collection from zip/GitHub
2. Document chunking with LangChain
3. Embedding generation with Google AI
4. Vector storage in Pinecone
5. Retrieval and answer generation
```

**Output:** Complete RAG implementation in `app.py`

**Key Functions Created:**
- `collect_code_files()` - File discovery
- `load_and_split_documents()` - Chunking
- `create_or_get_pinecone_index()` - Index management
- `index_codebase()` - Main indexing flow
- `answer_question()` - Q&A with retrieval

---

### Phase 3: UI/UX Implementation

**Prompt:**
```
Create Streamlit UI with:
1. Service status sidebar
2. Upload & Index tab with ZIP and GitHub options
3. Ask Questions tab with chat interface
4. Source attribution with expandable code snippets
5. Progress indicators and error messages
```

**Output:** Complete Streamlit interface

**UI Components:**
- Sidebar with status indicators
- Tabbed interface
- Chat history display
- Expandable source viewers
- Progress bars for indexing

---

### Phase 4: Error Handling & Validation

**Prompt:**
```
Add comprehensive error handling for:
- Missing API keys
- Invalid file uploads
- Large codebases
- GitHub clone failures
- Pinecone connection issues
```

**Output:** Error handling throughout `app.py`

**Error Scenarios Covered:**
- API key validation
- File size checks
- Directory size validation
- Git clone timeouts
- Empty file collections

---

### Phase 5: Documentation

**Prompt:**
```
Create comprehensive documentation:
1. README.md with setup and deployment instructions
2. AI_NOTES.md documenting AI usage
3. ABOUTME.md template for developer info
4. PROMPTS_USED.md (this file)
```

**Output:** Complete documentation suite

---

## 🔧 Technical Prompts

### Pinecone Index Creation

**Prompt:**
```
Create a Pinecone serverless index with:
- Dimension: 768 (Google embeddings)
- Metric: cosine
- Cloud: AWS
- Region: us-east-1
Handle existing index gracefully
```

**Implementation:**
```python
pc.create_index(
    name=index_name,
    dimension=768,
    metric='cosine',
    spec=ServerlessSpec(cloud='aws', region='us-east-1')
)
```

---

### Document Chunking Strategy

**Prompt:**
```
Implement optimal chunking for code files:
- Chunk size: 1000 characters
- Overlap: 200 characters
- Preserve code structure
- Add metadata (file path, chunk index)
```

**Implementation:**
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)
```

---

### LLM Prompt Engineering

**Prompt:**
```
Create a prompt template for code Q&A that:
1. Takes question and code context
2. Instructs LLM to be specific about file references
3. Acknowledges when info is insufficient
4. Keeps answers concise and code-focused
```

**Implementation:**
```python
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful code assistant. 
    Answer based on provided code snippets. Be specific 
    and reference file names."""),
    ("user", """Question: {question}
    
    Relevant Code:
    {context}
    
    Provide a clear answer based on the code above.""")
])
```

---

## 🐛 Debugging Prompts

### Session State Issue

**Problem:** Chat history not persisting  
**Prompt:** "Implement session state management for chat history with last 10 Q&A pairs"  
**Solution:** Added `st.session_state.qa_history` with list slicing

---

### Large File Handling

**Problem:** Memory issues with large files  
**Prompt:** "Add file size limits and skip large files gracefully"  
**Solution:** Implemented `MAX_FILE_SIZE_MB` check in `collect_code_files()`

---

### GitHub Clone Timeout

**Problem:** Large repos timing out  
**Prompt:** "Add timeout and depth limit to git clone command"  
**Solution:** Added `--depth 1` flag and 300-second timeout

---

## 🎨 UI/UX Prompts

### Source Attribution Display

**Prompt:**
```
Create an expandable section showing:
1. File path
2. Code snippet
3. Syntax highlighting
4. Multiple sources if available
```

**Output:** Expander with code blocks and markdown

---

### Status Indicators

**Prompt:**
```
Add sidebar showing connection status for:
- LLM (Gemini)
- Embeddings
- Database (Pinecone)
Use green/red indicators
```

**Output:** `check_service_status()` function with emoji indicators

---

## 📊 Optimization Prompts

### Performance Improvements

**Prompt:** "Add progress indicators for long operations (file processing, embedding)"  
**Implementation:** Added `st.progress()` and `st.spinner()` throughout

**Prompt:** "Optimize file collection to skip ignored directories early"  
**Implementation:** Early return in path traversal for `IGNORE_DIRS`

---

## 🚀 Deployment Prompts

### Render Configuration

**Prompt:**
```
Create deployment instructions for Render with:
- Build command
- Start command with PORT binding
- Environment variable setup
```

**Output:** Added to README.md deployment section

---

### Railway Configuration

**Prompt:**
```
Add Railway deployment guide with:
- Auto-detection notes
- Environment variable setup
- Custom start command if needed
```

**Output:** Added to README.md deployment section

---

## 📝 Documentation Prompts

### README Structure

**Prompt:**
```
Create a comprehensive README with:
1. Feature list
2. Tech stack
3. Prerequisites
4. Setup instructions
5. Usage guide
6. Deployment guides (Render, Railway, Streamlit)
7. Troubleshooting section
```

**Output:** Complete README.md

---

### AI Notes Documentation

**Prompt:**
```
Document AI usage including:
- What AI was used for
- What was manually verified
- LLM selection reasoning
- Known limitations
- Future improvements
```

**Output:** Complete AI_NOTES.md

---

## 🔄 Iterative Refinement Prompts

1. **"Add file type filtering to only process supported code files"**
   - Added `SUPPORTED_EXTENSIONS` set

2. **"Implement ignore directories list for node_modules, .git, etc."**
   - Added `IGNORE_DIRS` set

3. **"Add better error messages with actionable suggestions"**
   - Enhanced error messages throughout

4. **"Show indexing progress to user"**
   - Added progress bar in `load_and_split_documents()`

5. **"Handle case where zip contains single root folder"**
   - Added directory detection in zip extraction

---

## 💡 Lessons from Prompt Engineering

### What Worked Well:

1. **Specific Requirements**
   - Clear file limits
   - Exact tech stack versions
   - Concrete use cases

2. **Structured Requests**
   - Breaking into phases
   - Function-level requests
   - Component-by-component UI

3. **Error Scenario Listing**
   - Enumerating edge cases
   - Asking for graceful handling
   - Requesting user-friendly messages

### What Needed Refinement:

1. **Initial chunking strategy** - Required adjustment for code structure
2. **Status check timing** - Needed to be non-blocking
3. **Progress indicators** - Required multiple iterations for UX

---

## 🎯 Final Verification Prompts

**Prompt:**
```
Review the complete application for:
1. Security (no hardcoded keys)
2. Error handling completeness
3. User experience flow
4. Documentation accuracy
5. Deployment readiness
```

**Checklist Completed:**
- ✅ No hardcoded API keys
- ✅ All error paths handled
- ✅ Clear user feedback
- ✅ Documentation matches code
- ✅ Ready for deployment

---

## 📚 Reference Prompts Used

1. "Show me LangChain's RecursiveCharacterTextSplitter usage for code"
2. "How to integrate Google Gemini with LangChain?"
3. "Pinecone serverless index creation example"
4. "Streamlit chat interface best practices"
5. "Git clone subprocess with timeout in Python"

---

**Total Development Time:** ~4 hours  
**Number of Major Prompts:** ~25  
**Iterations:** 3-4 per major component  
**AI Assistant:** Claude (Anthropic) - Sonnet 4.5
