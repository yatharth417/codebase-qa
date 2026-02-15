"""
Codebase Q&A with Proof - Streamlit Application
RAG-based code question answering with source attribution
"""

import os
import streamlit as st
import tempfile
import shutil
import zipfile
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
from dotenv import load_dotenv

# LangChain imports
from langchain_groq import ChatGroq
import langchain_groq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

# Debug imports (temporary)
import groq

# Load environment variables
load_dotenv()

# Configuration
MAX_CODEBASE_SIZE_MB = 100
MAX_FILES = 50
MAX_FILE_SIZE_MB = 0.5
SUPPORTED_EXTENSIONS = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.h', 
                       '.cs', '.rb', '.go', '.rs', '.php', '.md', '.txt', '.json', '.yaml', '.yml'}
IGNORE_DIRS = {'node_modules', '.git', '__pycache__', 'venv', 'env', '.next', 'dist', 'build'}

# Page configuration
st.set_page_config(
    page_title="Codebase Q&A",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'qa_history' not in st.session_state:
    st.session_state.qa_history = []
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'indexed' not in st.session_state:
    st.session_state.indexed = False
if 'collection_name' not in st.session_state:
    st.session_state.collection_name = "codebase_collection"


def check_service_status() -> Dict[str, bool]:
    """Check the health status of all services"""
    status = {
        'llm': False,
        'embeddings': False
    }
    
    # Check LLM - Verify Groq connectivity with actual inference
    try:
        groq_key = os.getenv('GROQ_API_KEY')
        if groq_key:
            llm = ChatGroq(
                model="llama3-70b-8192", 
                groq_api_key=groq_key
            )
            # Verify with actual inference call
            response = llm.invoke("Reply with OK")
            if response and response.content:
                status['llm'] = True
    except Exception as e:
        status['llm_error'] = str(e)
        print(f"LLM health check failed: {str(e)}")
    
    # Check Embeddings - Use gemini-embedding-001 (3072 dimensions)
    try:
        google_key = os.getenv('GOOGLE_API_KEY')
        if google_key:
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001", 
                google_api_key=google_key
            )
            status['embeddings'] = True
    except Exception as e:
        status['embeddings_error'] = str(e)
        pass
    
    return status


def get_file_size_mb(file_path: Path) -> float:
    """Get file size in MB"""
    return file_path.stat().st_size / (1024 * 1024)


def get_directory_size_mb(directory: Path) -> float:
    """Get total directory size in MB"""
    total = sum(f.stat().st_size for f in directory.rglob('*') if f.is_file())
    return total / (1024 * 1024)


def extract_zip(zip_file, extract_to: Path) -> bool:
    """Extract zip file to directory"""
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except Exception as e:
        st.error(f"Error extracting zip: {str(e)}")
        return False


def clone_github_repo(url: str, clone_to: Path) -> bool:
    """Clone GitHub repository"""
    try:
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', url, str(clone_to)],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            return True
        else:
            st.error(f"Git clone failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        st.error("Git clone timeout (5 minutes). Repository too large.")
        return False
    except Exception as e:
        st.error(f"Error cloning repository: {str(e)}")
        return False


def collect_code_files(directory: Path) -> List[Path]:
    """Collect all code files from directory"""
    files = []
    file_count = 0
    
    for file_path in directory.rglob('*'):
        # Skip if in ignored directory
        if any(ignore_dir in file_path.parts for ignore_dir in IGNORE_DIRS):
            continue
        
        # Check if file
        if not file_path.is_file():
            continue
        
        # Check extension
        if file_path.suffix not in SUPPORTED_EXTENSIONS:
            continue
        
        # Check file size
        if get_file_size_mb(file_path) > MAX_FILE_SIZE_MB:
            st.warning(f"Skipping large file: {file_path.name} (>{MAX_FILE_SIZE_MB}MB)")
            continue
        
        files.append(file_path)
        file_count += 1
        
        # Check max files limit
        if file_count >= MAX_FILES:
            st.warning(f"Reached maximum file limit ({MAX_FILES}). Stopping collection.")
            break
    
    return files


def load_and_split_documents(files: List[Path], base_path: Path) -> List[Document]:
    """Load code files and split into chunks"""
    documents = []
    
    # Text splitter for code
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, file_path in enumerate(files):
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Create relative path for metadata
            relative_path = file_path.relative_to(base_path)
            
            # Split content into chunks
            chunks = text_splitter.split_text(content)
            
            # Create documents with metadata
            for chunk_idx, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        'source': str(relative_path),
                        'file_type': file_path.suffix,
                        'chunk_index': chunk_idx
                    }
                )
                documents.append(doc)
            
            # Update progress
            progress = (idx + 1) / len(files)
            progress_bar.progress(progress)
            status_text.text(f"Processing: {relative_path} ({idx + 1}/{len(files)})")
        
        except Exception as e:
            st.warning(f"Error processing {file_path.name}: {str(e)}")
    
    progress_bar.empty()
    status_text.empty()
    
    return documents


def index_codebase(source_path: Path) -> bool:
    """Index the codebase into Chroma"""
    try:
        # Check directory size
        dir_size = get_directory_size_mb(source_path)
        if dir_size > MAX_CODEBASE_SIZE_MB:
            st.error(f"Codebase too large: {dir_size:.2f}MB (max: {MAX_CODEBASE_SIZE_MB}MB)")
            return False
        
        st.info(f"Codebase size: {dir_size:.2f}MB")
        
        # Collect files
        with st.spinner("Collecting code files..."):
            files = collect_code_files(source_path)
        
        if not files:
            st.error("No supported code files found!")
            return False
        
        st.success(f"Found {len(files)} code files")
        
        # Load and split documents
        with st.spinner("Processing and chunking code..."):
            documents = load_and_split_documents(files, source_path)
        
        if not documents:
            st.error("No documents created!")
            return False
        
        st.success(f"Created {len(documents)} document chunks")
        
        # Create embeddings and vector store
        with st.spinner("Creating embeddings and indexing to Chroma..."):
            # Use embedding-001
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=os.getenv('GOOGLE_API_KEY')
            )
            
            # Create Chroma vector store with persistence
            persist_directory = "./chroma_db"
            vector_store = Chroma.from_documents(
                documents=documents,
                embedding=embeddings,
                persist_directory=persist_directory,
                collection_name=st.session_state.collection_name
            )
            
            st.session_state.vector_store = vector_store
            st.session_state.indexed = True
        
        st.success("✅ Codebase indexed successfully!")
        return True
    
    except Exception as e:
        st.error(f"Error during indexing: {str(e)}")
        return False


def answer_question(question: str) -> Tuple[str, List[Dict]]:
    """Answer question using RAG pipeline"""
    if not st.session_state.vector_store:
        return "Please index a codebase first.", []
    
    try:
        # Retrieve relevant documents
        docs = st.session_state.vector_store.similarity_search(question, k=5)
        
        if not docs:
            return "No relevant code found for your question.", []
        
        # Prepare context from documents
        context_parts = []
        sources = []
        
        for idx, doc in enumerate(docs):
            source_info = {
                'file_path': doc.metadata.get('source', 'Unknown'),
                'chunk_index': doc.metadata.get('chunk_index', 0),
                'content': doc.page_content
            }
            sources.append(source_info)
            context_parts.append(
                f"[File: {source_info['file_path']}]\n{doc.page_content}\n"
            )
        
        context = "\n---\n".join(context_parts)
        
        # Create prompt - combining system and user messages
        full_prompt = f"""You are a helpful code assistant. Answer the user's question based on the provided code snippets.
Be specific and reference the file names when relevant. If the code doesn't contain enough information, say so.

Question: {question}

Relevant Code:
{context}

Please provide a clear and concise answer based on the code above."""
        
        # Get LLM response
        llm = ChatGroq(
            model="llama3-70b-8192",
            groq_api_key=os.getenv('GROQ_API_KEY'),
            temperature=0.3
        )
        
        response = llm.invoke(full_prompt)
        
        answer = response.content
        
        return answer, sources
    
    except Exception as e:
        return f"Error generating answer: {str(e)}", []


def main():
    """Main application"""
    
    # Sidebar - Status and Info
    with st.sidebar:
        st.title("🔍 Codebase Q&A")
        st.markdown("---")
        
        # Service Status
        st.subheader("Service Status")
        status = check_service_status()
        
        # LLM Status
        st.write("🤖 LLM (Groq):", "🟢 Connected" if status['llm'] else "🔴 Disconnected")
        if not status['llm'] and 'llm_error' in status:
            st.caption(f"Error: {status['llm_error']}")
        
        # Embeddings Status
        st.write("📊 Embeddings (Gemini):", "🟢 Connected" if status['embeddings'] else "🔴 Disconnected")
        if not status['embeddings'] and 'embeddings_error' in status:
            st.caption(f"Error: {status['embeddings_error']}")
        
        # Vector DB Status
        st.write("💾 Vector DB:", "🟢 Chroma (Local)" if st.session_state.indexed else "⚪ Not Indexed")
        
        st.markdown("---")
        
        # Indexing Status
        st.subheader("Indexing Status")
        if st.session_state.indexed:
            st.success("✅ Codebase Indexed")
            st.info(f"Collection: {st.session_state.collection_name}")
            st.caption("Stored in: ./chroma_db")
        else:
            st.warning("⏳ No codebase indexed")
        
        st.markdown("---")
        
        # Debug Info (temporary debug code)
        st.subheader("🐛 Debug Info")
        st.caption(f"Groq SDK: {groq.__version__}")
        st.caption(f"LangChain Groq: {langchain_groq.__version__}")
        
        st.markdown("---")
        
        # Info
        st.subheader("ℹ️ Limits")
        st.write(f"- Max codebase: {MAX_CODEBASE_SIZE_MB}MB")
        st.write(f"- Max files: {MAX_FILES}")
        st.write(f"- Max file size: {MAX_FILE_SIZE_MB}MB")
    
    # Main content
    st.title("🔍 Codebase Q&A with Proof")
    st.markdown("""
    Upload your codebase or provide a GitHub URL to ask questions about your code.
    Get answers with file references and actual code snippets as proof.
    """)
    
    # Check API keys
    if not os.getenv('GOOGLE_API_KEY'):
        st.error("⚠️ GOOGLE_API_KEY not found in environment variables!")
        st.stop()
    
    if not os.getenv('GROQ_API_KEY'):
        st.error("⚠️ GROQ_API_KEY not found in environment variables!")
        st.stop()
    
    
    # Tabs for different sections
    tab1, tab2 = st.tabs(["📤 Upload & Index", "💬 Ask Questions"])
    
    with tab1:
        st.header("Upload Codebase")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Option 1: Upload ZIP")
            uploaded_file = st.file_uploader("Choose a ZIP file", type=['zip'])
            
            if uploaded_file:
                if st.button("Index from ZIP", type="primary"):
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_path = Path(temp_dir)
                        extract_path = temp_path / "extracted"
                        extract_path.mkdir()
                        
                        # Extract
                        if extract_zip(uploaded_file, extract_path):
                            # Find the root directory (in case zip contains a single root folder)
                            dirs = list(extract_path.iterdir())
                            if len(dirs) == 1 and dirs[0].is_dir():
                                source_path = dirs[0]
                            else:
                                source_path = extract_path
                            
                            # Index
                            index_codebase(source_path)
        
        with col2:
            st.subheader("Option 2: GitHub URL")
            github_url = st.text_input("Enter GitHub repository URL", 
                                      placeholder="https://github.com/username/repo")
            
            if github_url:
                if st.button("Index from GitHub", type="primary"):
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_path = Path(temp_dir)
                        clone_path = temp_path / "repo"
                        
                        # Clone
                        if clone_github_repo(github_url, clone_path):
                            # Index
                            index_codebase(clone_path)
    
    with tab2:
        st.header("Ask Questions")
        
        if not st.session_state.indexed:
            st.warning("⚠️ Please index a codebase first (Upload & Index tab)")
        else:
            # Display chat history
            for qa in st.session_state.qa_history[-10:]:  # Show last 10
                with st.chat_message("user"):
                    st.write(qa['question'])
                
                with st.chat_message("assistant"):
                    st.write(qa['answer'])
                    
                    if qa['sources']:
                        with st.expander(f"📁 View {len(qa['sources'])} source(s)"):
                            for idx, source in enumerate(qa['sources']):
                                st.markdown(f"**File:** `{source['file_path']}`")
                                st.code(source['content'], language='python')
                                if idx < len(qa['sources']) - 1:
                                    st.markdown("---")
            
            # Chat input
            question = st.chat_input("Ask a question about your codebase...")
            
            if question:
                # Display user message
                with st.chat_message("user"):
                    st.write(question)
                
                # Get answer
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        answer, sources = answer_question(question)
                    
                    st.write(answer)
                    
                    if sources:
                        with st.expander(f"📁 View {len(sources)} source(s)"):
                            for idx, source in enumerate(sources):
                                st.markdown(f"**File:** `{source['file_path']}`")
                                st.code(source['content'], language='python')
                                if idx < len(sources) - 1:
                                    st.markdown("---")
                
                # Save to history
                st.session_state.qa_history.append({
                    'question': question,
                    'answer': answer,
                    'sources': sources
                })
                
                # Keep only last 10
                if len(st.session_state.qa_history) > 10:
                    st.session_state.qa_history = st.session_state.qa_history[-10:]
                
                st.rerun()


if __name__ == "__main__":
    main()