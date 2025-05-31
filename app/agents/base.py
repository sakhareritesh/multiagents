import os
import json
import google.generativeai as genai
from typing import Dict, Any, List, Optional

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, model_name='gemini-1.5-flash'):
        self.model = genai.GenerativeModel(model_name)
        self.agent_type = "base_agent"
        print(f"{self.agent_type.capitalize()} initialized with Gemini model: {model_name}")
    
    def extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract JSON from a text response"""
        try:
            # Try to parse the entire response as JSON
            return json.loads(response_text)
        except json.JSONDecodeError:
            # If that fails, try to extract JSON from the text
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            else:
                # Create a basic structure if JSON parsing fails
                raise ValueError("Failed to extract JSON from response")
    
    def extract_field(self, text: str, field_name: str, valid_values: List[str] = None, default: str = None) -> str:
        """Extract a field from text response"""
        import re
        
        # Try to find the field in the text
        pattern = rf'{field_name}[:\s]+([^\n]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            value = match.group(1).strip().lower()
            
            # If we have valid values, check if the extracted value is in them
            if valid_values:
                for valid in valid_values:
                    if valid.lower() in value:
                        return valid
            else:
                return value
        
        # Return default if no match or no valid value found
        return default