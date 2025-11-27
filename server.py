from fastapi import *
import uvicorn
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
import hashlib, secrets, random

index = open("index.html").read()
sitemap = open("sitemap.xml").read()
admin = open("admin.html").read()
support = open("support.html", encoding="utf-8").read()
user = open("user.html").read()
login = open("login.html").read()

legal_characters = list("abcdefghijklmnopqrstuvwxyz0123456789!_")
team_points = {}

db = []
for i in range(50):
    password = "".join([random.choice(legal_characters) for i in range(5)])
    db.append([str(i), f"{random.randint(0, 1000000)/100}$", hashlib.md5(password.encode("utf-8")).hexdigest(), password])

user_pass = {}
user_balance = {}
for i in db:
    user_pass.update({i[0]:i[3]})
    user_balance.update({i[0]:i[1]})

print(db[0])

for i in range(len(db)):
    admin = admin.replace("[DATA]", f"<tr><td>{db[i][0]}</td><td>{db[i][1]}</td><td>{db[i][2]}</td></tr>[DATA]")
admin = admin.replace("[DATA]", "")

app = FastAPI()

@app.get("/")
def read_root():
    return HTMLResponse(index)

@app.get("/index")
def read_root():
    return HTMLResponse(index)

@app.get("/sitemap.xml")
def read_root():
    return PlainTextResponse(sitemap)

@app.get("/support")
def read_root():
    return HTMLResponse(support)

@app.get("/admin")
def read_root():
    return HTMLResponse(admin)

@app.get("/user/{id}/{password}")
def read_root(id, password):
    try:
        if user_pass[id] == password:
            return HTMLResponse(user.replace("[BALANCE]", f"{user_balance[id]}"))
    except:
        return {"error": "not found"}

@app.get("/login")
def read_root():
    return HTMLResponse(login)

@app.get("/flag/{user_id}/{password}/{team}")
def submit_flag(user_id, password, team):
    if user_pass[user_id] == password:
        # append teampoints
        pass
    return [user_id, password, team]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
