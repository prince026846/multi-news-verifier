# app.py
import os
import mimetypes
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# text/image/audio/video processing
from PIL import Image
import pytesseract
import docx2txt
import PyPDF2
import whisper
# from moviepy.editor import VideoFileClip

# simple AI model
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# utilities
from langdetect import detect
from deep_translator import GoogleTranslator

# Create app and folders
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ----- Adjust this if tesseract is not found on Windows -----
# If you are on Windows and installed Tesseract in "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# uncomment and set path:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ---- Load Whisper model ONCE (tiny is fast for CPU demos; swap to "small" if you have time) ----
print("Loading Whisper model (this may take some seconds)...")
whisper_model = whisper.load_model("tiny")  # small models are faster; change to "small" if CPU is faster

# ----- Simple demo dataset to teach the tiny AI (replace with bigger dataset later) -----
fake_samples = [
    "Free 5000 rupees from government to all citizens, click here",
    "Breaking: actor died due to vaccine within hours share now",
    "WhatsApp will charge 5 rupees per message tomorrow forward to 10 people",
    "Modi giving free laptops to students register now",
    "NASA confirms sun rose from west today shocking"
]
real_samples = [
    "Government announces scholarship program for engineering students",
    "ISRO successfully launches PSLV mission from Sriharikota",
    "New traffic rules notified by Ministry of Road Transport",
    "University releases exam timetable for the semester",
    "RBI keeps repo rate unchanged in latest policy"
]
texts = fake_samples + real_samples
labels = ["fake"] * len(fake_samples) + ["real"] * len(real_samples)

# ----- Train a tiny TF-IDF + LogisticRegression model -----
model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=5000)),
    ("logreg", LogisticRegression(max_iter=400))
])
model.fit(texts, labels)
print("Tiny AI model trained (demo).")

# ----- Helper: extract text from uploaded file -----
def extract_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext in [".txt", ".text"]:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        elif ext == ".pdf":
            txt = []
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for p in reader.pages:
                    page_text = p.extract_text()
                    if page_text:
                        txt.append(page_text)
            return "\n".join(txt)
        elif ext in [".docx"]:
            return docx2txt.process(filepath)
        elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
            img = Image.open(filepath)
            text = pytesseract.image_to_string(img)
            return text
        elif ext in [".mp3", ".wav", ".m4a", ".ogg"]:
            # use whisper for speech-to-text
            res = whisper_model.transcribe(filepath)
            return res.get("text", "")
        elif ext in [".mp4", ".mov", ".mkv", ".avi"]:
            # Extract audio from video and transcribe, also try OCR from one frame
            clip = VideoFileClip(filepath)
            audio_path = filepath + "_audio.wav"
            # write audio
            clip.audio.write_audiofile(audio_path, logger=None)
            res = whisper_model.transcribe(audio_path)
            audio_text = res.get("text", "")
            # save one frame (at 1s) and OCR it
            frame_path = filepath + "_frame.jpg"
            try:
                clip.save_frame(frame_path, t=1.0)
                frame_text = pytesseract.image_to_string(Image.open(frame_path))
            except Exception:
                frame_text = ""
            clip.close()
            # combine
            return audio_text + "\n" + frame_text
        else:
            return ""  # unknown extension
    except Exception as e:
        print("Error extracting:", e)
        return ""

# ----- Helper: classify text with tiny AI and give verdict + confidence -----
def verify_text(text):
    clean = (text or "").strip()
    if not clean:
        return "No content extracted", 0
    try:
        proba = model.predict_proba([clean])[0]
        classes = model.classes_
        best_idx = proba.argmax()
        best_label = classes[best_idx]
        best_conf = float(proba[best_idx])
        if best_conf < 0.60:
            return "Needs Confirmation", int(best_conf * 100)
        return ("Real" if best_label == "real" else "Fake"), int(best_conf * 100)
    except Exception as e:
        print("Verification error:", e)
        return "Needs Confirmation", 0

# ----- Helper: translate message to target language (target e.g., 'hi' for Hindi) -----
def translate_message(text, target_lang):
    try:
        if not target_lang or target_lang == "auto":
            return text
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception as e:
        print("Translation error:", e)
        return text

# ----- Web routes -----
@app.route("/", methods=["GET", "POST"])
def index():
    result_text = None
    confidence = None
    extracted_text = ""
    if request.method == "POST":
        # user can paste text or upload file
        pasted = request.form.get("pasted_text", "").strip()
        lang_choice = request.form.get("target_lang", "auto")
        file = request.files.get("file")
        if pasted:
            extracted_text = pasted
        elif file and file.filename != "":
            # save file
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            extracted_text = extract_text_from_file(path)
        else:
            result_text = "Please paste text or upload a file."
            return render_template("index.html", result=result_text, extracted_text=extracted_text)

        # detect language
        try:
            detected = detect(extracted_text) if extracted_text.strip() else "en"
        except Exception:
            detected = "en"

        # translate to English for the AI model (if needed)
        english_text = extracted_text
        if detected != "en":
            try:
                english_text = GoogleTranslator(source="auto", target="en").translate(extracted_text)
            except Exception:
                english_text = extracted_text

        # verify using the tiny AI
        verdict, conf = verify_text(english_text)

        # build message and translate back to requested language
        message = f"Verdict: {verdict}. Confidence: {conf}%. (This is an AI guess. Cross-check with official sources.)"
        output_lang = detected if lang_choice == "auto" else lang_choice
        final = translate_message(message, output_lang)

        result_text = final
        confidence = conf

    return render_template("index.html", result=result_text, extracted_text=extracted_text, confidence=confidence)

if __name__ == "__main__":
    app.run(debug=True)
