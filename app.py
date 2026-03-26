from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'financas_secret_key_2024'

DB_PATH = os.path.join(os.path.dirname(__file__), 'financas.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.executescript(open(os.path.join(os.path.dirname(__file__), 'schema.sql')).read())
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('lancamentos'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_val = request.form['login']
        senha = request.form['senha']
        conn = get_db()
        user = conn.execute(
            'SELECT * FROM usuario WHERE login = ? AND situacao = "A"', (login_val,)
        ).fetchone()
        conn.close()
        if user and check_password_hash(user['senha'], senha):
            session['user_id'] = user['id']
            session['user_name'] = user['nome']
            return redirect(url_for('lancamentos'))
        flash('Login ou senha inválidos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/lancamentos')
def lancamentos():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    tipo = request.args.get('tipo', '')
    situacao = request.args.get('situacao', '')
    query = 'SELECT * FROM lancamento WHERE 1=1'
    params = []
    if tipo:
        query += ' AND tipo_lancamento = ?'
        params.append(tipo)
    if situacao:
        query += ' AND situacao = ?'
        params.append(situacao)
    query += ' ORDER BY data_lancamento DESC'
    rows = conn.execute(query, params).fetchall()

    total_receita = sum(r['valor'] for r in rows if r['tipo_lancamento'] == 'R')
    total_despesa = sum(r['valor'] for r in rows if r['tipo_lancamento'] == 'D')
    saldo = total_receita - total_despesa
    conn.close()
    return render_template('lancamentos.html', lancamentos=rows,
                           total_receita=total_receita,
                           total_despesa=total_despesa,
                           saldo=saldo,
                           filtro_tipo=tipo,
                           filtro_situacao=situacao)

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
