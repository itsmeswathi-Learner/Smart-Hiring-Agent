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



<img width="1887" height="928" alt="image" src="https://github.com/user-attachments/assets/28301494-f87a-4e00-b9ba-864595b54b53" />
<img width="520" height="666" alt="image" src="https://github.com/user-attachments/assets/767831c9-742c-4391-b728-30db9f803591" />
<img width="1840" height="829" alt="image" src="https://github.com/user-attachments/assets/791eee2c-f145-4271-8131-7a8103bdb970" />
<img width="1721" height="826" alt="image" src="https://github.com/user-attachments/assets/20abc9e3-876d-4f0e-a804-f5c237eeb553" />
<img width="1890" height="275" alt="image" src="https://github.com/user-attachments/assets/065427ac-0469-4a32-a508-2d1df3d314fe" />
<img width="825" height="709" alt="image" src="https://github.com/user-attachments/assets/41cefb0b-2aeb-4b59-8dae-d4780f2420ee" />
<img width="639" height="482" alt="image" src="https://github.com/user-attachments/assets/41304502-6a3e-4bc5-bc91-2d6466b0998b" />
<img width="723" height="834" alt="image" src="https://github.com/user-attachments/assets/5d3ee3ea-b93c-4734-bac2-35d9d28ee976" />
<img width="1805" height="622" alt="image" src="https://github.com/user-attachments/assets/44807943-2cf3-476a-beab-268f588e4a1a" />
<img width="1180" height="828" alt="image" src="https://github.com/user-attachments/assets/19fe2fdc-baf8-45e6-8dd9-41557f30f3c7" />
<img width="1554" height="835" alt="image" src="https://github.com/user-attachments/assets/8ccb2df1-c623-4ad5-bcf4-12679a5d0cc2" />
<img width="1205" height="459" alt="image" src="https://github.com/user-attachments/assets/d680adaa-263f-4d13-863c-769e39f7f912" />


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

If you're using or testing this project, I’d love your feedback!
