import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

class SharedMemory:
    def __init__(self):
        self.entries: Dict[str, dict] = {}
    
    def store(self, entry: dict) -> str:
        """Store an entry in memory and return its ID"""
        entry_id = f"mem_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now().isoformat()
        
        memory_entry = {
            "id": entry_id,
            "timestamp": timestamp,
            **entry
        }
        
        self.entries[entry_id] = memory_entry
        
        # Keep only last 50 entries to prevent memory bloat
        if len(self.entries) > 50:
            oldest_key = sorted(self.entries.keys())[0]
            del self.entries[oldest_key]
        
        print(f"Memory stored: {entry_id} - {entry.get('format')}/{entry.get('intent')}")
        return entry_id
    
    def get(self, entry_id: str) -> Optional[dict]:
        """Get an entry by ID"""
        return self.entries.get(entry_id)
    
    def get_all(self) -> List[dict]:
        """Get all entries sorted by timestamp"""
        return sorted(
            list(self.entries.values()),
            key=lambda x: x.get("timestamp", "")
        )
    
    def get_by_conversation_id(self, conversation_id: str) -> List[dict]:
        """Get all entries for a specific conversation"""
        return [
            entry for entry in self.entries.values()
            if entry.get("conversationId") == conversation_id
        ]
    
    def clear(self) -> None:
        """Clear all entries from memory"""
        self.entries.clear()
        print("Memory cleared")
    
    def get_stats(self) -> dict:
        """Get statistics about the memory contents"""
        entries = list(self.entries.values())
        
        format_counts = {}
        intent_counts = {}
        
        for entry in entries:
            # Count formats
            entry_format = entry.get("format", "unknown")
            format_counts[entry_format] = format_counts.get(entry_format, 0) + 1
            
            # Count intents
            intent = entry.get("intent", "unknown")
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        return {
            "total": len(entries),
            "byFormat": format_counts,
            "byIntent": intent_counts
        }

# Singleton instance
shared_memory = SharedMemory()