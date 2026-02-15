# AI Usage Notes

## AI Tool Used

**Claude** (Anthropic) - Used as coding assistant and debugging partner

## What I Did Myself

### Architecture & Design
- Chose RAG architecture for code Q&A
- Selected tech stack: Groq (fast + free), Google Embeddings (quality + free), Chroma (simple + local)
- Designed upload → index → query workflow
- Planned error handling and limits

### Key Decisions
- **Groq**: Fastest free option (~300 tok/sec), good for code
- **Google Embeddings**: High quality, 1500 req/day free
- **Chroma**: Simple local vector DB, no external service

### Implementation
- Wrote file collection logic with ignore patterns
- Designed chunking strategy (500 chars, 100 overlap)
- Built health check system (real API calls)
- Created source attribution with metadata

### Testing & Debugging
- Tested with multiple codebases locally
- Fixed dependency conflicts (langchain-core versions)
- Resolved model deprecation (llama3-70b → llama-3.3-70b)
- Fixed embedding model naming (models/gemini-embedding-001)
- Debugged Railway deployment issues

## What AI Helped With

### Code Generation
AI generated boilerplate based on my specifications:
- Streamlit app structure
- LangChain pipeline setup
- File processing functions

**I reviewed, understood, and modified everything before using it.**

### Debugging
When stuck, I:
1. Tried solving myself first
2. Asked AI with full error messages
3. Understood the solution before applying
4. Tested to verify it works

### Documentation
AI helped format README and comments, but content was mine.

## My Verification Process

For every AI-generated code:
1. ✅ Read and understood the logic
2. ✅ Tested locally with different inputs
3. ✅ Modified when needed
4. ✅ Checked for security issues
5. ✅ Verified it meets requirements

## Problems I Solved

1. **Dependency conflicts** - Researched compatible versions, tested locally
2. **Model deprecation** - Found replacement in Groq docs
3. **Embedding model 404** - Tested different formats, found working one
4. **Railway deployment** - Fixed langchain-core version requirements

## Time Breakdown

**Total**: ~6 hours
- 1 hour: Research & planning (no AI)
- 2 hours: Implementation (with AI)
- 2 hours: Debugging (mix)
- 1 hour: Deployment & docs
