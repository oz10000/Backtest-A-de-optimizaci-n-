import sqlite3
from datetime import datetime

DB_PATH = 'sq3lite_trader.db'  # SQ3 Lite

def init_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Tabla de resultados de optimización
    c.execute('''
    CREATE TABLE IF NOT EXISTS optimization_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        tf_entrada TEXT,
        tf_tendencia TEXT,
        adx_th INTEGER,
        rsi_low INTEGER,
        rsi_high INTEGER,
        mult_stop REAL,
        mult_tp REAL,
        use_slope BOOLEAN,
        profit REAL,
        trades INTEGER,
        win_rate REAL,
        max_dd REAL
    )
    ''')

    # Tabla de trades individuales
    c.execute('''
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        combo_id INTEGER,
        entry_time DATETIME,
        exit_time DATETIME,
        tipo TEXT,
        entry_price REAL,
        exit_price REAL,
        retorno REAL,
        razon TEXT,
        win BOOLEAN,
        leverage_used REAL,
        capital_used REAL
    )
    ''')

    conn.commit()
    conn.close()

def save_optimization_result(tf_entrada, tf_tendencia, params, metrics):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO optimization_results (tf_entrada, tf_tendencia, adx_th, rsi_low, rsi_high, mult_stop, mult_tp, use_slope, profit, trades, win_rate, max_dd)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        tf_entrada,
        tf_tendencia,
        params['adx_th'],
        params['rsi_low'],
        params['rsi_high'],
        params['mult_stop'],
        params['mult_tp'],
        int(params['use_slope']),
        metrics['profit'],
        metrics['trades'],
        metrics['win_rate'],
        metrics['max_dd']
    ))
    conn.commit()
    conn.close()
