"""Base agent class for all specialized agents"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.created_at = datetime.utcnow()
        self.session_id: Optional[str] = None
        self.context: Dict[str, Any] = {}
        
    @abstractmethod
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request and return response"""
        pass
    
    def set_session_context(self, session_id: str, context: Dict[str, Any]):
        """Set the session context for this agent"""
        self.session_id = session_id
        self.context = context
        logger.info(f"{self.name} - Session context set: {session_id}")
    
    def get_session_context(self) -> Dict[str, Any]:
        """Get current session context"""
        return self.context
    
    def log_action(self, action: str, details: Dict[str, Any]):
        """Log an agent action for audit trail"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": self.name,
            "action": action,
            "session_id": self.session_id,
            "details": details
        }
        logger.info(f"Agent Action: {log_entry}")
        return log_entry
