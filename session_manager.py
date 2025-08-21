# session_manager.py
import uuid

# Store chat history in memory for now
_sessions = {}

def get_session(session_id: str = None):
    """Get or create a session by ID"""
    if session_id and session_id in _sessions:
        return session_id, _sessions[session_id]

    # create new session
    new_id = str(uuid.uuid4())
    _sessions[new_id] = []
    return new_id, _sessions[new_id]

def update_session(session_id: str, question: str, answer: str):
    """Save Q/A to session"""
    if session_id not in _sessions:
        _sessions[session_id] = []
    _sessions[session_id].append({"question": question, "answer": answer})
