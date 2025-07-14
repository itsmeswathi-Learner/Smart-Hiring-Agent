🧠 Smart Hiring Agent

A smart hiring agent platform with resume upload, Interview round, MCQ test (Aptitude + Verbal + Logical Reasoning), coding round with proctoring features. 

This project helps automate the hiring process by evaluating candidates through multiple stages: 

     -->resume scoring
     -->Interview round
     -->Aptitude+verbal reasoning+logical reasoning(MCQ Test)
     -->Coding round

🚀 Features

📄 Resume Upload & ATS Scoring

     Analyze resumes for keywords, formatting, readability
🤖 Interview

      Chatbot-based interview simulation
🧮 MCQ Test

    30 questions: 10 Aptitude, 10 Verbal, 10 Logical Reasoning
    ⏱️ 1-Minute Timer
     Auto-next after time ends
🧑‍💻 Coding Round

     Submit code for backend analysis
📥 MySQL

     Stores user data, answers, and results     
📊 Final Dashboard

     View scores from all rounds
🛡️ Proctoring

     Prevents copy/paste, tab switch, window resizing


🧰 Technologies Used

Frontend          

            -HTML5, CSS3, Vanilla JavaScript

Backend    

              -Flask (Python)
Database           

              -MySQL
AI Features       

              -chatbot simulation
Proctoring        

              -JavaScript event listeners
Deployment        

              -Local Flask server


📦 Requirements

🔧 Python Packages

Install these before running:

      pip install flask mysql-connector-python werkzeug textstat language_tool_python
🖥️ MySQL

Ensure you have a working MySQL setup. Import the schema using:

     mysql -u root -p < database.sql

🧪 How to Run Locally

1.Clone the repo

     git clone https://github.com/your-username/smart-hiring-agent.git 
     cd smart-hiring-agent
2.Install dependencies

     pip install -r requirements.txt
3.Start the Flask app

    python app.py
4.Open in browser

    http://127.0.0.1:5000

🧪 How to Use

1. Resume Upload
   
       Go to /upload_resume
       Upload .pdf or .docx resume
       Enter job description
       View ATS score and matched keywords
2. Interview Simulation
   
       Go to /interview
       Get score based on answer type and grammar  
3. MCQ Test
 
       Go to /mcq
       Complete 30 questions (10 per section)
       Timer per question (60 seconds)
       Proctoring prevents cheating
4. Coding Round
   
       Go to /coding
       Write code in editor
       Submit for backend analysis
**Chatbot
      Jotform assistent

📊 Database Tables

users                   - Stores user login details
resume_scores           - Stores resume ATS scores
mcqanswers              - Stores each MCQ answer             
mcqresults              - Stores final MCQ score and AI evaluation
codingresults           - Stores coding submissions
interviewresults        - Stores interview questions and user answers


🧪 Proctoring Features

❌ Blocks keyboard shortcuts (Ctrl+C, Ctrl+V, etc.)

❌ Blocks right-click

❌ Detects tab/window switch

❌ Prevents window resizing/minimizing

⚠️ Shows alert on violation

🚫 Closes test if repeated violations



🧠 AI Scoring Logic
✅ MCQ: +1 for correct, -0.1 for incorrect

✅ Resume: Keyword match, section presence, formatting

✅ Interview: Practical vs theoretical answers, grammar, confidence



🧾 Contributing
If you want to contribute:

Fork the repo
Create a new branch:
git checkout -b feature/new-interview-round
Commit changes:
git commit -m 'Add new feature'
Push to your branch:
git push origin feature/new-interview-round
Open a Pull Request

📬 Contact

swathilakshmigurram17@gmail.com
Project Link:
👉 https://github.com/itsmeswathi-Learner/smart-hiring-agent



🤝 Suggestions & Feedback
I'm actively looking for ways to improve this Smart Hiring Agent platform. If you have any suggestions , feedback , or want to contribute , please do share!

You can help by suggesting:

Better MCQ questions (topic-wise)
Improved ATS resume scoring logic
AI-based interview evaluation
Webcam or face detection proctoring
PDF report generation
Admin panel for recruiters
Deployment guides for Render, PythonAnywhere, Heroku
Dockerfile and containerization
Real-time dashboard or analytics
If you're using this in production or testing it, I'd love to hear from you!

📬 How to Share Feedback
📨 Email:
swathilakshmigurram17@gmail.com
