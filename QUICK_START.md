# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## 📦 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🔑 2. Set Up API Keys

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```env
GOOGLE_API_KEY=your_google_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

### Where to Get API Keys:

**Google Gemini API Key:**
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

**Pinecone API Key:**
1. Go to https://app.pinecone.io/
2. Sign up for free account
3. Create a project
4. Copy API key from "API Keys" section

## ✅ 3. Verify Setup

```bash
python test_setup.py
```

You should see all green checkmarks ✅

## 🚀 4. Run the App

```bash
streamlit run app.py
```

The app will open at http://localhost:8501

## 🎯 5. Test It Out

### Upload a Test Codebase

**Option 1: Upload ZIP**
1. Zip a small code project (< 10MB)
2. Upload via the interface
3. Click "Index from ZIP"

**Option 2: Use GitHub**
1. Enter a public GitHub URL (e.g., https://github.com/streamlit/streamlit)
2. Click "Index from GitHub"

### Ask Questions

Try these example questions:
- "What does this codebase do?"
- "How is authentication handled?"
- "Show me the main entry point"
- "What APIs are exposed?"

## 🐛 Common Issues

### "Module not found"
```bash
pip install -r requirements.txt
```

### "API key not found"
- Check your `.env` file exists
- Verify keys are correct
- No quotes needed around keys

### "No supported files found"
- Ensure your codebase has code files (.py, .js, etc.)
- Check it's not all in ignored directories (node_modules, .git)

## 📚 Next Steps

- Read the full [README.md](README.md) for details
- Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) to deploy
- Review [AI_NOTES.md](AI_NOTES.md) for architecture

## 💡 Pro Tips

1. **Start Small**: Test with a small codebase first (< 10MB)
2. **Be Specific**: Ask targeted questions for better answers
3. **Check Sources**: Always verify the code snippets returned
4. **Iterate**: Refine your questions based on initial answers

---

**Need Help?** Open an issue on GitHub!
