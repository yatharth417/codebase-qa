# Prompts Used

Record of key prompts used with Claude AI during development.

---

## Initial Setup

**Prompt:**
```
I need to fix dependency conflicts in my requirements.txt. 
[Provided error message about langchain-groq compatibility]
```

**Result:** Fixed version conflicts in requirements.txt

---

## Model Issues

**Prompt:**
```
Error: "The model 'llama3-70b-8192' has been decommissioned"
What's the replacement?
```

**Result:** Updated to `llama-3.3-70b-versatile`

---

**Prompt:**
```
Error: "404 models/embedding-001 is not found for API version v1beta"
```

**Result:** Fixed embedding model name to `models/gemini-embedding-001`

---

## Deployment

**Prompt:**
```
Railway build failing with dependency conflict:
[Provided full error about langchain-core versions]
```

**Result:** Updated `langchain-core>=0.3.37,<0.4.0`

---

## Documentation

**Prompt:**
```
Create README.md, AI_NOTES.md, ABOUTME.md, and PROMPTS_USED.md
Requirements:
- How to run
- What AI was used for
- What I verified myself
- Why I chose specific LLMs
```

**Result:** Generated documentation templates

---

## Debugging Process

**Prompt:**
```
App works locally but LLM shows "Disconnected" on Railway.
What debugging steps should I follow?
```

**Result:** Systematic debugging checklist

---

