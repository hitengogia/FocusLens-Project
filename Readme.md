# 🧠 FocusLens AI 
## 📌 Overview

**FocusLens AI** is a real-time AI-powered attention monitoring system that analyzes user focus, engagement, and distraction using computer vision and behavioral analytics.

The system uses a webcam to detect facial expressions, gaze direction, and presence to compute an **engagement score** in real time. It also tracks session data and generates analytics reports.

---

## 🚀 Features

* 🎥 Real-time face detection using **face-api.js**
* 👁️ Gaze tracking (multi-zone detection)
* 😊 Expression-based engagement analysis
* 📊 Engagement score calculation (live)
* ⏱️ Session tracking with timer
* 🚨 Distraction & absence detection
* 📈 Focus timeline visualization
* 🧾 Exportable session reports (JSON)
* 🗄️ Backend storage with SQLite
* 📊 Session history & analytics

---

## 🧠 How It Works

### 1. Face Detection

Uses **TinyFaceDetector** from face-api.js to detect the user's face.

### 2. Gaze Tracking

Gaze direction is computed using:

* Nose position
* Eye alignment
* Facial landmarks

Mapped into zones like:

```
TL, TC, TR
ML, MC, MR
BL, BC, BR
```

### 3. Engagement Score

Score is calculated using weighted factors:

* Expression → 50%
* Gaze → 30%
* Presence → 20%

Final score:

```
Score = Expression + Gaze + Presence
```

---

## 🏗️ Tech Stack

### Frontend

* HTML, CSS, JavaScript
* face-api.js (ML in browser)

### Backend

* Python (Flask)
* SQLite database

---

## 📁 Project Structure

```
focuslens-project/
│
├── backend/
│   ├── app.py
│   └── focuslens.db
│
├── frontend/
│   ├── index.html
│   └── models/
│       ├── tiny_face_detector_model
│       ├── face_landmark_68_model
│       └── face_expression_model
```

---

## ⚙️ Setup Instructions

### 1. Clone / Download Project

### 2. Install Backend Dependencies

```bash
pip install flask flask-cors
```

---

### 3. Run Backend

```bash
cd backend
python app.py
```

Runs at:

```
http://localhost:5000
```

---

### 4. Run Frontend

```bash
cd frontend
python -m http.server 8000
```

Open:

```
http://localhost:8000
```

---

## 🔑 Important Notes

* Allow **camera permissions** in browser
* Ensure `models/` folder exists with required files
* Do NOT open HTML using `file://` — use localhost

---

## 📊 Output

The system provides:

* Real-time engagement score
* Focus percentage
* Distraction count
* Alerts (look-away events)
* Session reports (JSON export)

---

## 🎯 Applications

* Online learning platforms
* Remote work productivity tracking
* Behavioral analytics systems
* Attention monitoring tools

---

## 🔮 Future Improvements

* 📱 Phone detection
* 🔔 Real-time alerts (sound/visual)
* 🧠 AI-based focus insights
* 📊 Advanced analytics dashboard
* ☁️ Cloud integration

---

## 👨‍💻 Author

**Hiten Gogia**

---

This project is for educational and research purposes.
