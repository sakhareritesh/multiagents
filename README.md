### 🧠 Multi-Agent Processing System
A powerful document processing system that uses Gemini AI to classify, extract, and analyze various types of content. The system employs multiple specialized AI agents working together to process emails, JSON data, and text documents.
![image](https://github.com/user-attachments/assets/0eb61cb9-23df-4421-ab8d-4714438a5851)
## ✨ Features
- **🔍 Intelligent Classification**: Automatically identifies document type and intent
- **📧 Email Processing**: Extracts sender details, intent, urgency, and business requirements
- **📄 JSON Processing**: Parses and standardizes JSON data into a consistent format
- **📝 Text Analysis**: Extracts key information from plain text documents
- **💾 Shared Memory**: Cross-agent context sharing and history tracking
- **⚠️ Anomaly Detection**: Identifies inconsistencies and missing information
- **🔄 Real-time Processing**: Instant results with streaming UI updates
- **💯 Free Tier**: Uses Google's Gemini AI (free tier available)
- 
## 🛠️ Technology Stack
- **Backend**: Python 3.9+ with FastAPI
- **AI**: Google Generative AI (Gemini 1.5 Flash)
- **Frontend**: HTML, CSS, JavaScript
- **Data Validation**: Pydantic
- **Memory Store**: In-memory with Python dictionaries

## 🚀 Installation
**Install dependencies:**
pip install -r requirements.txt
**Set up your Gemini API key:**
GOOGLE_API_KEY=your_gemini_api_key_here
**Running the Application**
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

## 📊 How It Works
![image](https://github.com/user-attachments/assets/8bd6fbb3-169a-40a3-8a14-b4a86238dcc2)
