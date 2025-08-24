import datetime
import os

def format_duration(seconds: float) -> str:
    year = 365 * 24 * 3600
    month = 30 * 24 * 3600
    day = 24 * 3600
    hour = 3600
    minute = 60
    millisecond = 1e-3
    microsecond = 1e-6

    parts = []

    if seconds >= year:
        y = int(seconds // year)
        seconds %= year
        parts.append(f"{y} ปี")
    if seconds >= month:
        m = int(seconds // month)
        seconds %= month
        parts.append(f"{m} เดือน")
    if seconds >= day:
        d = int(seconds // day)
        seconds %= day
        parts.append(f"{d} วัน")
    if seconds >= hour:
        h = int(seconds // hour)
        seconds %= hour
        parts.append(f"{h} ชม.")
    if seconds >= minute:
        mi = int(seconds // minute)
        seconds %= minute
        parts.append(f"{mi} นาที")
    if seconds >= 1:
        s = int(seconds)
        seconds %= 1
        parts.append(f"{s} วินาที")
    if seconds >= millisecond:
        ms = int(seconds // millisecond)
        seconds %= millisecond
        parts.append(f"{ms} มิลลิวินาที")
    if seconds >= microsecond:
        us = int(seconds // microsecond)
        seconds %= microsecond
        parts.append(f"{us} ไมโครวินาที")

    return " ".join(parts) if parts else "0 ไมโครวินาที"

def log(*args):
    log_message = " ".join(str(a) for a in args)
    log_file = "buddhamAI_cli.log"
    timestamp = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    new_entry = f"[{timestamp}] {log_message}"

    # เช็คว่ามีเนื้อหาและลงท้ายด้วย \n หรือไม่
    if os.path.getsize(log_file) > 0:
        with open(log_file, "rb+") as f:
            f.seek(-1, os.SEEK_END)
            last_char = f.read(1)
            if last_char != b"\n":
                new_entry = "\n" + new_entry

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(new_entry)