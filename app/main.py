from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from fastapi.responses import JSONResponse, FileResponse
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Check if API key is available
if not os.getenv("GOOGLE_API_KEY"):
    print("WARNING: GOOGLE_API_KEY not found in environment variables")

app = FastAPI(title="Multi-Agent Processing System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import agents after app initialization to avoid circular imports
from app.agents import classifier_agent, email_agent, json_agent
from app.memory import shared_memory

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    # Redirect to the HTML page
    return FileResponse("static/index.html")

@app.get("/")
async def read_root():
    return {"message": "Multi-Agent Processing System API"}

@app.post("/api/agents/classifier")
async def process_with_classifier(request: Request):
    try:
        data = await request.json()
        input_text = data.get("input")
        input_type = data.get("inputType", "unknown")
        
        if not input_text:
            raise HTTPException(status_code=400, detail="Input text is required")
        
        # Process with classifier agent
        result = classifier_agent.process(input_text, input_type)
        return JSONResponse(content=result)
    
    except Exception as e:
        print(f"Error in classifier endpoint: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Processing failed", "details": str(e)}
        )

@app.post("/api/agents/email")
async def process_with_email_agent(request: Request):
    try:
        data = await request.json()
        input_text = data.get("input")
        
        if not input_text:
            raise HTTPException(status_code=400, detail="Email content is required")
        
        # Process with email agent
        result = email_agent.process(input_text)
        return JSONResponse(content=result)
    
    except Exception as e:
        print(f"Error in email agent endpoint: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Email processing failed", "details": str(e)}
        )

@app.post("/api/agents/json")
async def process_with_json_agent(request: Request):
    try:
        data = await request.json()
        input_text = data.get("input")
        
        if not input_text:
            raise HTTPException(status_code=400, detail="JSON input is required")
        
        # Process with JSON agent
        result = json_agent.process(input_text)
        return JSONResponse(content=result)
    
    except Exception as e:
        print(f"Error in JSON agent endpoint: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "JSON processing failed", "details": str(e)}
        )

@app.get("/api/memory")
async def get_memory():
    try:
        entries = shared_memory.get_all()
        stats = shared_memory.get_stats()
        return {"entries": entries, "stats": stats, "success": True}
    
    except Exception as e:
        print(f"Error retrieving memory: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to retrieve memory"}
        )

@app.delete("/api/memory")
async def clear_memory():
    try:
        shared_memory.clear()
        return {"message": "Memory cleared successfully", "success": True}
    
    except Exception as e:
        print(f"Error clearing memory: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to clear memory"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)