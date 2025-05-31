### 🧠 Multi-Agent Processing System
A powerful document processing system that uses Gemini AI to classify, extract, and analyze various types of content. The system employs multiple specialized AI agents working together to process emails, JSON data, and text documents.
### Video Link for the project:-
For Codebase:- https://youtu.be/SpWtAKRd1d0
For Working Model:- https://youtu.be/RXNRHtwXLow
### Similiar Agent Done with Typescript and next.js which is deployed
Deployed Link:- https://multiagents1next-szpq.vercel.app/
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
`pip install -r requirements.txt`  
**Set up your Gemini API key:**  
`GOOGLE_API_KEY=your_gemini_api_key_here`  
**Running the Application:**  
`python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload`

## 📊 How It Works
![image](https://github.com/user-attachments/assets/40104e91-5623-46a8-a998-e8957f4fb139)

## 🔌 API Endpoints
## |Endpoint| Method| Description
**API Endpoints:**  
`POST /api/agents/classifier`  
Process input with the Classifier Agent  
`POST /api/agents/email`  
Process email content directly  
`POST /api/agents/json`  
Process JSON data directly  
`GET /api/memory`  
Retrieve all memory entries  
`DELETE /api/memory`  
Clear all memory entries


## 🧪 Example Usage
you can use the sample email,json and text in the web app
## Email Parse
![image](https://github.com/user-attachments/assets/4c221f19-59e8-4e98-b1f8-c16234eb346e)
## Json 
![image](https://github.com/user-attachments/assets/7a3a3e73-e324-44e5-aecd-1feb06b433d6)
## Text
![image](https://github.com/user-attachments/assets/3e71e0e5-8818-476b-94c1-eadc761d6e1f)

## 🔍 Agent Details
### Classifier Agent
- **Purpose**: Determines document type and intent
- **Input**: Raw text content
- **Output**: Classification and routing decision
- **Model**: Gemini 1.5 Flash
### Email Agent
- **Purpose**: Extracts structured data from emails
- **Input**: Email content
- **Output**: CRM-style record with sender, intent, requirements
- **Model**: Gemini 1.5 Flash
### JSON Agent
- **Purpose**: Standardizes JSON data
- **Input**: JSON content
- **Output**: FlowBit schema with standardized fields
- **Model**: Gemini 1.5 Flash
