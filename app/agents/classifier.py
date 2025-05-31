import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.agents.base import BaseAgent
from app.memory import shared_memory

class ClassifierAgent(BaseAgent):
    def __init__(self):
        super().__init__(model_name='gemini-1.5-flash')
        self.agent_type = "classifier_agent"
        print("Classifier Agent initialized with Gemini model")
    
    def process(self, input_text: str, input_type: Optional[str] = None) -> Dict[str, Any]:
        """Process input and classify it"""
        print("Classifier Agent: Starting classification...")
        
        try:
            # Step 1: Classify the input using Gemini
            classification = self._classify_input(input_text, input_type)
            print("Classification result:", classification)
            
            # Step 2: Route to appropriate specialized agent
            extracted_data = {}
            anomalies = []
            processing_agent = "classifier_agent"
            
            try:
                # Import agents here to avoid circular imports
                from app.agents import email_agent, json_agent
                
                if classification["format"] == "email":
                    print("Routing to Email Agent...")
                    email_result = email_agent.process(input_text)
                    extracted_data = email_result["extracted_data"]
                    anomalies = email_result.get("anomalies", [])
                    processing_agent = "email_agent"
                
                elif classification["format"] == "json":
                    print("Routing to JSON Agent...")
                    json_result = json_agent.process(input_text)
                    extracted_data = json_result["extracted_data"]
                    anomalies = json_result.get("anomalies", [])
                    processing_agent = "json_agent"
                
                else:
                    print("Using basic extraction...")
                    extracted_data = self._basic_extraction(input_text, classification["intent"])
                    processing_agent = "basic_extractor"
            
            except Exception as e:
                print(f"Agent processing error: {str(e)}")
                anomalies.append(f"Processing error: {str(e)}")
                
                # Fallback to basic extraction
                extracted_data = self._basic_extraction(input_text, classification["intent"])
                processing_agent = "fallback_extractor"
            
            # Step 3: Store in shared memory
            memory_id = shared_memory.store({
                "source": input_text[:500],  # Store first 500 chars
                "format": classification["format"],
                "intent": classification["intent"],
                "extracted_data": extracted_data,
                "anomalies": anomalies if anomalies else None,
                "processing_agent": processing_agent
            })
            
            print("Processing completed successfully")
            
            return {
                "classification": classification,
                "extracted_data": extracted_data,
                "memory_id": memory_id,
                "timestamp": datetime.now().isoformat(),
                "anomalies": anomalies if anomalies else None,
                "processing_agent": processing_agent
            }
        
        except Exception as e:
            print(f"Classifier Agent error: {str(e)}")
            raise Exception(f"Classification failed: {str(e)}")
    
    def _classify_input(self, input_text: str, input_type: Optional[str] = None) -> Dict[str, Any]:
        """Classify the input using Gemini"""
        prompt = f"""You are a document classification AI agent. Analyze the following input and classify it accurately.

Input Type Hint: {input_type or "unknown"}
Content: {input_text}

Classify the:
1. Format: What type of content is this? (email, json, pdf, text)
2. Intent: What is the business purpose? (invoice, rfq, complaint, regulation, general, quote_request, support, webhook)
3. Confidence: How confident are you? (0-1 scale)
4. Reasoning: Explain your classification decision

Look for:
- Email indicators: From:, Subject:, email addresses, signatures
- JSON structure: brackets, key-value pairs, webhook patterns
- Business keywords: RFQ, invoice, complaint, regulation, urgent
- Intent signals: request for quote, payment terms, compliance requirements

Be precise and confident in your classification.

Return your answer as a JSON object with format, intent, confidence, and reasoning fields.
"""
        
        response = self.model.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text
        
        # Find JSON in the response
        try:
            # Try to parse the entire response as JSON
            classification = self.extract_json_from_response(response_text)
        except ValueError:
            # Last resort: try to create a structured response from text
            classification = {
                "format": self.extract_field(response_text, "format", ["email", "json", "text", "pdf"]),
                "intent": self.extract_field(response_text, "intent", 
                                            ["invoice", "rfq", "complaint", "regulation", "general", 
                                             "quote_request", "support", "webhook"]),
                "confidence": float(self.extract_field(response_text, "confidence", default="0.7")),
                "reasoning": self.extract_field(response_text, "reasoning", default="Classification based on content analysis")
            }
        
        return classification
    
    def _basic_extraction(self, input_text: str, intent: str) -> Dict[str, Any]:
        """Extract basic information from text"""
        try:
            prompt = f"""Extract key information from this {intent} content:

{input_text}

Provide:
1. A concise summary (2-3 sentences)
2. Key points or requirements (bullet points)
3. Important entities (dates, amounts, names, companies, etc.)
4. Urgency level based on language and deadlines
5. Suggested action items

Focus on business-relevant information and be thorough.

Return your answer as a JSON object with summary, key_points (array), entities (array of objects with type and value), urgency (low/medium/high), and action_items (array) fields.
"""
            
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Try to parse JSON from response
            try:
                extraction = self.extract_json_from_response(response_text)
            except ValueError:
                # Create a basic structure if JSON parsing fails
                extraction = {
                    "summary": "Failed to extract detailed information",
                    "key_points": ["Processing error occurred"],
                    "entities": [],
                    "urgency": "medium",
                    "action_items": ["Review input and try again"]
                }
            
            return extraction
        
        except Exception as e:
            print(f"Basic extraction error: {str(e)}")
            return {
                "summary": "Failed to extract detailed information",
                "key_points": ["Processing error occurred"],
                "entities": [],
                "urgency": "medium",
                "action_items": ["Review input and try again"]
            }