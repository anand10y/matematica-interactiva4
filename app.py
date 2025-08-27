import streamlit as st
from sympy import symbols, exp, integrate, pretty
import random
import math

x = symbols('x')

st.set_page_config(page_title="Integrale definite interactive", page_icon="📚", layout="centered")
st.title("📚 Lecție interactivă: Integrale definite")

# ----------------- Teorie -----------------
st.header("Formule uzuale pentru integrale definite")
st.subheader("1. Integrală putere")
st.latex(r"\int_a^b x^n \, dx = \frac{b^{n+1} - a^{n+1}}{n+1}, \quad n \neq -1")
st.subheader("2. Integrală inversă")
st.latex(r"\int_a^b \frac{1}{x} \, dx = \ln|b| - \ln|a| = \ln\left|\frac{b}{a}\right|")
st.subheader("3. Integrală exponențială")
st.latex(r"\int_a^b e^x \, dx = e^b - e^a")
st.write("Aceste formule pot fi combinate pentru a calcula integrale mai complexe.")

# ----------------- Setări exerciții -----------------
st.header("Setează numărul de exerciții")
num_ex = st.slider("Alege câte exerciții vrei să rezolvi:", min_value=1, max_value=10, value=3)

# ----------------- Funcție pentru generarea unui exercițiu -----------------
def generate_exercise():
    types = ["x^n", "1/x", "e^x"]
    t = random.choice(types)

    if t == "x^n":
        a = random.randint(0,3)
        b = random.randint(a+1,5)
        n = random.randint(1,4)
        expr = x**n
        correct = (b**(n+1) - a**(n+1))/(n+1)
        statement = f"∫_{a}^{b} x^{n} dx"
        options = [round(correct,3), round(correct*2,3), round(correct/2,3), round(correct+1,3)]
    elif t == "1/x":
        a = random.randint(1,3)
        b = random.randint(a+1,6)
        expr = 1/x
        correct = round(math.log(b) - math.log(a),3)
        statement = f"∫_{a}^{b} 1/x dx"
        options = [correct, round(correct+1,3), round(correct-0.5,3), round(correct*2,3)]
    else:  # e^x
        a = random.randint(0,2)
        b = random.randint(a+1,4)
        expr = exp(x)
        correct = round(float(exp(b)-exp(a)),3)
        statement = f"∫_{a}^{b} e^x dx"
        options = [correct, round(correct+1,3), round(correct-1,3), round(correct*2,3)]

    random.shuffle(options)
    return statement, correct, options, expr, a, b

# ----------------- Inițializare starea aplicației -----------------
if "exercises" not in st.session_state or st.button("Generează exerciții noi"):
    st.session_state.exercises = [generate_exercise() for _ in range(num_ex)]
    st.session_state.score = 0
    st.session_state.answered = [False]*num_ex

st.header("Exerciții practice (alegere multiplă)")

for i, (stmt, correct, opts, expr, a, b) in enumerate(st.session_state.exercises):
    st.subheader(f"{i+1}. {stmt}")
    choice = st.radio("Alege răspunsul corect:", opts, key=f"mc{i}")
    col1, col2 = st.columns([1,2])
    with col1:
        if st.button(f"Verifică răspuns {i+1}", key=f"btn{i}") and not st.session_state.answered[i]:
            if choice == correct:
                st.success("Corect!")
                st.session_state.score += 1
            else:
                st.error(f"Gresit. Răspuns corect: {correct}")
            st.session_state.answered[i] = True
    with col2:
        if st.button(f"Vezi toți pașii {i+1}", key=f"steps{i}"):
            st.write(f"**Rezolvare pas cu pas pentru:** {stmt}")
            integral = integrate(expr, (x, a, b))
            st.latex(f"\\int_{{{a}}}^{{{b}}} {str(expr)} \\, dx = {integral}")
            # afișăm și forma pas cu pas simplificată pentru putere
            if expr.func.__name__ == 'Pow':
                n = expr.args[1]
                st.latex(f"= \\frac{{{b}^{{{n}+1}} - {a}^{{{n}+1}}}}{{{n}+1}}")
            elif expr == 1/x:
                st.latex(f"= \\ln|{b}| - \\ln|{a}| = {round(math.log(b)-math.log(a),3)}")
            elif expr == exp(x):
                st.latex(f"= e^{b} - e^{a} = {round(float(exp(b)-exp(a)),3)}")

# ----------------- Afișare scor și progres -----------------
answered_count = sum(st.session_state.answered)
if answered_count > 0:
    st.info(f"Progres: {answered_count}/{num_ex} exerciții completate")
    st.info(f"Scor: {st.session_state.score}/{answered_count}")
