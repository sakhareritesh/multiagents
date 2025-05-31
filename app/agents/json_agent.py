import json
from datetime import datetime
from typing import Dict, Any, List

from app.agents.base import BaseAgent

class JsonAgent(BaseAgent):
    def __init__(self):
        super().__init__(model_name='gemini-1.5-flash')
        self.agent_type = "json_agent"
    
    def process(self, json_input: str) -> Dict[str, Any]:
        """Process JSON input and extract structured data"""
        print("JSON Agent: Starting JSON processing...")
        
        anomalies = []
        
        # Step 1: Parse and validate JSON
        try:
            parsed_json = json.loads(json_input)
            print("JSON parsed successfully")
        except json.JSONDecodeError:
            anomalies.append("Invalid JSON format - could not parse")
            raise Exception("Invalid JSON input")
        
        # Step 2: Analyze and extract data using Gemini
        try:
            analysis = self._analyze_json(parsed_json)
            print("JSON analysis completed")
            
            # Step 3: Add detected anomalies
            anomalies.extend(analysis.get("detected_anomalies", []))
            
            # Step 4: Create FlowBit standardized format
            flow_bit_data = {
                "id": analysis["extracted_data"]["id"],
                "type": analysis["extracted_data"]["type"],
                "source": "json_agent",
                "timestamp": datetime.now().isoformat(),
                "data": analysis["extracted_data"],
                "metadata": {
                    "confidence": analysis["confidence"],
                    "processing_agent": "json_agent",
                    "anomalies": anomalies if anomalies else None,
                    "business_context": analysis.get("business_context", "")
                }
            }
            
            # Step 5: Validate FlowBit structure
            try:
                self._validate_flow_bit(flow_bit_data)
                print("FlowBit validation successful")
                
                return {
                    "extracted_data": flow_bit_data,
                    "anomalies": anomalies if anomalies else None
                }
            
            except Exception as validation_error:
                print(f"FlowBit validation failed: {str(validation_error)}")
                anomalies.append("Data does not fully conform to FlowBit schema")
                
                return {
                    "extracted_data": flow_bit_data,
                    "anomalies": anomalies
                }
        
        except Exception as e:
            print(f"JSON Agent processing error: {str(e)}")
            raise Exception(f"JSON processing failed: {str(e)}")
    
    def _analyze_json(self, parsed_json: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze JSON data using Gemini"""
        prompt = f"""You are a JSON processing specialist. Analyze this JSON data and extract it into a standardized business format:

{json.dumps(parsed_json, indent=2)}

Extract and standardize:
1. ID (use existing ID or generate descriptive one)
2. Type (invoice, order, webhook, payment, etc.)
3. Vendor/supplier/company name
4. Amount and currency (if financial)
5. Description of the transaction/event
6. Due date or important dates
7. Status (pending, approved, completed, etc.)
8. Line items with quantities and prices (if applicable)

Also identify anomalies:
- Missing critical fields for the document type
- Inconsistent data types or formats
- Invalid amounts, dates, or values
- Suspicious or unusual patterns
- Data quality issues

Provide:
- Confidence score (0-1)
- Business context explanation
- Comprehensive anomaly detection

Be thorough and business-focused.

Return your answer as a JSON object with extracted_data, detected_anomalies, confidence, and business_context fields.
"""
        
        response = self.model.generate_content(prompt)
        response_text = response.text
        
        try:
            analysis = self.extract_json_from_response(response_text)
        except ValueError:
            # Create a basic structure if JSON parsing fails
            raise Exception("Failed to parse JSON analysis results")
        
        return analysis
    
    def _validate_flow_bit(self, flow_bit_data: Dict[str, Any]) -> None:
        """Validate FlowBit data structure"""
        required_fields = ["id", "type", "source", "timestamp", "data", "metadata"]
        for field in required_fields:
            if field not in flow_bit_data:
                raise Exception(f"Missing required field: {field}")
        
        if "confidence" not in flow_bit_data["metadata"]:
            raise Exception("Missing confidence in metadata")
        
        if "processing_agent" not in flow_bit_data["metadata"]:
            raise Exception("Missing processing_agent in metadata")