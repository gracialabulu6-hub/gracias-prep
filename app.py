# ============================
# GRACIAS SHIMIAH - Système de Présence (Version Professionnelle)
# ============================

from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# ---------- EMPLOYÉS ----------
employes = {
    "GRACIAS": "285",
    "LABULU": "320",
    "KABAMBA": "588",
    "SHIMIAH": "1234",
    "MOULA": "3232"
}

presences = {}

# ---------- TEMPLATE HTML PRO ----------
html_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GRACIAS PREP - Présences</title>

<style>
    body {
        margin: 0;
        padding: 0;
        font-family: 'Arial', sans-serif;
        background: linear-gradient(135deg, #3c82f6, #7b2ff7);
        color: #222;
    }

    header {
        background: rgba(255,255,255,0.25);
        backdrop-filter: blur(10px);
        text-align: center;
        padding: 20px;
        border-bottom: 1px solid rgba(255,255,255,0.4);
    }

    header img {
        width: 140px;
        height: auto;
    }

    main {
        padding: 20px;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 25px;
    }

    .section {
        background: white;
        width: 320px;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
    }

    h3 {
        text-align: center;
        color: #3c82f6;
    }

    input[type="text"] {
        width: 100%;
        padding: 12px;
        margin-top: 10px;
        border-radius: 8px;
        border: 1px solid #ccc;
        font-size: 15px;
    }

    button {
        width: 100%;
        padding: 12px;
        margin-top: 15px;
        background: #3c82f6;
        color: white;
        border: none;
        font-size: 16px;
        border-radius: 8px;
        cursor: pointer;
    }

    button:hover {
        background: #2563eb;
    }

    .present { color: #059669; font-weight: bold; }
    .absent { color: #dc2626; font-weight: bold; }

    footer {
        text-align: center;
        padding: 15px;
        color: white;
        margin-top: 20px;
    }
</style>

</head>
<body>

<header>
    <!-- Ton logo -->
    <img src="{{ url_for:\Users\user\Desktop\mon projet\static',filename='logo.png') }}" alt="Logo GRACIAS">
    <h2 style="color:white; margin-top:10px;">Système de Présence</h2>
</header>

<main>

    <!-- Marquer Présence -->
    <div class="section">
        <h3>Marquer présence</h3>
        <form method="post" action="/marquer">
            <input type="text" name="code_emp" placeholder="Code employé" required>
            <button type="submit">Valider</button>
        </form>
    </div>

    <!-- Présents -->
    <div class="section">
        <h3>Présents</h3>
        <ul>
            {% for emp, heure in presences.items() %}
            <li>
                <span class="present">{{ emp }}</span><br>
                Email : {{ emp.lower() }}@presences.com<br>
                Arrivé à : {{ heure }}
            </li><br>
            {% endfor %}
        </ul>
    </div>

    <!-- Absents -->
    <div class="section">
        <h3>Absents</h3>
        <ul>
            {% for emp in absents %}
            <li><span class="absent">{{ emp }}</span></li>
            {% endfor %}
        </ul>
    </div>

    <!-- Nouvelle journée -->
    <div class="section">
        <form method="post" action="/reset">
            <button style="background:#fbbf24; color:black;">Nouvelle journée</button>
        </form>
    </div>

</main>

<footer>
    © 2025 GRACIAS PREP — Système de Présence
</footer>

</body>
</html>
"""

# ---------- ROUTES ----------
@app.route('/', methods=['GET'])
def accueil():
    return render_template_string(
        html_template,
        presences=presences,
        absents=[e for e in employes if e not in presences]
    )

@app.route('/marquer', methods=['POST'])
def marquer():
    code_emp = request.form.get('code_emp')
    nom = None

    # Vérifier le code employé
    for e, c in employes.items():
        if c == code_emp:
            nom = e
            break

    if nom and nom not in presences:
        presences[nom] = datetime.now().strftime("%H:%M:%S")

    return redirect(url_for('accueil'))

@app.route('/reset', methods=['POST'])
def reset():
    presences.clear()
    return redirect(url_for('accueil'))

# ---------- LANCEMENT ----------
if __name__ == "__main__":
    print("Ouvre ton navigateur ici → http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000)
