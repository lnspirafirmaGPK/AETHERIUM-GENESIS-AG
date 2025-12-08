import os
import json
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
[span_6](start_span)from anthropic import Anthropic # จาก Anthropic API Wrapper.pdf[span_6](end_span)

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CerebralBridge")

# --- 1. ส่วน Class หลัก (CerebralBridge) ---
class CerebralBridge:
    def __init__(self):
        # [span_7](start_span)โหลด API Key (ควรตั้งใน .env)[span_7](end_span)
        self.anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        # self.gemini_client = ... (ถ้ามี)
        logger.info("🧠 Cerebral Bridge Online: Ready to connect to Akashic Records.")

    def _ask_claude(self, prompt: str, model: str = "claude-3-sonnet-20240229") -> dict:
        """
        [span_8](start_span)Logic จากไฟล์ Anthropic API Wrapper.pdf[span_8](end_span)
        """
        try:
            message = self.anthropic_client.messages.create(
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        [span_9](start_span)"content": f"Based on AETHERIUM-GENESIS protocol, analyze: {prompt}", #[span_9](end_span)
                    }
                ],
                model=model,
            )
            
            # [span_10](start_span)ดึงคำตอบ[span_10](end_span)
            response_content = message.content[0].text if message.content else "No response."
            
            return {
                "success": True,
                "output": response_content,
                "model": message.model,
                [span_11](start_span)"usage": message.usage.to_dict() if hasattr(message, 'usage') else {} #[span_11](end_span)
            }
        except Exception as e:
            return {
                "success": False,
                [span_12](start_span)"output": f"Anthropic Error: {str(e)}", #[span_12](end_span)
                "model": model
            }

    async def consult(self, provider: str, prompt: str):
        """Routing ภายในตัว Bridge"""
        if provider == "claude":
            return self._ask_claude(prompt)
        elif provider == "gemini":
            # return self._ask_gemini(prompt) # รอใส่โค้ด Gemini
            return {"success": True, "output": "[Mock] Gemini Thinking...", "model": "gemini-mock"}
        else:
            return {"success": False, "output": "Unknown Provider"}

# --- 2. ส่วน Web Server (FastAPI) เพื่อรองรับ API Gateway.pdf ---
# [span_13](start_span)API Gateway[span_13](end_span) จะยิงมาที่ http://python-service:8080/claude

app = FastAPI()
bridge = CerebralBridge()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/claude")
async def handle_claude(request: PromptRequest):
    logger.info(f"bridge received claude request: {request.prompt[:20]}...")
    result = await bridge.consult("claude", request.prompt)
    
    # [span_14](start_span)ส่งคืน Format เดียวกับที่ API Gateway.pdf ต้องการ[span_14](end_span)
    return {
        "success": result["success"],
        "output": result["output"],
        "type": "text",
        "meta": {
            "model": result.get("model", "claude-unknown")
        }
    }

# วิธีรัน: uvicorn core.cerebral_bridge_service:app --host 0.0.0.0 --port 8080
