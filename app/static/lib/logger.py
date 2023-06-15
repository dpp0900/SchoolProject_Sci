log_path = "logs/"
logs = {"error": "error.log", "info": "info.log", "debug": "debug.log"}

def write_log(author, text, time, logtype):
    with open(log_path + logs[logtype], "a") as f:
        f.write(f"[{time}] [{logtype}] {author}: {text}\n")