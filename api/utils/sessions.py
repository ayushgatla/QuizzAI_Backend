from uuid import uuid4
from typing import Dict, List, Optional
from datetime import datetime
from utils.crew import agent_maneger

class SessionManager:
    def __init__(self):
      
        self.sessions: Dict[str, dict] = {}
    
    def create_session(self) -> tuple[str, dict]:
       
        chat_id = str(uuid4())
        crew_session_id = str(uuid4())
        agents = agent_maneger.create_agent(chat_id)
        
        session_data = {
            "chat_id": chat_id,
            "crew_session_id": chat_id,
            "pdf_text": None,
            "pdf_filename": None,
            "processed": False,
            "messages": [],  # Store chat history
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        self.sessions[chat_id] = session_data
    
        return chat_id, session_data
    
    def get_session(self, chat_id: str) -> Optional[dict]:
       
        return self.sessions.get(chat_id)
    
    def update_session(self, chat_id: str, updates: dict) -> bool:
        
        if chat_id not in self.sessions:
            return False
        
        self.sessions[chat_id].update(updates)
        self.sessions[chat_id]["updated_at"] = datetime.now().isoformat()
        return True
    
    def add_message(self, chat_id: str, message: dict) -> bool:
        
        if chat_id not in self.sessions:
            return False
        
        self.sessions[chat_id]["messages"].append({
            **message,
            "timestamp": datetime.now().isoformat()
        })
        return True
    
    def delete_session(self, chat_id: str) -> bool:
       
        if chat_id in self.sessions:
            del self.sessions[chat_id]
            return True
        return False


session_manager = SessionManager()