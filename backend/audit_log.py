# backend/audit_log.py
import pandas as pd
import os
from datetime import datetime
from config import WORKING_DIR

LOG_FILE = os.path.join(WORKING_DIR, "audit_log.csv")

def log_action(user, role, action, query, status):
    """
    Logs an event to a CSV file.
    """
    new_entry = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "User": user,
        "Role": role,
        "Action": action,
        "Query": query,
        "Status": status
    }
    
    df = pd.DataFrame([new_entry])
    
    if not os.path.exists(LOG_FILE):
        df.to_csv(LOG_FILE, index=False)
    else:
        df.to_csv(LOG_FILE, mode='a', header=False, index=False)

def get_audit_logs():
    if os.path.exists(LOG_FILE):
        return pd.read_csv(LOG_FILE).sort_values(by="Timestamp", ascending=False)
    return pd.DataFrame(columns=["Timestamp", "User", "Role", "Action", "Query", "Status"])