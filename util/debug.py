
from control.config import DEBUG_MUST_INCLUDE, DEBUG_OUTPUT

def debug_log(s: str):
    if not DEBUG_OUTPUT or DEBUG_MUST_INCLUDE not in s:
        return
    
    print(s)