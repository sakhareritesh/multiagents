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
![image](https://github.com/user-attachments/assets/40104e91-5623-46a8-a998-e8957f4fb139)

## 🔌 API Endpoints
## |Endpoint| Method| Description
/api/agents/classifier|POST|Process input with the Classifier Agent
/api/agents/email|POST|Process email content directly
/api/agents/json`|POST|Process JSON data directly
/api/memory`|GET|Retrieve all memory entries
/api/memory|DELETE|clear all memory entries

## 🧪 Example Usage
import requests
email_content = """
From: john.doe@acmecorp.com
Subject: Urgent RFQ - Manufacturing Equipment
Hi there,
We need a quote for 50 units of industrial pumps for our new facility. 
This is urgent as we need to finalize our vendor selection by Friday.
Specifications:
- Flow rate: 100 GPM
- Pressure: 150 PSI
- Material: Stainless steel
Please send your best pricing and delivery timeline.
Best regards,
John Doe
Procurement Manager
ACME Corp
"""
response = requests.post(
    "http://localhost:8000/api/agents/classifier",
    json={"input": email_content, "inputType": "email"}
)
result = response.json()
print(f"Format: {result['classification']['format']}")
print(f"Intent: {result['classification']['intent']}")
print(f"Extracted data: {result['extracted_data']}")

![image](https://github.com/user-attachments/assets/4c221f19-59e8-4e98-b1f8-c16234eb346e)


