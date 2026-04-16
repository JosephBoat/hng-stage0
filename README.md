# HNG Stage 0 – Name Classification API

> A simple REST API built with Django and Django REST Framework that integrates with the [Genderize API](https://genderize.io) to classify a given name and return structured metadata including gender prediction, probability, and confidence level.

🚀 **Live API:** [https://hng-stage0-weld.vercel.app/](https://hng-stage0-weld.vercel.app/)

---

## Endpoint

### Classify Name

```
GET /api/classify?name={name}
```

**Example Request**

```
GET /api/classify?name=john
```

**Success Response `200 OK`**

```json
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-01T12:00:00Z"
  }
}
```

---

## Processing Rules

| Field | Description |
|---|---|
| `gender` | Extracted from external API |
| `probability` | Extracted from external API |
| `sample_size` | Renamed from `count` |
| `is_confident` | `probability >= 0.7` AND `sample_size >= 100` |
| `processed_at` | Generated dynamically in UTC (ISO 8601) |

---

## Error Responses

**`400 Bad Request`** — Missing or empty name parameter

```json
{ "status": "error", "message": "Missing or empty name parameter" }
```

**`422 Unprocessable Entity`** — Invalid input or no prediction available

```json
{ "status": "error", "message": "No prediction available for the provided name" }
```

**`500 / 502 Server Error`** — Upstream or internal failure

```json
{ "status": "error", "message": "Upstream service failure" }
```

---

## Edge Case Handling

If Genderize returns `gender: null` or `count: 0`, the API responds with:

```json
{ "status": "error", "message": "No prediction available for the provided name" }
```

---

## CORS Support

CORS is enabled globally:

```
Access-Control-Allow-Origin: *
```

This allows external systems (including graders) to access the API without restrictions.

---

## Tech Stack

- **Python** / **Django** / **Django REST Framework**
- **Requests** (for external API calls)
- **Vercel** (deployment)

---

## Installation & Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/JosephBoat/hng-stage0.git
cd hng-stage0
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/Scripts/activate   # Windows
# source venv/bin/activate     # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

---

## Project Structure

```
hng-stage0/
│
├── api/
│   ├── views.py
│   ├── urls.py
│   └── index.py
│
├── backend/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── requirements.txt
├── vercel.json
└── README.md
```

---

## Deployment

This project is deployed on Vercel using a serverless Python configuration.

| Detail | Value |
|---|---|
| Entry point | `api/index.py` |
| Framework | Django (WSGI-based) |
| Build | Vercel Python runtime |
| Routes | Configured via `vercel.json` |

---

## Performance Requirements

- Response time under 500ms (excluding external API latency)
- Stateless request handling
- Supports concurrent requests

---

## Author

**Joseph Boateng** — Backend Engineer  
HNG Internship Stage 0 Submission
