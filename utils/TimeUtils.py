from datetime import datetime

def compute_duration(start, end):
    try:
        delta = end - start
        total_minutes = int(delta.total_seconds() // 60)
        hours, minutes = divmod(total_minutes, 60)
        return f"{hours:02d}:{minutes:02d}"
    except:
        return "--:--"

def compute_duration_minutes(start_str, end_str):
    try:
        start_dt = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
        delta = end_dt - start_dt
        return int(delta.total_seconds() // 60)
    except:
        return 0

def format_duration(total_minutes):
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours:02d}:{minutes:02d}"
