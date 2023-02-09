
from control.config import DEBUG_OUTPUT

def debug_log(s: str):
    if not DEBUG_OUTPUT:
        return
    
    print(s)