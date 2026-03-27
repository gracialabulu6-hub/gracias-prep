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
message = ""

# ---------- TEMPLATE HTML MODERNE ----------
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
    font-family: 'Poppins', sans-serif;
    background: #f1f5f9;
}

/* HEADER */
header {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    padding: 20px;
    text-align: center;
}

header img {
    width: 120px;
    height: auto;
}

/* GRID */
main {
    padding: 20px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}

/* CARD */
.section {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: 0.2s;
}

.section:hover {
    transform: translateY(-4px);
}

/* TITRE */
h3 {
    margin-bottom: 15px;
}

/* INPUT */
input {
    width: 100%;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #ddd;
}

/* BUTTON */
button {
    width: 100%;
    padding: 12px;
    margin-top: 10px;
    border-radius: 10px;
    border: none;
    background: #2563eb;
    color: white;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: #1d4ed8;
}

/* STATS */
.stats {
    display: flex;
    justify-content: space-between;
}

.stat {
    flex: 1;
    text-align: center;
}

/* COLORS */
.present { color: #16a34a; font-weight: bold; }
.absent { color: #dc2626; font-weight: bold; }

/* MESSAGE */
.message {
    text-align: center;
    padding: 10px;
    margin-bottom: 10px;
    font-weight: bold;
}

.success { color: green; }
.error { color: red; }

footer {
    text-align: center;
    padding: 15px;
    color: #555;
}

</style>
</head>

<body>

<header>
    <img src="https://i.imgur.com/u8yP1y6.png" alt="Logo GRACIAS">
    <h2>GRACIAS PREP - Système de Présence</h2>
    <p>{{ date }}</p>
</header>

<main>

    {% if message %}
    <div class="section message {{ 'success' if '✔' in message else 'error' }}">
        {{ message }}
    </div>
    {% endif %}

    <!-- ACTION -->
    <div class="section">
        <h3>Pointer un employé</h3>
        <form method="post" action="/marquer">
            <input type="text" name="code_emp" placeholder="Code employé" required>
            <button type="submit">Valider</button>
        </form>
    </div>

    <!-- STATS -->
    <div class="section">
        <h3>Statistiques</h3>
        <div class="stats">
            <div class="stat">
                <h2>{{ employes|length }}</h2>
                <p>Total</p>
            </div>
            <div class="stat">
                <h2 style="color:green;">{{ presences|length }}</h2>
                <p>Présents</p>
            </div>
            <div class="stat">
                <h2 style="color:red;">{{ absents|length }}</h2>
                <p>Absents</p>
            </div>
        </div>
    </div>

    <!-- PRESENTS -->
    <div class="section">
        <h3>Présents</h3>
        <ul>
        {% for emp, heure in presences.items() %}
            <li>
                <span class="present">{{ emp }}</span><br>
                🕒 {{ heure }}
            </li><br>
        {% endfor %}
        </ul>
    </div>

    <!-- ABSENTS -->
    <div class="section">
        <h3>Absents</h3>
        <ul>
        {% for emp in absents %}
            <li class="absent">{{ emp }}</li>
        {% endfor %}
        </ul>
    </div>

    <!-- RESET -->
    <div class="section">
        <form method="post" action="/reset">
            <button style="background:#f59e0b;">Nouvelle journée</button>
        </form>
    </div>

</main>

<footer>
    © 2026 GRACIAS PREP — Système de Présence
</footer>

</body>
</html>
"""

# ---------- ROUTES ----------
@app.route('/')
def accueil():
    return render_template_string(
        html_template,
        presences=presences,
        employes=employes,
        absents=[e for e in employes if e not in presences],
        date=datetime.now().strftime("%d/%m/%Y"),
        message=message
    )

@app.route('/marquer', methods=['POST'])
def marquer():
    global message

    code_emp = request.form.get('code_emp')
    nom = None

    for e, c in employes.items():
        if c == code_emp:
            nom = e
            break

    if nom:
        if nom not in presences:
            presences[nom] = datetime.now().strftime("%H:%M:%S")
            message = "✔ Présence enregistrée"
        else:
            message = "⚠ Déjà enregistré"
    else:
        message = "❌ Code incorrect"

    return redirect(url_for('accueil'))

@app.route('/reset', methods=['POST'])
def reset():
    global message
    presences.clear()
    message = "🔄 Nouvelle journée démarrée"
    return redirect(url_for('accueil'))

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
