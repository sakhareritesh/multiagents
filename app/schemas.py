from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

class Classification(BaseModel):
    format: str
    intent: str
    confidence: float
    reasoning: str

class Entity(BaseModel):
    type: str
    value: str

class BasicExtraction(BaseModel):
    summary: str
    key_points: List[str]
    entities: List[Entity]
    urgency: str
    action_items: List[str]

class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None

class JsonExtractedData(BaseModel):
    id: str
    type: str
    vendor: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None
    line_items: Optional[List[LineItem]] = None

class JsonAnalysis(BaseModel):
    extracted_data: JsonExtractedData
    detected_anomalies: List[str]
    confidence: float
    business_context: str

class FlowBitData(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None
    vendor: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None
    line_items: Optional[List[LineItem]] = None

class FlowBitMetadata(BaseModel):
    confidence: float
    processing_agent: str
    anomalies: Optional[List[str]] = None
    business_context: Optional[str] = None

class FlowBit(BaseModel):
    id: str
    type: str
    source: str
    timestamp: str
    data: FlowBitData
    metadata: FlowBitMetadata

class Sender(BaseModel):
    name: str
    email: str
    company: Optional[str] = None
    title: Optional[str] = None

class Quantity(BaseModel):
    item: str
    quantity: Optional[float] = None
    specifications: Optional[str] = None

class EmailExtractedData(BaseModel):
    request_type: str
    requirements: List[str]
    deadline: Optional[str] = None
    budget: Optional[str] = None
    quantities: Optional[List[Quantity]] = None
    contact_preference: Optional[str] = None
    key_dates: Optional[List[str]] = None

class EmailExtraction(BaseModel):
    sender: Sender
    subject: str
    intent: str
    urgency: str
    extracted_data: EmailExtractedData
    conversation_id: str
    confidence: float
    sentiment: str

class CrmRecord(BaseModel):
    lead_id: str
    source: str
    timestamp: str
    contact: Sender
    communication: Dict[str, Any]
    opportunity: EmailExtractedData
    next_actions: List[str]
    confidence: float
    priority: str