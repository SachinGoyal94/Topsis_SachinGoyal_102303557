from flask import Flask, render_template, request
import os, re, smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from topsis import topsis

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# basic filename sanitizer
def secure_filename(name):
    return re.sub(r"[^A-Za-z0-9_.-]", "_", name)



@app.route('/submit', methods=['POST'])
def submit():
    try:
        file = request.files['file']
        weights = request.form['weights']
        impacts = request.form['impacts']
        email = request.form['email']

        if not re.match(EMAIL_REGEX, email):
            return ("Invalid Email Format", 400)

        # Validate weights and impacts lengths and formats without converting to lists
        w_parts = [w.strip() for w in weights.split(',') if w.strip()]
        i_parts = [i.strip() for i in impacts.split(',') if i.strip()]

        if len(w_parts) != len(i_parts):
            return ("Weights and impacts count mismatch", 400)

        for i in i_parts:
            if i not in ['+', '-']:
                return ("Impacts must be + or -", 400)

        # ensure weights are numeric
        try:
            _ = [float(x) for x in w_parts]
        except Exception:
            return ("Weights must be numeric", 400)

        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_path = os.path.join(UPLOAD_FOLDER, "result.csv")
        file.save(input_path)

        # topsis() in package expects weights and impacts as comma-separated strings
        topsis(input_path, ','.join(w_parts), ','.join(i_parts), output_path)

        send_email(email, output_path)
        return ("Result sent to your email successfully!", 200)
    except Exception as e:
        return (f"Internal error: {str(e)}", 500)


def send_email(receiver, attachment):
    if not SENDER_EMAIL or not EMAIL_PASSWORD:
        raise RuntimeError("Email sender credentials not configured")

    msg = EmailMessage()
    msg['Subject'] = 'TOPSIS Result'
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver
    msg.set_content("Attached is your TOPSIS result file.")

    with open(attachment, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application',
                           subtype='octet-stream', filename=os.path.basename(attachment))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)