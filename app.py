
from flask import Flask, request, render_template_string
import csv
import os
from datetime import datetime

app = Flask(__name__)

plans = [
    {"name": "New Endowment Plan", "number": "714",
     "category": "Endowment Plan",
     "url": "https://licindia.in/web/guest/endowment-plans"},
    {"name": "New Jeevan Anand", "number": "715",
     "category": "Endowment Plan",
     "url": "https://licindia.in/web/guest/endowment-plans"},
    {"name": "Digi Term", "number": "876",
     "category": "Term Assurance",
     "url": "https://web.licindia.in/en/web/guest/term-assurance-plans"},
    {"name": "Bima Kavach", "number": "887",
     "category": "Term Assurance",
     "url": "https://web.licindia.in/en/web/guest/term-assurance-plans"}
]

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Life Insurance Advisor</title>
<style>
body { margin:0; font-family:Arial,sans-serif;
       background:#f4f7fb; color:#243044; }
header, footer { background:#073b70; color:white; padding:20px 7%; }
header { display:flex; justify-content:space-between; flex-wrap:wrap; }
nav a { color:white; margin-left:12px; text-decoration:none; }
.hero { text-align:center; padding:45px 15px;
        background:#e2efff; }
section { padding:30px 7%; }
.cards { display:grid; grid-template-columns:
         repeat(auto-fit,minmax(220px,1fr)); gap:18px; }
.card, form { background:white; padding:22px; border-radius:12px;
              box-shadow:0 3px 12px #dce3ec; }
.card h3 { color:#073b70; }
.btn { display:inline-block; background:#087c66; color:white;
       padding:12px 17px; border:0; border-radius:7px;
       text-decoration:none; cursor:pointer; }
input, select { width:100%; padding:12px; margin:8px 0 16px;
                box-sizing:border-box; border:1px solid #ccd4df;
                border-radius:6px; }
.notice { font-size:13px; color:#58677a; }
.success { background:#e1f3ed; padding:15px; border-radius:8px; }
</style>
</head>
<body>
<header>
<h2>Life Insurance Advisor</h2>
<nav><a href="#plans">Plans</a><a href="#callback">Request Call Back</a></nav>
</header>

<div class="hero">
<h1>Plan for a Secure Tomorrow</h1>
<p>Explore insurance options and request a call from your advisor.</p>
<a class="btn" href="#callback">Request a Call Back</a>
</div>

<section id="plans">
<h2>Insurance Plan Information</h2>
<div class="cards">
{% for plan in plans %}
<div class="card">
<h3>{{ plan.name }}</h3>
<p>Plan number: {{ plan.number }}</p>
<p>{{ plan.category }}</p>
<a class="btn" href="{{ plan.url }}" target="_blank"
   rel="noopener noreferrer">Official LIC Information</a>
</div>
{% endfor %}
</div>
<p class="notice">Check official LIC documents for current terms and
benefits. This is an independent demonstration website.</p>
</section>

<section id="callback">
<h2>Request a Call Back</h2>
<p>Enter your details. The advisor can use the submitted number
to contact you about your enquiry.</p>

{% if message %}
<div class="success"><strong>{{ message }}</strong></div>
{% endif %}

<form action="/callback" method="POST">
<label for="name">Your name</label>
<input id="name" name="name" maxlength="80" required
       placeholder="Enter your name">

<label for="phone">Phone number to call back</label>
<input id="phone" name="phone" type="tel" maxlength="20"
       required placeholder="Enter your phone number">

<label for="plan">What are you interested in?</label>
<select id="plan" name="plan" required>
<option value="">Select a plan or enquiry</option>
{% for plan in plans %}
<option value="{{ plan.name }}">{{ plan.name }}</option>
{% endfor %}
<option value="General enquiry">General enquiry</option>
</select>

<button class="btn" type="submit">Request Call Back</button>
</form>
<p class="notice">By submitting, you ask the advisor to contact you
about this enquiry. Use customer information only with appropriate
consent and protect it from unauthorized access.</p>
</section>

<footer>
<p>Life Insurance Advisor</p>
<p>Independent demo website — not an official LIC website.</p>
</footer>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML, plans=plans, message="")


@app.route("/callback", methods=["POST"])
def callback():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    selected_plan = request.form.get("plan", "").strip()

    allowed_plans = [p["name"] for p in plans]
    allowed_plans.append("General enquiry")

    if (not name or len(name) > 80 or not phone or len(phone) > 20
            or selected_plan not in allowed_plans):
        return render_template_string(
            HTML, plans=plans,
            message="Please check your name, phone number and selection."
        ), 400

    filename = "enquiries.csv"
    new_file = not os.path.exists(filename)

    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow([
                "Date", "Name", "Phone", "Interested Plan", "Status"
            ])
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            name, phone, selected_plan, "Callback requested"
        ])

    return render_template_string(
        HTML, plans=plans,
        message=(
            "Thank you, " + name + "! Your call-back request has been "
            "recorded for " + selected_plan +
            ". The advisor can call you at the number you provided."
        )
    )


if __name__ == "__main__":
    app.run(debug=False, port=5000)
    if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
    