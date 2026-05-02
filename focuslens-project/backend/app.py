from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB = "focuslens.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        started_at TEXT,
        duration_s INTEGER,
        focus_pct INTEGER,
        avg_score INTEGER,
        distraction_count INTEGER,
        alert_count INTEGER,
        total_frames INTEGER,
        focused_frames INTEGER
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS frames (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        score INTEGER,
        gaze_zone TEXT,
        expression TEXT,
        face_present INTEGER,
        ts TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        event_type TEXT,
        message TEXT,
        ts TEXT
    )''')

    conn.commit()
    conn.close()

init_db()

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/api/sessions', methods=['POST'])
def create_session():
    data = request.json
    sid = str(uuid.uuid4())

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute('''
        INSERT INTO sessions (id, user_id, started_at)
        VALUES (?, ?, ?)
    ''', (sid, data.get("user_id"), datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()

    return jsonify({"session_id": sid})

@app.route('/api/sessions/<sid>/frames', methods=['POST'])
def add_frames(sid):
    data = request.json
    frames = data.get("frames", [])

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    for f in frames:
        c.execute('''
            INSERT INTO frames (session_id, score, gaze_zone, expression, face_present, ts)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            sid,
            f.get("score"),
            f.get("gaze_zone"),
            f.get("expression"),
            f.get("face_present"),
            f.get("ts")
        ))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

@app.route('/api/sessions/<sid>/events', methods=['POST'])
def add_event(sid):
    data = request.json

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute('''
        INSERT INTO events (session_id, event_type, message, ts)
        VALUES (?, ?, ?, ?)
    ''', (
        sid,
        data.get("event_type"),
        data.get("message"),
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

@app.route('/api/sessions/<sid>/end', methods=['POST'])
def end_session(sid):
    data = request.json

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute('''
        UPDATE sessions SET
        duration_s=?,
        focus_pct=?,
        avg_score=?,
        distraction_count=?,
        alert_count=?,
        total_frames=?,
        focused_frames=?
        WHERE id=?
    ''', (
        data.get("duration_s"),
        data.get("focus_pct"),
        data.get("avg_score"),
        data.get("distraction_count"),
        data.get("alert_count"),
        data.get("total_frames"),
        data.get("focused_frames"),
        sid
    ))

    conn.commit()
    conn.close()

    return jsonify({"status": "saved"})

@app.route('/api/sessions')
def get_sessions():
    user_id = request.args.get("user_id")
    limit = int(request.args.get("limit", 5))

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute('''
        SELECT * FROM sessions
        WHERE user_id=?
        ORDER BY started_at DESC
        LIMIT ?
    ''', (user_id, limit))

    rows = c.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "started_at": r[2],
            "duration_s": r[3],
            "focus_pct": r[4],
            "avg_score": r[5],
            "distraction_count": r[6]
        })

    return jsonify(result)

@app.route('/api/analytics/summary')
def summary():
    user_id = request.args.get("user_id")

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute('''
        SELECT AVG(focus_pct), AVG(avg_score),
               COUNT(*), SUM(distraction_count)
        FROM sessions WHERE user_id=?
    ''', (user_id,))

    row = c.fetchone()
    conn.close()

    return jsonify({
        "avg_focus_pct": int(row[0]) if row[0] else None,
        "avg_score": int(row[1]) if row[1] else None,
        "total_sessions": row[2],
        "total_distractions": row[3] or 0
    })

if __name__ == "__main__":
    app.run(debug=True)