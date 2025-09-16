import os
import time
import asyncio
import subprocess
from fastapi import FastAPI, Request
import socketio
import dotenv
import aiohttp
from debugger import log
import uvicorn
import json

dotenv.load_dotenv()
app = FastAPI()

# ---------- Socket ----------
socket = socketio.Client()
socket.connect(f"http://{os.getenv('API_SERVER')}:{os.getenv('API_SERVER_PORT')}")

def socket_emit(event, data):
    try:
        socket.emit(event, data)
    except Exception as e:
        log(f"[Socket] Emit error: {e}")

# ---------- Task Manager ----------
class TaskManager:
    def __init__(self):
        self.queue = []           # list ของ {taskId, args, chatId}
        self.running_task = None
        self.results = {}         
        self.status = {}          
        self.processes = {}       

    def add_task(self, taskId, args, chatId):
        self.queue.append({"taskId": taskId, "args": args, "chatId": chatId})
        self.status[taskId] = "queued"
        log(f"[TaskManager] Add task {taskId} with chatId={chatId} args={args}")

    def cancel_task(self, taskId):
        # cancel queued
        for i, task in enumerate(self.queue):
            if task["taskId"] == taskId:
                self.queue.pop(i)
                self.status[taskId] = "cancelled"
                log(f"[TaskManager] Cancel queued task {taskId}")
                return True
        # cancel running
        proc = self.processes.get(taskId)
        if proc and proc.poll() is None:
            proc.terminate()
            self.status[taskId] = "cancelled"
            log(f"[TaskManager] Terminated running task {taskId}")
            return True
        return False

    def get_status(self, taskId):
        return self.status.get(taskId)

    def get_result(self, taskId):
        return self.results.get(taskId)

    async def saveAnswer(self, taskId, chatId, data_obj):
        """ส่งคำตอบ AI ไป /qNa/answer"""
        api_url = f"http://{os.getenv('API_SERVER')}:{os.getenv('API_SERVER_PORT')}/qNa/answer"
        payload = {
            "taskId": taskId,
            "chatId": chatId,
            "qNaWords": f"{data_obj['data'].get('answer', '')}\n\nอ้างอิงข้อมูลจาก {data_obj['data'].get('references', '')}\n\nใช้เวลา {data_obj['data'].get('duration', '')}"
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, json=payload) as resp:
                    resp_json = await resp.json()
                    log(f"[TaskManager] AI answer sent to /qNa/answer: {resp_json}")
        except Exception as e:
            log(f"[TaskManager] Failed to send AI answer: {e}")

    async def process_next(self):
        if self.running_task is not None or not self.queue:
            return

        task = self.queue.pop(0)
        taskId, args, chatId = task["taskId"], task["args"], task["chatId"]
        self.running_task = task
        self.status[taskId] = "running"
        log(f"[TaskManager] Start task {taskId} chatId={chatId}")

        try:
            proc = subprocess.Popen(
                ["python", "-Xutf8", "BuddhamAI_cli.py"] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                env={**os.environ, "PYTHONUTF8": "1"}
            )
            self.processes[taskId] = proc

            out, err = await asyncio.get_event_loop().run_in_executor(None, proc.communicate)

            if self.status.get(taskId) == "cancelled":
                self.results[taskId] = {"status": "cancelled", "args": args, "chatId": chatId}
            elif proc.returncode == 0:
                try:
                    data_obj = json.loads(out) if out.strip().startswith("{") else {"answer": out}
                except Exception:
                    data_obj = {"answer": out}

                self.results[taskId] = {"status": "done", "data": data_obj, "args": args, "chatId": chatId}
                self.status[taskId] = "done"
                # socket_emit("message", str({data_obj['data']['answer']} + '\n\nใช้เวลา ' + {data_obj['data']['duration']}))
                socket_emit("message", f"{data_obj['data'].get('answer', '')}\n\nอ้างอิงข้อมูลจาก {data_obj['data'].get('references', '')}\n\nใช้เวลา {data_obj['data'].get('duration', '')}")
                log(f"[TaskManager] Task {taskId} done")

                # ส่งไป /qNa/answer
                # log(f"dataObj: {data_obj}")
                # log(f"answer: {data_obj['data']['answer']}" + '\n\nใช้เวลา ' + f" duration: {data_obj['data']['duration']}")
                await self.saveAnswer(taskId, chatId, data_obj)
            else:
                self.results[taskId] = {"status": "error", "error": err, "args": args, "chatId": chatId}
                self.status[taskId] = "error"
                log(f"[TaskManager] Task {taskId} error: {err}")

        except Exception as e:
            self.results[taskId] = {"status": "error", "error": str(e), "args": args, "chatId": chatId}
            self.status[taskId] = "error"
            log(f"[TaskManager] Task {taskId} exception: {e}")

        finally:
            self.running_task = None
            self.processes.pop(taskId, None)

# ---------- Background loop ----------
@app.on_event("startup")
async def startup_event():
    async def loop():
        while True:
            await app.task_manager.process_next()
            await asyncio.sleep(0.5)
    asyncio.create_task(loop())

# ---------- FastAPI endpoints ----------
@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    log(f"[API] /ask received: {data}")
    args = data.get("args", [])
    chatId = data.get("chatId")
    taskId = str(int(time.time() * 1000))
    app.task_manager.add_task(taskId, args, chatId)
    return {"args": args, "taskId": taskId, "status": "queued", "chatId": chatId}

@app.post("/cancel/{taskId}")
async def cancel(taskId: str):
    success = app.task_manager.cancel_task(taskId)
    status = app.task_manager.get_status(taskId)
    return {"taskId": taskId, "status": status, "cancelled": success}

@app.get("/status/{taskId}")
async def status(taskId: str):
    res = app.task_manager.get_result(taskId)
    status_val = app.task_manager.get_status(taskId)
    if status_val is None:
        return {"error": "task not found", "taskId": taskId}
    return res if res else {"taskId": taskId, "status": status_val}

# ---------- Main ----------
if __name__ == "__main__":
    app.task_manager = TaskManager()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("AI_SERVER_PORT", 8000)))