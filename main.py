from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
import google.generativeai as genai
import os

# Load API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Use correct model
model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response generator
def get_response(syspt, user_text: str) -> str:
    response = model.generate_content(f"{syspt}\n\nUser: {user_text}")
    return response.text


@app.get("/", response_class=HTMLResponse)
async def home():
    return "HelloWorld('Print')"

@app.api_route("/ai", methods=["GET", "POST"])
async def ai_endpoint(request: Request):
    try:
        if request.method == "GET":
            user_text = request.query_params.get("text")
            sp = request.query_params.get("system_prompt")
        else:  # POST
            body = await request.json()
            user_text = body.get("text") if body else None
            sp = body.get("system_prompt") if body else None

        if not user_text or not sp:
            return JSONResponse({"error": "No text / system prompt provided"}, status_code=400)

        reply = get_response(sp, user_text)

        return JSONResponse({
            "user": user_text,
            "response": reply,
            "credit": "Made by Sanchit"
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
