from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import re
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from topsis.topsis import topsis   # keep this as per your structure

# Load environment variables
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not SENDER_EMAIL or not EMAIL_PASSWORD:
    raise RuntimeError("Email credentials not set in environment variables")

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Create FastAPI app
app = FastAPI(title="TOPSIS Backend API")

# -------------------- CORS (IMPORTANT) --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://topsis-sachin-goyal-102303557.vercel.app",
        "*"
    ],  # Add your frontend domain(s) here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------------------------------------

# Create uploads folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/health")
def health():
    return {"status": "OK"}


@app.post("/submit")
async def submit(
    file: UploadFile = File(...),
    weights: str = Form(...),
    impacts: str = Form(...),
    email: str = Form(...)
):
    # 1. Validate email
    if not re.match(EMAIL_REGEX, email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    # 2. Validate weights & impacts (keep as strings)
    weights_list = weights.split(",")
    impacts_list = impacts.split(",")

    if len(weights_list) != len(impacts_list):
        raise HTTPException(
            status_code=400,
            detail="Number of weights must be equal to number of impacts"
        )

    for imp in impacts_list:
        if imp not in ["+", "-"]:
            raise HTTPException(
                status_code=400,
                detail="Impacts must be either + or -"
            )

    # 3. Save uploaded file
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(UPLOAD_FOLDER, "result.csv")

    with open(input_path, "wb") as f:
        f.write(await file.read())

    # 4. Run TOPSIS (do NOT change data type)
    topsis(input_path, weights, impacts, output_path)

    # 5. Send result via email
    send_email(email, output_path)

    return {"message": "Result sent to email successfully"}


def send_email(receiver, attachment):
    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver
    msg.set_content("Attached is your TOPSIS result file.")

    with open(attachment, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename="result.csv"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
