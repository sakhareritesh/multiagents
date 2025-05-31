import uuid
from datetime import datetime
from typing import Dict, Any, List

from app.agents.base import BaseAgent

class EmailAgent(BaseAgent):
    def __init__(self):
        super().__init__(model_name='gemini-1.5-flash')
        self.agent_type = "email_agent"
    
    def process(self, email_content: str) -> Dict[str, Any]:
        """Process email content and extract structured data"""
        print("Email Agent: Starting email processing...")
        
        try:
            # Extract data using Gemini
            extracted = self._extract_email_data(email_content)
            print("Email extraction completed")
            
            # Generate comprehensive CRM record
            crm_record = {
                "lead_id": f"lead_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:6]}",
                "source": "email",
                "timestamp": datetime.now().isoformat(),
                "contact": extracted["sender"],
                "communication": {
                    "subject": extracted["subject"],
                    "intent": extracted["intent"],
                    "urgency": extracted["urgency"],
                    "sentiment": extracted["sentiment"],
                    "conversation_id": extracted["conversation_id"],
                },
                "opportunity": extracted["extracted_data"],
                "next_actions": self._generate_next_actions(
                    extracted["intent"], 
                    extracted["urgency"], 
                    extracted["sentiment"]
                ),
                "confidence": extracted["confidence"],
                "priority": self._calculate_priority(
                    extracted["urgency"], 
                    extracted["intent"], 
                    extracted["sentiment"]
                ),
            }
            
            # Detect anomalies
            anomalies = self._detect_anomalies(extracted)
            
            return {
                "extracted_data": crm_record,
                "conversation_id": extracted["conversation_id"],
                "anomalies": anomalies if anomalies else None
            }
        
        except Exception as e:
            print(f"Email Agent processing error: {str(e)}")
            raise Exception(f"Email processing failed: {str(e)}")
    
    def _extract_email_data(self, email_content: str) -> Dict[str, Any]:
        """Extract structured data from email content using Gemini"""
        prompt = f"""You are an email processing specialist for CRM systems. Parse this email content and extract comprehensive structured data:

{email_content}

Extract and analyze:

SENDER INFORMATION:
- Full name, email address, company, job title
- Look in signatures, headers, and email body

EMAIL CLASSIFICATION:
- Subject line
- Intent: rfq, quote_request, complaint, support, invoice_inquiry, general, urgent_request
- Urgency: low/medium/high (look for urgent keywords, deadlines, CAPS)
- Sentiment: positive/neutral/negative tone

BUSINESS DETAILS:
- Type of request or inquiry
- Specific requirements or specifications
- Deadlines and important dates
- Budget mentions or price discussions
- Quantities and items requested
- Preferred contact method
- All key dates mentioned

CONVERSATION TRACKING:
- Generate a unique conversation ID
- Confidence score for extraction accuracy

Look for urgency indicators:
- Words like "urgent", "ASAP", "deadline", "immediately"
- Specific dates and timelines
- Escalation language

Be thorough and business-focused. Extract all actionable information.

Return your answer as a JSON object with sender, subject, intent, urgency, extracted_data, conversation_id, confidence, and sentiment fields.
"""
        
        response = self.model.generate_content(prompt)
        response_text = response.text
        
        try:
            extracted = self.extract_json_from_response(response_text)
        except ValueError:
            # Create a basic structure if JSON parsing fails
            raise Exception("Failed to parse email extraction results")
        
        # Ensure conversation_id exists
        if "conversation_id" not in extracted:
            extracted["conversation_id"] = f"conv_{uuid.uuid4().hex[:10]}"
        
        return extracted
    
    def _generate_next_actions(self, intent: str, urgency: str, sentiment: str) -> List[str]:
        """Generate next actions based on email classification"""
        actions = []
        
        # Intent-based actions
        if intent in ["rfq", "quote_request"]:
            actions.append("Prepare detailed quotation")
            actions.append("Review technical specifications")
            actions.append("Check inventory and pricing")
            actions.append("Assign to sales team")
        
        if intent == "complaint":
            actions.append("Escalate to customer service manager")
            actions.append("Investigate reported issue")
            actions.append("Prepare resolution plan")
        
        if intent == "support":
            actions.append("Route to technical support")
            actions.append("Create support ticket")
        
        # Urgency-based actions
        if urgency == "high":
            actions.insert(0, "PRIORITY: Respond within 2 hours")
            actions.append("Notify team lead immediately")
        
        # Sentiment-based actions
        if sentiment == "negative":
            actions.append("Handle with extra care")
            actions.append("Consider escalation to senior staff")
        
        # Standard actions
        actions.append("Send acknowledgment email")
        actions.append("Update CRM with interaction")
        
        return actions
    
    def _calculate_priority(self, urgency: str, intent: str, sentiment: str) -> str:
        """Calculate priority based on email classification"""
        score = 0
        
        # Urgency scoring
        if urgency == "high":
            score += 3
        elif urgency == "medium":
            score += 2
        else:
            score += 1
        
        # Intent scoring
        if intent == "complaint":
            score += 2
        elif intent in ["rfq", "quote_request"]:
            score += 2
        elif intent == "urgent_request":
            score += 3
        
        # Sentiment scoring
        if sentiment == "negative":
            score += 2
        
        if score >= 7:
            return "critical"
        if score >= 5:
            return "high"
        if score >= 3:
            return "medium"
        return "low"
    
    def _detect_anomalies(self, extracted: Dict[str, Any]) -> List[str]:
        """Detect anomalies in extracted email data"""
        anomalies = []
        
        # Email format validation
        if "sender" in extracted and "email" in extracted["sender"]:
            email = extracted["sender"]["email"]
            if "@" not in email or "." not in email:
                anomalies.append("Invalid or suspicious email format")
        
        # Confidence check
        if extracted.get("confidence", 0) < 0.7:
            anomalies.append("Low confidence in extraction accuracy")
        
        # Business logic validation
        if extracted.get("intent") == "rfq" and (
            "extracted_data" not in extracted or
            "requirements" not in extracted["extracted_data"] or
            not extracted["extracted_data"]["requirements"]
        ):
            anomalies.append("RFQ detected but no clear requirements identified")
        
        # Urgency vs content mismatch
        if extracted.get("urgency") == "high" and (
            "extracted_data" not in extracted or
            "deadline" not in extracted["extracted_data"] or
            not extracted["extracted_data"]["deadline"]
        ):
            anomalies.append("High urgency claimed but no specific deadline mentioned")
        
        # Missing critical information
        if "sender" not in extracted or "name" not in extracted["sender"] or len(extracted["sender"]["name"]) < 2:
            anomalies.append("Sender name missing or incomplete")
        
        if extracted.get("intent") in ["quote_request", "rfq"] and (
            "extracted_data" not in extracted or
            "quantities" not in extracted["extracted_data"] or
            not extracted["extracted_data"]["quantities"]
        ):
            anomalies.append("Quote request without quantity specifications")
        
        return anomalies