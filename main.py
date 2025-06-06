from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
from pydantic import BaseModel, Field
import tensorflow as tf
import numpy as np
import mysql.connector
import json
from fastapi import Form
from werkzeug.security import generate_password_hash

# ✅ Učitavanje modela
model = tf.keras.models.load_model("model.h5")
print("✅ Model je učitan.")

# ✅ Povezivanje sa MySQL bazom
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Bugarin12345",
    database="spedicija"
)
cursor = connection.cursor(dictionary=True)
print("✅ Povezano sa MySQL bazom.")

# ✅ FastAPI aplikacija
app = FastAPI(title="FastAPI Spedicija API")

@app.get("/status")
def get_status():
    return {"message": "FastAPI je aktivan! 🎯"}

# ✅ Pydantic model za JSON predikciju
class PredictInput(BaseModel):
    troskovi: Annotated[list[float], Field(alias="troškovi", min_length=5, max_length=5)]
    vremenski_faktori: Annotated[list[float], Field(min_length=5, max_length=5)]

    class Config:
        validate_by_name = True
        json_schema_extra = {
            "example": {
                "troškovi": [3420, 10, 15, 1539, 171],
                "vremenski_faktori": [200, 450, 100, 20, 50]
            }
        }

# ✅ HTML forma na /
@app.get("/", response_class=HTMLResponse)
def read_root_html(greska: int = 0):
    greska_msg = ""
    if greska == 1:
        greska_msg = "<p style='color:red;'>❌ Moraš uneti tačno po 5 vrednosti.</p>"
    elif greska == 2:
        greska_msg = "<p style='color:red;'>❌ Došlo je do greške u obradi podataka.</p>"

    return f"""
    <html>
        <head><title>Spedicija AI Predikcija</title></head>
        <body>
            <h2>Predikcija troškova i vremena putovanja</h2>
            {greska_msg}
            <form action="/predict-ui" method="post">
                <label>Troškovi (5 vrednosti, zarezom):</label><br>
                <input type="text" name="troskovi" value="3420,10,15,1539,171"/><br>
                <label>Vremenski faktori (5 vrednosti, zarezom):</label><br>
                <input type="text" name="vremenski_faktori" value="200,450,100,20,50"/><br><br>
                <input type="submit" value="Pošalji"/>
            </form>
        </body>
    </html>
    """

# ✅ Prikaz rezultata GET /result
@app.get("/result", response_class=HTMLResponse)
def show_result(trošak: float = 0.0, vreme: float = 0.0):
    return f"""
    <html>
        <head><title>Rezultat</title></head>
        <body>
            <h3>✅ Rezultat:</h3>
            <p>Ukupni trošak: {trošak:.2f} €</p>
            <p>Vreme putovanja: {vreme:.2f} h</p>
            <a href="/">⬅ Nazad</a>
        </body>
    </html>
    """

# ✅ Obrada forme POST → /predict-ui → redirect na /result
@app.post("/predict-ui")
def predict_ui(
    request: Request,
    troskovi: str = Form(...),
    vremenski_faktori: str = Form(...)
):
    try:
        troskovi_lista = list(map(float, troskovi.split(",")))
        vremenski_lista = list(map(float, vremenski_faktori.split(",")))

        if len(troskovi_lista) != 5 or len(vremenski_lista) != 5:
            return HTMLResponse("<h3>❌ Greška: Moraš uneti tačno po 5 vrednosti.</h3>")

        combined_input = troskovi_lista + vremenski_lista
        ulaz = np.array(combined_input).reshape(1, -1)
        predikcija = model.predict(ulaz)

        return HTMLResponse(f"""
        <h3>✅ Rezultat:</h3>
        <p>Ukupni trošak: {float(predikcija[0][0]):.2f} €</p>
        <p>Vreme putovanja: {float(predikcija[0][1]):.2f} h</p>
        <a href="/">⬅ Nazad</a>
        """)

    except Exception as e:
        return HTMLResponse(f"<h3>❌ Greška: {str(e)}</h3>")


# ✅ JSON API endpoint sa API ključem
@app.post("/predict")
def predict(data: PredictInput, request: Request, x_api_key: str = Header(None)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API ključ je obavezan")

    cursor.execute("SELECT * FROM api_keys WHERE api_key = %s AND is_active = TRUE", (x_api_key,))
    api_user = cursor.fetchone()
    if not api_user:
        raise HTTPException(status_code=401, detail="Nevažeći API ključ")

    combined_input = data.troskovi + data.vremenski_faktori
    ulaz = np.array(combined_input).reshape(1, -1)
    predikcija = model.predict(ulaz)

    rezultat = {
        "ukupni_trošak": float(predikcija[0][0]),
        "vreme_putovanja": float(predikcija[0][1])
    }

    ip = request.client.host
    cursor.execute(
        "INSERT INTO api_logs (api_key, firma, ulaz_json, rezultat_json, ip_adresa) VALUES (%s, %s, %s, %s, %s)",
        (x_api_key, api_user["firma"], json.dumps(data.dict(by_alias=True)), json.dumps(rezultat), ip)
    )
    connection.commit()

    return rezultat

# ✅ Registracija korisnika
class RegisterInput(BaseModel):
    email: str
    password: str
    firma: str

@app.post("/register")
def register(user: RegisterInput):
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Korisnik već postoji.")

    hashed_password = generate_password_hash(user.password)
    cursor.execute(
        "INSERT INTO users (email, password_hash, firma) VALUES (%s, %s, %s)",
        (user.email, hashed_password, user.firma)
    )
    connection.commit()

    return {"message": "Uspešno registrovan korisnik."}
