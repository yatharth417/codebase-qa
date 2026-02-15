"""
Setup Verification Script
Run this to verify all dependencies are installed correctly
"""

import sys

def test_imports():
    """Test if all required packages can be imported"""
    
    tests = {
        'Streamlit': 'streamlit',
        'LangChain': 'langchain',
        'Google Generative AI': 'google.generativeai',
        'LangChain Google GenAI': 'langchain_google_genai',
        'Pinecone': 'pinecone',
        'LangChain Pinecone': 'langchain_pinecone',
        'Python dotenv': 'dotenv',
    }
    
    print("🔍 Testing package imports...\n")
    
    all_passed = True
    for name, module in tests.items():
        try:
            __import__(module)
            print(f"✅ {name:<25} OK")
        except ImportError as e:
            print(f"❌ {name:<25} FAILED: {e}")
            all_passed = False
    
    return all_passed


def test_environment():
    """Check for environment variables"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print("\n🔍 Checking environment variables...\n")
    
    env_vars = {
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
        'PINECONE_API_KEY': os.getenv('PINECONE_API_KEY'),
    }
    
    all_set = True
    for var_name, var_value in env_vars.items():
        if var_value:
            print(f"✅ {var_name:<20} Set ({var_value[:8]}...)")
        else:
            print(f"❌ {var_name:<20} NOT SET")
            all_set = False
    
    return all_set


def test_services():
    """Test connection to services"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print("\n🔍 Testing service connections...\n")
    
    all_connected = True
    
    # Test Google Gemini
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        gemini_key = os.getenv('GOOGLE_API_KEY')
        if gemini_key:
            llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_key)
            print("✅ Google Gemini API    Connected")
        else:
            print("⚠️  Google Gemini API    Key not set")
            all_connected = False
    except Exception as e:
        print(f"❌ Google Gemini API    Failed: {e}")
        all_connected = False
    
    # Test Google Embeddings
    try:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        gemini_key = os.getenv('GOOGLE_API_KEY')
        if gemini_key:
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=gemini_key
            )
            print("✅ Google Embeddings    Connected")
        else:
            print("⚠️  Google Embeddings    Key not set")
            all_connected = False
    except Exception as e:
        print(f"❌ Google Embeddings    Failed: {e}")
        all_connected = False
    
    # Test Pinecone
    try:
        from pinecone import Pinecone
        pinecone_key = os.getenv('PINECONE_API_KEY')
        if pinecone_key:
            pc = Pinecone(api_key=pinecone_key)
            indexes = pc.list_indexes()
            print("✅ Pinecone Database    Connected")
        else:
            print("⚠️  Pinecone Database    Key not set")
            all_connected = False
    except Exception as e:
        print(f"❌ Pinecone Database    Failed: {e}")
        all_connected = False
    
    return all_connected


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Codebase Q&A - Setup Verification")
    print("=" * 60)
    
    imports_ok = test_imports()
    env_ok = test_environment()
    services_ok = test_services()
    
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    print(f"Imports:     {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"Environment: {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"Services:    {'✅ PASS' if services_ok else '❌ FAIL'}")
    
    if imports_ok and env_ok and services_ok:
        print("\n✅ All tests passed! Ready to run the app.")
        print("Run: streamlit run app.py")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        if not imports_ok:
            print("   → Run: pip install -r requirements.txt")
        if not env_ok:
            print("   → Create .env file with your API keys")
        if not services_ok:
            print("   → Verify your API keys are correct")
        return 1


if __name__ == "__main__":
    sys.exit(main())
