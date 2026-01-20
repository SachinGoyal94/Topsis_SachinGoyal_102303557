# TOPSIS Implementation - Sachin Goyal

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![PyPI](https://img.shields.io/badge/PyPI-1.0.0-green.svg)](https://pypi.org/project/topsis-sachingoyal-102303557/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A complete TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) implementation in Python with both **CLI** and **Web Service** interfaces.

---

## 🚀 Quick Start

### 📦 Install from PyPI

```bash
pip install topsis-sachingoyal-102303557==1.0.0
```

### 🌐 Try the Web Interface

Access the live web service at:  
**[https://topsis-sachin-goyal-102303557.vercel.app/](https://topsis-sachin-goyal-102303557.vercel.app/)**

Upload your CSV, enter weights and impacts, and receive results via email!

---

## 📁 Project Structure

```
Topsis_SachinGoyal_102303557/
│
├── topsis/                     # Python package
│   ├── __init__.py
│   └── topsis.py               # Core TOPSIS implementation
│
├── templates/                  # Web frontend
│   └── index.html              # Beautiful web UI
│
├── uploads/                    # Temporary file storage (created automatically)
│
├── main.py                     # FastAPI backend server
├── data.csv                    # Sample input data
├── setup.py                    # Package setup configuration
├── requirements.txt            # Python dependencies
├── sample.env                  # Environment variables template
├── README.md                   # This file
```

---

## 📋 Requirements

- **Python 3.6+**
- **Dependencies:** pandas, numpy, fastapi, mailjet-rest, python-dotenv

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔧 Setup for Local Development

### 1. Clone the Repository

```bash
git clone <https://github.com/SachinGoyal94/Topsis_SachinGoyal_102303557>
cd Topsis_SachinGoyal_102303557
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root with the following:

```env
SENDER_NAME=Your Name
SENDER_EMAIL=your-verified-email@example.com
MJ_APIKEY_PUBLIC=your-mailjet-public-key
MJ_APIKEY_PRIVATE=your-mailjet-private-key
```

> **Note:** A `sample.env` file is provided as a template. Copy it to `.env` and fill in your credentials.

**Required Variables:**
- `SENDER_NAME` - Your name or service name
- `SENDER_EMAIL` - Verified sender email in Mailjet
- `MJ_APIKEY_PUBLIC` - Your Mailjet API public key
- `MJ_APIKEY_PRIVATE` - Your Mailjet API secret key

### 4. Run the Backend Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### 5. Open the Frontend

Navigate to `http://127.0.0.1:8000` in your browser (if serving static files) or open `templates/index.html` directly.

---

## 💻 CLI Usage

### Command Syntax

```bash
python -m topsis.topsis <InputFile> "<Weights>" "<Impacts>" <OutputFile>
```

### Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `InputFile` | Path to input CSV file | `data.csv` |
| `Weights` | Comma-separated numeric weights | `"1,1,1,1,2"` |
| `Impacts` | Comma-separated + or - | `"+,+,-,+,+"` |
| `OutputFile` | Path for output CSV | `result.csv` |

### Example

```bash
python -m topsis.topsis data.csv "1,1,1,1,2" "+,+,+,-,+" result.csv
```

**Output:** Creates `result.csv` with two additional columns:
- `Topsis Score` (higher is better)
- `Rank` (1 = best)

---

## 📊 Input CSV Format

Your CSV must have:
- **First column:** Identifier (e.g., product name, model ID)
- **Remaining columns:** Numeric criteria values

### Example Input

```csv
Name,Cost,Performance,Reliability,Efficiency
ProductA,250,8,9,7
ProductB,200,7,8,9
ProductC,300,9,7,8
```

### Example Output

```csv
Name,Cost,Performance,Reliability,Efficiency,Topsis Score,Rank
ProductA,250,8,9,7,0.534,2
ProductB,200,7,8,9,0.628,1
ProductC,300,9,7,8,0.421,3
```

---

## 🌐 Web Service Usage

1. **Visit:** [https://topsis-sachin-goyal-102303557.vercel.app/](https://topsis-sachin-goyal-102303557.vercel.app/)
2. **Upload** your CSV file
3. **Enter** weights (e.g., `1,1,1`)
4. **Enter** impacts (e.g., `+,+,-`)
5. **Enter** your email address
6. **Submit** and receive results via email

---


## ⚠️ Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Input file not found` | File path is incorrect | Check file path and try again |
| `Invalid email format` | Email is malformed | Use valid email format |
| `Weights and impacts count mismatch` | Different number of weights vs impacts | Ensure equal counts |
| `Impacts must be + or -` | Invalid impact symbol | Use only `+` or `-` |
| `Weights must be numeric` | Non-numeric weight | Use only numbers |
| `All columns must be numeric` | Non-numeric criteria values | Ensure all criteria are numbers |

---

## 📚 How TOPSIS Works

1. **Normalize** the decision matrix using Euclidean normalization
2. **Weight** the normalized matrix
3. **Identify** ideal best and worst solutions
4. **Calculate** Euclidean distances from ideal solutions
5. **Compute** similarity score: `S = D- / (D+ + D-)`
6. **Rank** alternatives by score (higher is better)

---

## 🛠️ Technology Stack

- **Backend:** FastAPI (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Email Service:** Mailjet REST API
- **Package Management:** PyPI
- **Deployment:** 
  - Frontend: Vercel
  - Backend: Render 

---

## 👤 Author

**Sachin Goyal**  

---

## 🔗 Links

- **PyPI Package:** [topsis-sachingoyal-102303557](https://pypi.org/project/topsis-sachingoyal-102303557/1.0.0/)
- **Web App:** [https://topsis-sachin-goyal-102303557.vercel.app/](https://topsis-sachin-goyal-102303557.vercel.app/)
- **GitHub:** [https://github.com/SachinGoyal94/Topsis_SachinGoyal_102303557](https://github.com/SachinGoyal94/Topsis_SachinGoyal_102303557)

---

