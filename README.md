# 🧠 Smart Hiring Agent

An intelligent hiring platform that automates candidate evaluation through multiple stages:

* 📄 Resume Scoring (ATS)
* 🧠 Interview Round with Speech-to-Text
* 🧮 MCQ Test (Aptitude + Verbal + Logical Reasoning)
* 👨‍💻 Coding Round with Proctoring and Video Monitoring

Helps recruiters streamline hiring and empowers students to experience realistic assessments.



## 🚀 Features

### 📄 Resume Upload & ATS Scoring

* Upload resumes in `.pdf` or `.docx` format
* Analyze for:

  * Keyword match against job description
  * Formatting quality
  * Section presence & readability

### 🤖 Interview Simulation

* Chatbot conducts structured interview questions
* Includes **speech-to-text input** using browser microphone
* Evaluates based on:

  * Answer quality (theory vs practical)
  * Grammar & structure
  * Confidence simulation

### 🧮 MCQ Test (Aptitude, Verbal, Logical)

* Total 30 Questions: 10 Aptitude, 10 Verbal, 10 Logical Reasoning
* Features:

  * 60-second timer per question
  * Auto-next after time ends
  * Cheating prevention

### 👨‍💻 Coding Round

* Online code editor with syntax highlighting
* Secure code execution using Judge0 API
* Real-time **video recording** for proctoring
* Submit code for backend logic testing
* Evaluated on correctness, efficiency, and edge cases
* Timer-based enforcement and auto-submit upon timeout

### 📥 MySQL Database Integration

* Stores:

  * User credentials
  * Resume scores
  * Interview results
  * MCQ answers & scores
  * Coding submissions & outcomes

### 🛡️ Proctoring Features

* Prevents cheating via:

  * Disabling Ctrl+C, Ctrl+V, right-click
  * Tab/window switch detection
  * Window resizing or minimize detection
  * Shows warning on violation
  * Auto-disqualify after repeated alerts
  * **Video recording of candidate during the coding round using JavaScript MediaRecorder API**
  * **Speech-to-text for interview via Web Speech API**

---

## 🧰 Tech Stack

**Frontend**: HTML5, CSS3, Vanilla JavaScript
**Backend**: Flask (Python)
**Database**: MySQL
**AI Logic**: Interview evaluator (rule based AI) , Resume keyword matcher.
**Proctoring**: JS event listeners, camera and microphone stream APIs

**APIs & Libraries**:

* 🧪 **Judge0 RapidAPI**: Used for secure and efficient online code execution during the coding round
* 📚 **Textstat, language\_tool\_python**: Used for grammar and readability analysis in interview evaluation
* 🎥 **MediaRecorder API**: Records video during coding round for submission
* 🎤 **getUserMedia() API**: Captures microphone input for real-time monitoring
* 🗣️ **Web Speech API**: Converts spoken answers to text in the interview round
* 🔐 **Other Flask-compatible libraries**: For session handling, file processing, and input sanitation

---

## 📦 Requirements

### 🔧 Python Packages

Install these before running:

```bash
pip install flask mysql-connector-python werkzeug textstat language_tool_python
```

### 🖥️ MySQL Setup

Ensure your MySQL server is running.
Import schema:

```bash
mysql -u root -p < database.sql
```

---

## 🧪 How to Run Locally

1. **Clone the repo**

```bash
git clone https://github.com/itsmeswathi-Learner/Smart-Hiring-Agent.git
cd Smart-Hiring-Agent
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Start Flask App**

```bash
python app.py
```

4. **Visit in Browser**

```
http://127.0.0.1:5000
```

---

## 🧪 User Guide

### 1. Resume Scoring

* Route: `/upload_resume`
* Upload resume
* Enter job description
* View ATS score

### 2. Interview Round

* Route: `/interview`
* Shows questions
* Speech input via microphone
* Scores grammar + relevance + confidence+ answer type

### 3. MCQ Test

* Route: `/mcq`
* 30 timed questions
* Sections: Aptitude, Verbal, Logical

### 4. Coding Round

* Route: `/coding`
* Code in-browser with test cases
* Timer starts with video recording enabled
* Auto-submit after timeout or tab switch violations
* Code submitted to backend for Judge0 evaluation
* Results are stored in dashboard

---

## 🗃️ Database Schema Overview

| Table Name         | Purpose                                           |
| ------------------ | ------------------------------------------------- |
| `users`            | Stores login credentials                          |
| `resume_scores`    | ATS resume evaluations                            |
| `interviewresults` | Chatbot-based interview logs                      |
| `mcqanswers`       | All submitted MCQ answers                         |
| `mcqresults`       | Final MCQ scores                                  |
| `codingresults`    | Stores coding submissions                         |
| `webcams`        | Stores  path of recorded webcam sessions |

---

## 🔐 Proctoring (Cheating Prevention)

* ❌ Blocks Ctrl+C, Ctrl+V, right-click
* 🛑 Detects tab/window change
* 📏 Prevents resizing/minimizing
* ⚠️ Shows warning alert
* 🚫 Auto-terminate after repeated violations
* 🎥 **Live video recording** using browser camera(JavaScript MediaRecorder API)
* 🗣️ **Speech-to-text input** using Web Speech API
* ⏲️ **Timer lock** with forced auto-submit

---

## 🧠 AI Scoring Logic

* **MCQ**: +1 for correct, -0.1 for incorrect
* **Resume**: Section match + keyword presence + format score
* **Interview**: Evaluates grammar + answer style + simulated confidence
* **Coding**: Test case success, complexity score, code quality

---

## 🤝 Contributing

1. **Fork this repo**
2. Create a feature branch:

```bash
git checkout -b feature/my-feature
```

3. Commit your changes:

```bash
git commit -m "Add XYZ feature"
```

4. Push to GitHub:

```bash
git push origin feature/my-feature
```

5. Open a Pull Request 🚀

---

## 📬 Feedback & Suggestions

💌 Email: [swathilakshmigurram17@gmail.com](mailto:swathilakshmigurram17@gmail.com)
📌 Project Repo: [Smart Hiring Agent](https://github.com/itsmeswathi-Learner/Smart-Hiring-Agent)

### Ideas for Improvement:

* Better MCQ questions
* AI-enhanced Interview (Rule based)
* Webcam detection proctoring
* Admin dashboard
* Dockerfile for containerization
* Cloud deployment guide (Render, PythonAnywhere, Heroku)

If you're using or testing this project, I’d love your feedback!
