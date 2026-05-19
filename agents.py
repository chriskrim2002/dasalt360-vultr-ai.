import os, requests, base64
K = os.getenv("VULTR_INFERENCE_API_KEY")
U = "https://api.vultrinference.com/v1"
class DasaltAgent:
    def __init__(self, ins): self.ins = ins
    def chat(self, p, img=None):
        m = "llama-3.2-11b-vision-instruct" if img else "llama-3.1-70b-instruct-fp8"
        sys = f"{self.ins} Output ONLY elegant, neat PhD-level English. NO thinking tags. Use ₦."
        msgs = [{"role": "system", "content": sys}]
        if img: msgs.append({"role": "user", "content": [{"type": "text", "text": p}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}}]})
        else: msgs.append({"role": "user", "content": p})
        r = requests.post(f"{U}/chat/completions", headers={"Authorization": f"Bearer {K}"}, json={"model": m, "messages": msgs, "temperature": 0.1})
        txt = r.json()['choices'][0]['message']['content']
        return txt.split("</think>")[-1].strip() if "</think>" in txt else txt
class CFO(DasaltAgent):
    def __init__(self): super().__init__("CFO. Logic: 1400 Rate, 7000 Transit PER UNIT, 20% Margin. Format as a professional Executive Brief.")
    
