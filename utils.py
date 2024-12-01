from uuid import uuid4

def get_id() -> str:
    return str(uuid4())