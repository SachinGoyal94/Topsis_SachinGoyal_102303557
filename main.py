from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import re
from dotenv import load_dotenv
from topsis.topsis import topsis
from mailjet_rest import Client
import base64

# Load environment variables
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME", "TOPSIS Service")
MJ_APIKEY_PUBLIC = os.getenv("MJ_APIKEY_PUBLIC")
MJ_APIKEY_PRIVATE = os.getenv("MJ_APIKEY_PRIVATE")

if not SENDER_EMAIL or not MJ_APIKEY_PUBLIC or not MJ_APIKEY_PRIVATE:
    raise RuntimeError("Mailjet credentials not set in environment variables")

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Create FastAPI app
app = FastAPI(title="TOPSIS Backend API")

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for assignment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------------------------

# Upload folder
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
    try:
        # 1. Validate email
        if not re.match(EMAIL_REGEX, email):
            raise HTTPException(status_code=400, detail="Invalid email format")

        # 2. Validate weights & impacts
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

        # 4. Run TOPSIS
        topsis(input_path, weights, impacts, output_path)

        # 5. Send email
        send_email(email, output_path)

        return {"message": "Result sent to email successfully"}
    except RuntimeError as e:
        # Catch Mailjet errors and return to frontend
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


def send_email(receiver, attachment):
    mailjet = Client(auth=(MJ_APIKEY_PUBLIC, MJ_APIKEY_PRIVATE), version="v3.1")

    with open(attachment, "rb") as f:
        encoded_file = base64.b64encode(f.read()).decode()

    data = {
        "Messages": [
            {
                "From": {
                    "Email": SENDER_EMAIL,
                    "Name": SENDER_NAME
                },
                "To": [
                    {
                        "Email": receiver,
                        "Name": receiver.split("@")[0]
                    }
                ],
                "Subject": "TOPSIS Result",
                "TextPart": "Attached is your TOPSIS result file.",
                "HTMLPart": "<h3>Your TOPSIS result is attached.</h3>",
                "Attachments": [
                    {
                        "ContentType": "text/csv",
                        "Filename": "result.csv",
                        "Base64Content": encoded_file
                    }
                ]
            }
        ]
    }

    result = mailjet.send.create(data=data)
    resp = result.json()
    print("Mailjet response:", result.status_code, resp)
    # Mailjet returns 201 on success, but also check JSON for status
    if result.status_code not in (200,201) or not resp.get("Messages") or resp["Messages"][0].get("Status") != "success":
        raise RuntimeError(f"Mailjet error: {result.status_code} {resp}")
