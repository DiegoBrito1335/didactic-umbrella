from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html lang="pt">
<head>
  <meta charset="utf-8">
  <title>Calculadora de IMC com Cardápio</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style> body { font-family: sans-serif; padding: 20px; max-width: 600px; margin: auto; } </style>
</head>
<body>
  <h1>Calculadora de IMC</h1>
  <form method="post">
    <label>Peso (kg):</label><br>
    <input type="number" step="0.1" name="peso" required><br><br>
    <label>Altura (m):</label><br>
    <input type="number" step="0.01" name="altura" required><br><br>
    <button type="submit">Calcular IMC</button>
  </form>

  {% if resultado %}
    <hr>
    <h2>Resultado</h2>
    <pre>{{ resultado }}</pre>
  {% endif %}
</body>
</html>
"""


def gerar_cardapio(calorias):
    cafe = calorias * 0.20
    lanche = calorias * 0.10
    almoco = calorias * 0.35
    jantar = calorias * 0.25
    opcoes = gerar_opcoes()

    return f"""
Sugestão de divisão das {calorias:.0f} kcal:

🥣 Café da manhã (~{cafe:.0f} kcal): {random.choice(opcoes["cafe"])}
🍎 Lanche (~{lanche:.0f} kcal): {random.choice(opcoes["lanche"])}
🍽 Almoço (~{almoco:.0f} kcal): {random.choice(opcoes["almoco"])}
🍲 Jantar (~{jantar:.0f} kcal): {random.choice(opcoes["jantar"])}
"""


def gerar_opcoes():
    return {
        "cafe": [
            "Omelete + pão integral + café com leite",
            "2 ovos + tapioca + suco de laranja",
            "Mingau de aveia com banana", "Iogurte + granola + mamão",
            "Sanduíche de peito de peru", "Vitamina de morango + torradas",
            "Cuscuz com ovo + leite", "Pão integral + queijo + maçã",
            "Panqueca de banana + café", "Smoothie de frutas vermelhas"
        ],
        "lanche": [
            "Iogurte com mel", "Banana + pasta de amendoim", "Barrinha + chá",
            "Castanhas", "Tapioca com queijo", "Melancia + bolacha",
            "Vitamina de abacate", "Pão + patê de atum", "Maçã + queijo", "Smoothie"
        ],
        "almoco": [
            "Frango + arroz + feijão + salada", "Frango + purê + rúcula",
            "Tilápia + arroz + brócolis", "Patinho + arroz + abobrinha",
            "Omelete + arroz + salada", "Estrogonofe + arroz + alface",
            "Frango + macarrão integral", "Quibe + tabule + salada",
            "Tilápia + purê + salada", "Estrogonofe de carne + arroz + vagem"
        ],
        "jantar": [
            "Sopa + torradas", "Omelete + pão + salada", "Frango + purê + salada",
            "Tilápia + salada", "Wrap integral + salada", "Crepioca com queijo",
            "Salada de atum + legumes", "Quiche light + salada",
            "Hambúrguer de frango + arroz + salada", "Risoto + salada"
        ]
    }


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        peso = float(request.form["peso"])
        altura = float(request.form["altura"])
        imc = peso / (altura ** 2)
        resultado = f"Seu IMC é: {imc:.2f}\n"

        if imc < 18.5:
            resultado += "Classificação: Abaixo do peso"
        elif 18.5 <= imc < 25:
            resultado += "Classificação: Peso normal"
        else:
            calorias = (10*peso + 6.25*(altura*100) - 5*30 + 5) * 1.4 * 0.8
            resultado += f"\n\nPara emagrecer: {calorias:.0f} kcal/dia"
            resultado += "\n" + gerar_cardapio(calorias)

    return render_template_string(TEMPLATE, resultado=resultado)


if __name__ == "__main__":
    app.run(debug=True)
