from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from db_config import get_connection, fetch_all, execute_query
import os
import re
from collections import Counter
from textstat import flesch_reading_ease, flesch_kincaid_grade
import language_tool_python
import random
import requests
import time
import librosa
import numpy as np
import tempfile
from docx import Document
import PyPDF2

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx'}

# Allowed file extensions check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Extract keywords for ATS
def extract_keywords(text, top_n=20):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.lower().split()
    stopwords = set([
        'and', 'or', 'in', 'on', 'with', 'to', 'for', 'of', 'at', 'a', 'an', 'the',
        'is', 'are', 'by', 'as', 'be', 'this', 'that', 'it'
    ])
    words = [word for word in words if word not in stopwords and len(word) > 2]
    common = Counter(words).most_common(top_n)
    return [word for word, _ in common]


# ATS scoring function
def calculate_ats_score(resume_text, job_desc_text):
    score = 0
    total = 0
    resume_text = resume_text.strip()
    resume_lower = resume_text.lower()

    # Sections check
    sections = ['summary', 'education', 'experience', 'skills', 'projects', 'certifications', 'internships','extra-curicullar']
    for section in sections:
        total += 5
        if section in resume_lower:
            score += 5

    # Bullet points
    bullets = len(re.findall(r'[\*\-\u2022]', resume_text))
    total += 5
    score += 5 if bullets >= 5 else 2

    # Contact info
    total += 5
    if re.search(r'\b\d{10}\b', resume_text) and re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}\b', resume_text):
        score += 5
    elif re.search(r'\b\d{10}\b', resume_text) or re.search(r'@', resume_text):
        score += 3

    # Punctuation
    punctuations = len(re.findall(r'[.!?]', resume_text))
    total += 5
    score += 5 if punctuations > 10 else 2

    # Keyword diversity
    words = resume_text.split()
    unique_words = set(words)
    density = len(unique_words) / len(words) if words else 0
    total += 5
    score += 5 if density > 0.5 else 2

    # Readability
    try:
        readability_score = flesch_reading_ease(resume_text)
        grade_level = flesch_kincaid_grade(resume_text)
        total += 10
        if readability_score > 60 and grade_level < 12:
            score += 10
        elif readability_score > 40:
            score += 5
    except:
        total += 10
        score += 5

    # Job description keyword match
    jd_keywords = extract_keywords(job_desc_text, top_n=20)
    matched_keywords = [kw for kw in jd_keywords if kw in resume_lower]
    missing_keywords = list(set(jd_keywords) - set(matched_keywords))
    total += 50
    match_ratio = len(matched_keywords) / len(jd_keywords) if jd_keywords else 0
    if match_ratio >= 0.8:
        score += 50
    elif match_ratio >= 0.5:
        score += 35
    elif match_ratio >= 0.3:
        score += 20
    else:
        score += 10

    final_score = round((score / total) * 100, 2)
    return final_score, matched_keywords, missing_keywords


# Grammar Score
def get_grammar_score(text):
    if not text or not text.strip():
        return 0
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    num_errors = len(matches)
    num_words = len(text.split())
    if num_words == 0:
        return 0
    errors_per_100 = (num_errors / num_words) * 100
    if errors_per_100 == 0:
        score = 93
    elif errors_per_100 < 2:
        score = 90
    elif errors_per_100 < 5:
        score = 80
    elif errors_per_100 < 10:
        score = 65
    elif errors_per_100 < 20:
        score = 50
    elif errors_per_100 < 40:
        score = 30
    else:
        score = 10
    return round(score, 2)


# Voice Tone Score
def get_voice_tone_score(text):
    if not text or not text.strip():
        return 0
    positive_words = ['enthusiastic', 'confident', 'excited', 'motivated', 'passionate', 'eager', 'committed', 'positive', 'energetic', 'driven']
    negative_words = ['nervous', 'unsure', 'afraid', 'doubt', 'uncertain', 'hesitant', 'negative', 'worried', 'anxious', 'uncomfortable']
    text_lower = text.lower()
    pos_count = sum(text_lower.count(word) for word in positive_words)
    neg_count = sum(text_lower.count(word) for word in negative_words)
    score = 5 + (pos_count * 2) - (neg_count * 2)
    score = max(1, min(10, score))
    return score


# Communication Score
def get_communication_score(text):
    if not text or not text.strip():
        return 0
    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    num_sentences = len(sentences)
    words = text.split()
    num_words = len(words)
    avg_sentence_length = num_words / num_sentences if num_sentences else 0
    if avg_sentence_length < 8:
        length_score = 60
    elif avg_sentence_length > 25:
        length_score = 70
    else:
        length_score = 90
    filler_words = ['um', 'uh', 'like', 'you know', 'actually', 'basically', 'so', 'well']
    filler_count = sum(text.lower().count(fw) for fw in filler_words)
    filler_penalty = min(filler_count * 3, 30)
    connectors = ['and', 'but', 'because', 'however', 'therefore', 'moreover', 'thus', 'so']
    connector_count = sum(text.lower().count(c) for c in connectors)
    structure_score = 10 + min(connector_count * 5, 20)
    short_sentences = sum(1 for s in sentences if len(s.split()) < 5)
    long_sentences = sum(1 for s in sentences if len(s.split()) > 30)
    clarity_penalty = (short_sentences + long_sentences) * 2
    score = length_score + structure_score - filler_penalty - clarity_penalty
    return round(max(0, min(100, score)), 2)


# Confidence Score
def get_confidence_score(text):
    confident_phrases = ["I am confident", "I believe", "I am sure", "certainly", "definitely", "without a doubt",
                         "I can", "I will", "I have", "I know", "I managed", "I achieved", "I succeeded"]
    hedging_phrases = ["I think", "maybe", "perhaps", "possibly", "I guess", "I suppose", "I hope", "I feel", "I wish"]
    text_lower = text.lower()
    confident_count = sum(text_lower.count(phrase.lower()) for phrase in confident_phrases)
    hedge_count = sum(text_lower.count(phrase.lower()) for phrase in hedging_phrases)
    score = 60 + (confident_count * 8) - (hedge_count * 10)
    return round(max(0, min(100, score)), 2)


# Detect answer type
def detect_answer_type(text):
    keywords = ['experience', 'project', 'worked', 'developed', 'implemented']
    return "Practical" if any(word in text.lower() for word in keywords) else "Theoretical"


# Routes
@app.route('/')
def home():
    return render_template('landpage.html')


@app.route('/landing')
def landing():
    print("Landing page accessed")
    return render_template('landpage.html')


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    data = cursor.fetchone()
    conn.close()
    if data and check_password_hash(data[0], password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        flash("Invalid credentials")
        return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, password))
            conn.commit()
            flash("Signup successful! Please login.")
            return redirect(url_for('home'))
        except:
            flash("Username already exists.")
            return redirect(url_for('signup'))
        finally:
            conn.close()
    return render_template('signup.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        flash("Please log in first.")
        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('ats_score', None)
    flash("You have been logged out.")
    return redirect(url_for('home'))


@app.route('/upload_resume', methods=['GET', 'POST'])
def upload_resume():
    if 'username' not in session:
        flash("Please log in first.")
        return redirect(url_for('home'))
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['resume']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Extract text from the file
            text = ''
            if filename.endswith('.pdf'):
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ''.join([page.extract_text() for page in reader.pages])
            elif filename.endswith('.docx'):
                doc = Document(file_path)
                text = ''.join([para.text for para in doc.paragraphs])
            else:
                flash("Unsupported file format")
                return redirect(request.url)

            job_desc_text = request.form.get('job_description', '')
            if not job_desc_text:
                flash("Please provide a job description.")
                return redirect(request.url)

            ats_score, matched_keywords, missing_keywords = calculate_ats_score(text, job_desc_text)
            session['ats_score'] = ats_score

            # Save score in DB
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO resume_scores (username, filename, score) VALUES (%s, %s, %s)",
                (session['username'], filename, ats_score)
            )
            conn.commit()
            conn.close()

            return render_template('upload_resume.html', ats_score=ats_score, filename=filename,
                                   matched_keywords=matched_keywords, missing_keywords=missing_keywords)
    return render_template('upload_resume.html')


@app.route('/interview')
def interview():
    if 'username' not in session:
        flash("Please log in first.")
        return redirect(url_for('home'))
    if 'ats_score' not in session or session['ats_score'] < 40:
        flash("ATS score below 40%. Please improve your resume.")
        session.pop('username', None)
        session.pop('ats_score', None)
        return redirect(url_for('home'))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT question FROM interview_questions")
    all_questions = [row[0] for row in cursor.fetchall()]
    selected_questions = random.sample(all_questions, 4) if len(all_questions) >= 4 else all_questions
    return render_template("interview.html", questions=selected_questions)


@app.route('/coding')
def coding():
    return render_template("coding.html")


@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    raw_answers = request.form.get("answers", "")
    if not raw_answers.strip():
        return render_template("results.html", error="No answers provided.")
    answers = [line.strip() for line in raw_answers.splitlines() if line.strip()]
    if not answers:
        return render_template("results.html", error="No valid answers provided.")

    combined_text = " ".join(answers)
    grammar_score = get_grammar_score(combined_text)
    communication_score = get_communication_score(combined_text)
    voice_tone_score = get_voice_tone_score(combined_text)
    confidence_score = get_confidence_score(combined_text)

    answer_type = detect_answer_type(combined_text)

    overall_score = round((grammar_score + communication_score + (voice_tone_score * 10) + confidence_score) / 4, 2)
    overall_score = max(0, min(100, overall_score))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO interview_answers
        (username, answers, grammar_score, communication_score, voice_tone_score, confidence_score, overall_score, answer_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        session['username'],
        raw_answers,
        grammar_score,
        communication_score,
        voice_tone_score * 10,
        confidence_score,
        overall_score,
        answer_type
    ))
    conn.commit()
    conn.close()
    # Conditional redirect
    if overall_score > 49:
        return redirect(url_for('mcq'))  # Go to MCQ page
    else:
        flash(f"Your interview score is {overall_score}%. You need more than 50% to proceed to the next round.")
        return render_template('results.html',
                               answers=answers,
                               grammar_score=grammar_score,
                               communication_score=communication_score,
                               voice_tone_score=voice_tone_score * 10,
                               confidence_score=confidence_score,
                               overall_score=overall_score,
                               answer_type=answer_type)














# Judge0 config
JUDGE0_URL = "https://judge0-ce.p.rapidapi.com/submissions" 
JUDGE0_HEADERS = {
    "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
    "x-rapidapi-key": "5ce377b323mshe3f02ee25ceca4bp191893jsnb9e5640f94d6",
    "content-type": "application/json"
}


@app.route('/get_random_problem')
def get_problem():
    response = requests.get("https://codeforces.com/api/problemset.problems") 
    problems = response.json()["result"]["problems"]
    random_problem = random.choice([p for p in problems if 'name' in p and 'tags' in p])
    return jsonify({
        "title": f"{random_problem.get('index')} - {random_problem.get('name')}",
        "description": "This is a random problem from Codeforces.",
        "tags": random_problem.get("tags", []),
        "difficulty": random_problem.get("rating", "Unrated")
    })


@app.route('/submit_code_judge0', methods=["POST"])
def submit_code_judge0():
    data = request.get_json()
    source_code = data['code']
    language_id = int(data['lang'])
    stdin = data.get('stdin', '')

    submit_response = requests.post(JUDGE0_URL, json={
        "source_code": source_code,
        "language_id": language_id,
        "stdin": stdin
    }, headers=JUDGE0_HEADERS)

    token = submit_response.json()['token']
    time.sleep(3)
    result = requests.get(f"{JUDGE0_URL}/{token}", headers=JUDGE0_HEADERS).json()
    output = result.get("stdout", "") or result.get("compile_output", "") or result.get("stderr", "No output")
    return jsonify({"output": output})








def magnitude_filter(mag):
    return mag > np.percentile(mag, 75)


# API Endpoints
@app.route('/api/questions', methods=['GET'])
def get_questions():
    query = "SELECT * FROM coding_questions"
    result = fetch_all(query)
    if result is None:
        return jsonify({"error": "Failed to fetch questions"}), 500
    questions = []
    for row in result:
        question = {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'input': row[3],
            'output': row[4],
            'testcases': eval(row[5])  # Stored as JSON string or list in DB
        }
        questions.append(question)
    return jsonify(questions)


@app.route('/api/submit-code', methods=['POST'])
def submit_code_api():
    data = request.get_json()
    question_id = data.get('question_id')
    language_used = data.get('language')

    code_submitted = data.get('code')
    if not all([question_id, language_used, code_submitted]):
        return jsonify({"error": "Missing required fields"}), 400
    query = """
    INSERT INTO codingresults(submission_id,username,question_id,language_used,code_submitted,timestamp,
    score,judge0_output) VALUES(%s, %s, %s, %s, %s, NOW(), 0, '')
    
    """
    params = (question_id, language_used, code_submitted)
    success = execute_query(query, params)
    if not success:
        return jsonify({"error": "Failed to save code submission"}), 500
    return jsonify({"status": "success"})


@app.route('/api/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    rating = data.get('rating')
    comments = data.get('feedback')
    if rating is None or comments is None:
        return jsonify({"error": "Rating and feedback are required"}), 400
    query = """
    INSERT INTO feedback (rating, comments)
    VALUES (%s, %s)
    """
    params = (rating, comments)
    success = execute_query(query, params)
    if not success:
        return jsonify({"error": "Failed to save feedback"}), 500
    return jsonify({"status": "success"})



import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from db_config import get_connection  # assuming you have a db connection helper

UPLOAD_FOLDER = 'webcam_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)





@app.route('/api/save-webcam-recording', methods=['POST'])
def save_webcam_recording():
    if 'webcam_video' not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    video_file = request.files['webcam_video']
    username = request.form.get('username')

    if not username:
        return jsonify({"error": "Username required"}), 400

    if video_file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Option A: Save file to disk and store path in DB
    filename = secure_filename(f"{username}_webcam_{int(time.time())}.webm")
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    video_file.save(file_path)

    # Option B: Read binary data and store in LONGBLOB column
    # video_data = video_file.read()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # If using file path
        query = """
        INSERT INTO coding_webrecord (username, video_path) VALUES (%s, %s)
        """

        # If using BLOB storage
        # query = """
        # INSERT INTO coding_webrecord (username, video) VALUES (%s, LOAD_FILE(%s))
        # """
        # cursor.execute(query, (username, file_path))

        cursor.execute(query, (username, filename))
        conn.commit()
        return jsonify({"status": "success", "filename": filename})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()





# === DATABASE CONFIGURATION ===
# === ROUTES ===
@app.route('/mcq')
def mcq():
    return render_template("mcq.html")

@app.route('/get_random_questions')
def get_random_questions():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        rounds = ['Aptitude', 'Logical Reasoning', 'Verbal Reasoning']
        all_questions = []

        for rnd in rounds:
            query = """
                SELECT * FROM mcqquestions
                WHERE round = %s
                ORDER BY RAND()
                LIMIT 10
            """
            cursor.execute(query, (rnd,))
            questions = cursor.fetchall()
            all_questions.extend(questions)

        return jsonify(all_questions)

    except Exception as e:
        print("Error fetching questions:", str(e))
        return jsonify({"error": "Failed to load questions"}), 500

    finally:
        cursor.close()
        conn.close()



@app.route('/submit_mcq_answers', methods=['POST'])
def submit_mcq_answers():
    if 'username' not in session:
        return jsonify({"status": "error", "message": "User not logged in"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    answers = data.get('answers')
    score = data.get('score')  # total_score
    ai_score = data.get('ai_score')

    if not answers or score is None or ai_score is None:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    username = session['username']
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Insert individual answers
        for ans in answers:
            q_round = ans.get('round')
            q_text = ans.get('question')
            selected = ans.get('selected')
            correct = ans.get('correct')

            if not all([q_round, q_text, selected, correct]):
                print("Skipping incomplete answer:", ans)
                continue

            answer_query = """
                INSERT INTO mcqanswers 
                (username, round, question, selected_answer, correct_answer) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(answer_query, (username, q_round, q_text, selected, correct))

        # Insert final result
        result_query = """
            INSERT INTO mcqresults 
            (username, total_score, ai_score) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            total_score = VALUES(total_score),
            ai_score = VALUES(ai_score)
        """
        cursor.execute(result_query, (username, score, ai_score))
        conn.commit()

        # Save score in session
        session['mcq_score'] = score

        # Conditional redirect
        redirect_url = "/coding" if score > 10 else "/dashboard"
        return jsonify({
            "status": "success",
            "redirect": redirect_url
        })

    except Exception as e:
        conn.rollback()
        print("Error inserting MCQ data:", str(e))
        return jsonify({"status": "error", "message": "Failed to save answers."}), 500

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)

