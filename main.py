import os, requests, base64, uvicorn, shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from agents import CFO
app = FastAPI()
c = CFO()
K = os.getenv("VULTR_INFERENCE_API_KEY")
@app.get("/")
def home(): return {"status": "Dasalt 360 PhD AI Live"}
@app.post("/cost-new-inventory")
async def costing(text: str = Form("Requesting analysis"), file: UploadFile = File(None)):
    img = base64.b64encode(await file.read()).decode('utf-8') if file else None
    return {"financial_brief": c.chat(text, img)}
@app.post("/voice-to-voice-costing")
async def v2v(audio: UploadFile = File(...)):
    tmp = f"t_{audio.filename}"
    with open(tmp, "wb") as b: shutil.copyfileobj(audio.file, b)
    with open(tmp, "rb") as f:
        r_stt = requests.post("https://api.vultrinference.com/v1/audio/transcriptions", headers={"Authorization": f"Bearer {K}"}, files={"file": f}, data={"model": "whisper-1"})
    txt = r_stt.json().get("text", "Financial update")
    ai_msg = c.chat(txt)
    r_tts = requests.post("https://api.vultrinference.com/v1/audio/speech", headers={"Authorization": f"Bearer {K}"}, json={"model": "tts-1", "input": ai_msg, "voice": "alloy"})
    with open("o.mp3", "wb") as f: f.write(r_tts.content)
    os.remove(tmp)
    return FileResponse("o.mp3", media_type="audio/mpeg")
if __name__ == "__main__": uvicorn.run(app, host="0.0.0.0", port=8000)
