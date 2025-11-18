# GRACIAS PREP - Système de présence avec login pour tous les employés
from flask import Flask, render_template_string, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key_123"  # Pour gérer les sessions

# ---------- UTILISATEURS / LOGIN ----------
# Chaque employé peut se connecter avec son email et son code comme mot de passe
users = {
    "gracias@example.com": {"password": "285", "role": "employee"},
    "labulu@example.com": {"password": "320", "role": "employee"},
    "kabamba@example.com": {"password": "588", "role": "employee"},
    "shimiah@example.com": {"password": "1234", "role": "employee"},
    "moula@example.com": {"password": "3232", "role": "employee"},
    "admin@example.com": {"password": "admin123", "role": "admin"}
}

# ---------- EMPLOYÉS ----------
employes = {
    "GRACIAS": "285",
    "LABULU": "320",
    "KABAMBA": "588",
    "SHIMIAH": "1234",
    "MOULA": "3232"
}

presences = {}

# ---------- TEMPLATE LOGIN ----------
login_template = """
<!DOCTYPE html>
<html lang='fr'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Connexion — GRACIAS PREP</title>
<style>
body { font-family: Arial; background:#e8f0fe; display:flex; justify-content:center; align-items:center; height:100vh; }
.container { background:white; padding:30px; border-radius:12px; width:320px; box-shadow:0 4px 15px rgba(0,0,0,0.1); }
h2 { text-align:center; margin-bottom:20px; }
input { width:100%; padding:10px; margin:10px 0; border:1px solid #ccc; border-radius:8px; }
button { width:100%; background:#4285f4; color:white; padding:10px; border:none; border-radius:8px; cursor:pointer; font-size:16px; }
button:hover { background:#3367d6; }
.error { color:#d93025; font-weight:bold; text-align:center; }
</style>
</head>
<body>
<div class='container'>
<h2>Connexion</h2>
<form method='post' action='/login'>
<input type='email' name='email' placeholder='Email' required>
<input type='password' name='password' placeholder='Code employé' required>
<button type='submit'>Se connecter</button>
</form>
{% if error %}<p class='error'>{{ error }}</p>{% endif %}
</div>
</body>
</html>
"""

# ---------- TEMPLATE DASHBOARD ----------
main_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GRACIAS PREP</title>
<style>
body { font-family: Arial; background:#e8f0fe; color:#333; margin:0; padding:0;}
header { background:#4285f4; color:white; padding:15px; text-align:center; font-size:24px; font-weight:bold; display:flex; justify-content:space-between; align-items:center; }
.logout { background:#d93025; padding:8px 14px; border-radius:8px; color:white; text-decoration:none; margin-right:20px; }
main { padding:20px; display:flex; flex-wrap:wrap; justify-content:center; gap:30px;}
.section { background:white; border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1); padding:20px; width:300px;}
input[type="text"] { width:80%; padding:8px; margin-bottom:10px; font-size:14px; }
button { background-color:#34a853; color:white; border:none; padding:8px 12px; border-radius:8px; cursor:pointer; font-size:14px; margin-top:5px; }
button:hover { background-color:#2c8c45; }
.present { color:#0b8043; font-weight:bold; }
.absent { color:#d93025; font-weight:bold; }
footer { text-align:center; padding:15px; background:#fbbc05; color:black; font-weight:bold;}
</style>
</head>
<body>
<header>
<div>GRACIAS PREP</div>
<a class="logout" href="/logout">Déconnexion</a>
</header>
<main>
  <div class="section">
    <h3>Marquer présence</h3>
    <form method="post" action="/marquer">
      <input type="text" name="code_emp" placeholder="Entrez votre code employé">
      <br><button type="submit">Marquer présence</button>
    </form>
  </div>
  <div class="section">
    <h3>Présents</h3>
    <ul>
      {% for emp, heure in presences.items() %}
      <li><span class="present">{{ emp }}</span> - {{ heure }}</li>
      {% endfor %}
    </ul>
  </div>
  <div class="section">
    <h3>Absents</h3>
    <ul>
      {% for emp in absents %}
      <li><span class="absent">{{ emp }}</span></li>
      {% endfor %}
    </ul>
  </div>
  <div class="section">
    <form method="post" action="/reset">
      <button type="submit" style="background:#fbbc05; color:black;">Nouvelle journée</button>
    </form>
  </div>
</main>
<footer>© 2025 GRACIAS PREP</footer>
</body>
</html>
"""

# ---------- ROUTES ----------
@app.route('/')
def home():
    if "user" not in session:
        return redirect(url_for('login_page'))
    return render_template_string(
        main_template,
        presences=presences,
        absents=[e for e in employes if e not in presences]
    )

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in users and users[email]["password"] == password:
            session["user"] = email
            return redirect(url_for('home'))
        return render_template_string(login_template, error="Identifiants incorrects")
    return render_template_string(login_template)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/marquer', methods=['POST'])
def marquer():
    if "user" not in session:
        return redirect(url_for('login_page'))
    code_emp = request.form.get('code_emp')
    nom = None
    for e, c in employes.items():
        if c == code_emp:
            nom = e
            break
    if nom and nom not in presences:
        presences[nom] = datetime.now().strftime("%H:%M:%S")
    return redirect(url_for('home'))

@app.route('/reset', methods=['POST'])
def reset():
    if "user" not in session:
        return redirect(url_for('login_page'))
    presences.clear()
    return redirect(url_for('home'))

# ---------- LANCEMENT ----------
if __name__ == "__main__":
    print("Ouvre ton navigateur et va sur : http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000)
