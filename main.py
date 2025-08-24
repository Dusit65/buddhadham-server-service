# main.py
import sys
import os
import json
from multiprocessing import Pool, freeze_support
from fastapi import FastAPI, Request
import uvicorn
import BuddhamAI_cli

# ---------- Pool Worker ----------
def run_ask_cli(args: list[str]) -> dict:
    old_sys_argv = sys.argv
    try:
        sys.argv = ["BuddhamAI_cli.py"] + args
        result = BuddhamAI_cli.ask_cli()  # ask_cli ต้อง return dict
        return result
    except SystemExit:
        return {"data": "Process exited"}
    finally:
        sys.argv = old_sys_argv

# ---------- FastAPI ----------
app = FastAPI()

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    args = data.get("args", [])
    # จะเรียก pool จาก main
    result = app.pool.apply(run_ask_cli, (args,))
    json_output = json.dumps(result, ensure_ascii=False)
    print(json_output, flush=True)
    return result

# ---------- Main ----------
if __name__ == "__main__":
    freeze_support()  # สำหรับ Windows
    process_count = int(os.getenv("processes", 1))
    # สร้าง pool แล้วเก็บไว้ใน app object
    app.pool = Pool(processes=process_count)
    print(app.pool._processes)
    uvicorn.run(app, host="0.0.0.0", port=8000)