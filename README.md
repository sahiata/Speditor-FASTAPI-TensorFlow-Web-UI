# 🚚 Freight Cost & Time Prediction (FastAPI version)

This project is an AI-based freight route prediction API, built using **FastAPI**, **TensorFlow**, and **MySQL**. It predicts total transport cost and duration based on user-provided inputs related to expenses and time-related factors.

---

## 🔧 Technologies Used

- ✅ FastAPI – web framework
- ✅ Pydantic – input validation
- ✅ TensorFlow – for prediction model (.h5)
- ✅ MySQL – for user and logging database
- ✅ Swagger UI – automatic API documentation (`/docs`)
- ✅ HTML form – for frontend testing
- ✅ API key verification
- ✅ Request logging in the `api_logs` table

---

## 📁 Project Structure

Freight_API_FastAPI/
│
├── main.py # Main FastAPI application
├── model.h5 # Trained TensorFlow model


---

## 🚀 Running the App

In your terminal, run:

```bash
uvicorn main:app --reload

Visit the app at:
📍 http://127.0.0.1:8000

✅ Testing Options
1. Swagger UI
Open http://127.0.0.1:8000/docs to access interactive API documentation.

Example input for /predict:

json
{
  "troškovi": [3420, 10, 15, 1539, 171],
  "vremenski_faktori": [200, 450, 100, 20, 50]
}
👉 Header Required:

makefile

x-api-key: your_api_key_here
2. HTML Form (Frontend)
Access the root URL / to use the user-friendly web form.
It allows you to test predictions without Postman or Swagger.

🔐 API Key Verification
The /predict route requires an active API key (stored in the api_keys table).

If the key is missing or invalid, an HTTP 401 error is returned.

🧾 Logging Requests
Each successful prediction call is logged in the api_logs MySQL table with:

API key

Company name

Input data (JSON)

Prediction result (JSON)

IP address

🧍 User Registration
Users can register via POST /register by providing:

Email

Password

Company name

Passwords are hashed using Werkzeug for security.

⚠️ Notes
Testing was done via HTML form and Swagger UI.

Postman was not used during this phase.

The Flask-based version of the project was completed earlier and is not modified anymore.

👩‍💻 Author
Ivana Kostić
Junior AI Developer
📍 Belgrade, Serbia
