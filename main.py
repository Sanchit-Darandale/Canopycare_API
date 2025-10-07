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

# System prompt
SYSTEM_PROMPT = """
You are CanopyCare Assistant, a helpful and friendly guide for the CanopyCare project on tree plantation and soil protection in Maharashtra. Your role is to answer visitor queries about different plant species, soil types, soil protection methods, and proper tree plantation techniques. Provide clear, short, simple, and educational responses suitable for students, community members, and volunteers. When relevant, explain why certain plants or soils are suitable for specific regions of Maharashtra (Konkan, Western Ghats, Vidarbha, Marathwada, Pune Plateau, North Maharashtra). Encourage sustainable practices, community involvement, and environmental awareness. Always use an informative, positive, and motivating tone and your developer is Sanchit.
"""

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
def get_response(user_text: str) -> str:
    response = model.generate_content(f"{SYSTEM_PROMPT}\n\nUser: {user_text}")
    return response.text


@app.get("/", response_class=HTMLResponse)
async def home():
    return "HelloWorld('Print')"

@app.api_route("/ai", methods=["GET", "POST"])
async def ai_endpoint(request: Request):
    try:
        if request.method == "GET":
            user_text = request.query_params.get("text")
        else:  # POST
            body = await request.json()
            user_text = body.get("text") if body else None

        if not user_text:
            return JSONResponse({"error": "No text provided"}, status_code=400)

        reply = get_response(user_text)

        return JSONResponse({
            "user": user_text,
            "response": reply,
            "credit": "Made by Sanchit"
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
