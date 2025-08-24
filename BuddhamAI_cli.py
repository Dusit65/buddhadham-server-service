# buddhamAI_cli.py
import sys
import os
import pickle
import json
import time
import subprocess
import traceback
import numpy as np
import faiss
import ollama
import hashlib
from reDocuments import ensure_embeddings_up_to_date
from debugger import format_duration, log

try:
    def clear_screen():
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Unix/Linux/Mac
            os.system('clear')
    
    log_file = "buddhamAI_cli.log"
    required_models = ["gpt-oss:20b", "nomic-embed-text:v1.5"]
    EMB_PATH = "embeddings.npy"
    META_PATH = "metadata.pkl"
    DOCS_ALL_PATH = "documents/documentsPkl/documents_all.pkl"
    start = None
    end = None
    STATUS_FILE = "embed_status.json"
    
    if not os.path.exists(log_file):
        open(log_file, "w").close()
    with open(log_file, "r+") as f:
        f.truncate(0)

    def get_installed_models():
        # ลองใช้ --json ก่อน
        try:
            result = subprocess.run(
            ["ollama", "list", "--json"],
            capture_output=True,
            text=True
        )
            if result.returncode == 0 and result.stdout.strip().startswith("["):
                return [m["name"] for m in json.loads(result.stdout)]
        except Exception:
            pass  # ถ้าพัง ให้ไปใช้วิธี parse ธรรมดา

        # ใช้วิธีอ่านแบบข้อความปกติ
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True
        )
        lines = result.stdout.strip().split("\n")
        models = []
        for line in lines[1:]:  # ข้าม header
            parts = line.split()
            if parts:
                models.append(parts[0])
        return models

    def check_and_pull_models(models_to_check):
        try:
            local_model_names = get_installed_models()
            missing_models = [m for m in models_to_check if m not in local_model_names]

            if missing_models:
                for model in missing_models:
                    log(f"📥 กำลังโหลดโมเดล {model} ...")
                    subprocess.run(["ollama", "pull", model], check=True)
                    log(f"✅ โหลด {model} เสร็จแล้ว")
            else:
                log("✅ มี Models ครบแล้ว")
        except Exception:
            log("❌ เกิดข้อผิดพลาด:\n" + traceback.format_exc())
            exit(1)

    def flatten_docs(raw):
        docs = []
        for book_name, chapters in raw.items():
            for chapter_key, pages in chapters.items():
                for page_key, content in pages.items():
                    chapter_num = int(chapter_key.replace("chapter ", ""))
                    docs.append({
                        "bookname": book_name,
                        "chapter": chapter_num,
                        "content": content
                    })
        return docs

    def load_embeddings_and_metadata():
        log(f"ใช้ embeddings {required_models[1]}")
        log(f"โหลด {EMB_PATH} และ {META_PATH}")
        embeddings = np.load(EMB_PATH)
        with open(META_PATH, 'rb') as f:
            metadata = pickle.load(f)
        return embeddings, metadata

    def search(query, index, metadata, top_k, max_distance):
        log(f"กำลังค้นหาข้อมูลอ้างอิงสำหรับ: {query} ด้วย top_k={top_k} และ max_distance={max_distance}")

        # สร้าง embedding ของ query
        q_emb = ollama.embeddings(model='nomic-embed-text:v1.5', prompt=query)['embedding']
        q_emb = np.array([q_emb], dtype='float32')

        # ค้นหา nearest neighbors
        distances, ids = index.search(q_emb, top_k)
        log(f"ค้นหา nearest neighbors เจอ {len(ids[0])} รายการ")

        results = []
        filtered_out_results = []
        seen_docs = set()

        for i, idx in enumerate(ids[0]):
            if idx >= len(metadata):
                continue
            dist = distances[0][i]
            doc = metadata[idx]

            # สร้าง hash จาก content
            doc_hash = hashlib.md5(doc['content'].encode('utf-8')).hexdigest()

            # ถ้าซ้ำหรือเกิน max_distance
            if doc_hash in seen_docs or (max_distance is not None and dist > max_distance):
                filtered_out_results.append((doc, dist, idx))
                log(f"index={idx}, distance={dist:.4f} ถูกตัดออก")
                continue

            # เก็บผลลัพธ์พร้อม index และ distance
            results.append({
                "doc": doc,
                "distance": dist,
                "index": idx
            })
            seen_docs.add(doc_hash)

            # log index และ distance ของแต่ละรายการ
            log(f"index={idx}, distance={dist:.4f}")

        log(f"ค้นหาข้อมูลอ้างอิง ได้ผลลัพธ์ {len(results)} รายการ ได้แก่ {short_references([r['doc'] for r in results])}")

        if filtered_out_results:
            contexts = [f"{doc['content']}" for doc, _, _ in filtered_out_results]
            full_context = "\n".join(contexts)
            log(f"ข้อมูลอ้างอิงที่ถูกตัดออกจำนวน {len(filtered_out_results)} รายการ ได้แก่ {short_references([doc for doc, _, _ in filtered_out_results])}")
            log(f"ข้อมูลอ้างอิงที่ถูกตัดออก:\n{full_context}")

        return results
    def short_references(metadata):
        sorted_docs = sorted(metadata, key=lambda d: (d['bookName'], d['chapter']))
        return ", ".join([
            f"{d['bookName']} บท {d['chapter']}"
            for d in sorted_docs
        ])

    def check_rejection_message(text: str) -> bool:
        rejection_phrases = [
            "ไม่สามารถตอบคำถาม"
        ]
        return any(phrase in text for phrase in rejection_phrases)

    def ask(query, index, metadata, top_k=None, max_distance=None):
        top_k=len(query) if top_k is None else top_k
        global start
        results = search(query, index, metadata, top_k, max_distance=max_distance)

        contexts = [r["doc"]["content"] for r in results]
        
        full_context = "\n".join(contexts)
        prompt = f"""ข้อมูลอ้างอิง:\n{full_context}\nคำถาม: {query}"""
        model = 'gpt-oss:20b'
        log(f"กำลังถามโมเดล: \"{model}\" ด้วย prompt:\n{prompt}")
        start = time.perf_counter()
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": "คุณคือผู้ช่วยที่ใช้ข้อมูลอ้างอิงจากเอกสารหลายแหล่ง ซึ่งจะช่วยตอบคำถามเกี่ยวกับพระพทธรรมเท่านั้นถ้าได้รับคำถามนอกเหนือจากนี้ให้ตอบว่า ขออภัยครับ...ผมไม่สามารถตอบคำถามนี้ได้....เนื่องจากผมถูกออกแบบมาเพื่อให้ตอบคำถามเกี่ยวกับพระพุทธธรรมเท่านั้น"},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response['message']['content']
        ref_text = short_references([r["doc"] for r in results])
        end = time.perf_counter()
        processing_time = format_duration(end - start)
        log(f"ถามโมเดล \"{model}\" เสร็จสิ้น ใช้เวลา {processing_time}")
        if not check_rejection_message(answer):
            return {
                "answer": answer,
                "references": ref_text,
                "duration": processing_time
            }
        else:
            return {
                "answer": answer,
                "references": "",
                "duration": 0
            }
    
    def read_last_embed_time():
        if not os.path.exists(STATUS_FILE):
            return "1970-01-01 00:00:00"
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)["last_embed_time"]

    def init_bot():
        log("เช็คอัพเดตข้อมูล")
        embeddings, metadata = ensure_embeddings_up_to_date()
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        return index, metadata

    def parse_args(argv):
        message = None
        top_k = None
        max_distance = None

        i = 0
        while i < len(argv):
            arg = argv[i]
            if arg == '-k' and i + 1 < len(argv):
                try:
                    top_k = int(argv[i+1])
                except ValueError:
                    top_k = None
                i += 2
            elif arg == '-d' and i + 1 < len(argv):
                try:
                    max_distance = float(argv[i+1])
                except ValueError:
                    max_distance = None
                i += 2
            elif not arg.startswith('-') and message is None:
                message = arg
                i += 1
            else:
                i += 1

        return message, top_k, max_distance


    def ask_cli(argv=None):
        log("เริ่มต้น BuddhamAI")
        check_and_pull_models(required_models)

        if argv is None:  # ถ้าไม่ส่งมา → ใช้ sys.argv
            argv = sys.argv[1:]

        message, top_k, max_distance = parse_args(argv)

        if message is None or message.strip() == "":
                result = {"answer": "กรุณาถามคำถาม", "references": "ไม่มี", "duration": 0}
                data = {"data": result}
                json_str = json.dumps(data, ensure_ascii=False)
                log(json_str)
                print(json_str)
                return data  # ไม่ exit ตรงนี้ เพื่อให้ pool ใช้ได้

        index, metadata = init_bot()
        result = ask(message, index, metadata, top_k=top_k, max_distance=max_distance)

        data = {"data": result}
        json_str = json.dumps(data, ensure_ascii=False)
        log(json_str)
        print(json_str)
        return data  # return กลับไปให้ main.py ใช้

    if __name__ == "__main__":
        ask_cli()
        
except Exception:
    err_msg = traceback.format_exc()
    try:
        log("เกิดข้อผิดพลาด: " + err_msg)
        data = {"answer": f"เกิดข้อผิดพลาด: {err_msg}", "status": 500}
        json_str = json.dumps(data, ensure_ascii=False)
        log(json_str)
        print(json_str)
    except:
        log("เกิดข้อผิดพลาด: " + err_msg)
        data = {"answer": f"เกิดข้อผิดพลาด: {err_msg}", "status": 500}
        json_str = json.dumps(data, ensure_ascii=False)
        log(json_str)
        print(json_str)
        pass
    sys.exit(1)