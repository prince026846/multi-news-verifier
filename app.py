import os
import re
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# ML baseline
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from langdetect import detect
from deep_translator import GoogleTranslator

# Text extraction libraries
import pytesseract
from PIL import Image
import speech_recognition as sr
import moviepy.editor as mp

load_dotenv()

# API Keys
FACTCHECK_API_KEY = os.getenv("FACTCHECK_API_KEY", "")
BING_API_KEY = os.getenv("BING_API_KEY", "")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
NEWSAPI_AI_KEY = os.getenv("NEWSAPI_AI_KEY", "")
NEWSDATA_IO_KEY = os.getenv("NEWSDATA_IO_KEY", "")
# Added for Google Custom Search
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID", "")

# app = Flask(__name__)
app = Flask(__name__, template_folder="templates")
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Training data
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

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
    ("logreg", LogisticRegression(max_iter=300))
])
model.fit(texts, labels)

# Helper functions
def safe_detect_lang(text):
    try:
        return detect(text)
    except Exception:
        return "en"

def translate_text(text, target="en"):
    try:
        if not text.strip():
            return text
        return GoogleTranslator(source="auto", target=target).translate(text)
    except Exception:
        return text

def normalize_query(text):
    text = re.sub(r"\s+", " ", text).strip()
    return text[:300]

# Text extraction functions
def extract_text_from_image(file_path):
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Error extracting text from image: {str(e)}"

def extract_text_from_audio(file_path):
    try:
        r = sr.Recognizer()
        audio_clip = mp.AudioFileClip(file_path)
        temp_wav = file_path + ".wav"
        audio_clip.write_audiofile(temp_wav, logger=None)
        audio_clip.close()
        
        with sr.AudioFile(temp_wav) as source:
            audio = r.record(source)
        text = r.recognize_google(audio)
        
        if os.path.exists(temp_wav):
            os.remove(temp_wav)
        return text
    except Exception as e:
        return f"Error extracting text from audio: {str(e)}"

def extract_text_from_video(file_path):
    try:
        video = mp.VideoFileClip(file_path)
        audio = video.audio
        temp_audio = file_path + ".wav"
        audio.write_audiofile(temp_audio, logger=None)
        audio.close()
        video.close()
        
        text = extract_text_from_audio(temp_audio)
        
        if os.path.exists(temp_audio):
            os.remove(temp_audio)
        return text
    except Exception as e:
        return f"Error extracting text from video: {str(e)}"

def process_uploaded_file(file):
    if not file or file.filename == '':
        return ""
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    try:
        file_ext = filename.lower().split('.')[-1]
        
        if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']:
            extracted_text = extract_text_from_image(file_path)
        elif file_ext in ['mp3', 'wav', 'flac', 'm4a', 'aac']:
            extracted_text = extract_text_from_audio(file_path)
        elif file_ext in ['mp4', 'avi', 'mov', 'mkv', 'flv']:
            extracted_text = extract_text_from_video(file_path)
        elif file_ext in ['txt']:
            with open(file_path, 'r', encoding='utf-8') as f:
                extracted_text = f.read()
        else:
            extracted_text = f"Unsupported file format: {file_ext}"
        
        os.remove(file_path)
        return extracted_text
        
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        return f"Error processing file: {str(e)}"

# Enhanced evidence providers with AI
def search_newsapi_ai(query):
    """AI-powered news search with real-time data"""
    if not NEWSAPI_AI_KEY:
        return []
    
    url = "https://newsapi.ai/api/v1/article/getArticles"
    payload = {
        'query': {
            '$query': {
                '$and': [
                    {'conceptUri': f'http://en.wikipedia.org/wiki/{query.replace(" ", "_")}'},
                    {'lang': 'eng'}
                ]
            },
            '$filter': {
                'forceMaxDataTimeWindow': 7
            }
        },
        'resultType': 'articles',
        'articlesPage': 1,
        'articlesCount': 20,
        'articlesSortBy': 'date',
        'apiKey': NEWSAPI_AI_KEY
    }
    
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.ok:
            data = r.json()
            articles = data.get('articles', {}).get('results', [])
            out = []
            for article in articles:
                source_title = article.get('source', {}).get('title', 'Unknown')
                out.append({
                    "type": "newsapi_ai",
                    "title": article.get('title', ''),
                    "url": article.get('url', ''),
                    "source": source_title,
                    "sentiment": article.get('sentiment', 0),
                    "publishedAt": article.get('dateTime', ''),
                    "body": article.get('body', '')[:200],
                    "confidence": "high"
                })
            return out
    except Exception:
        return []
    return []

def search_newsdata_io(query):
    """Real-time news from NewsData.io"""
    if not NEWSDATA_IO_KEY:
        return []
    
    url = "https://newsdata.io/api/1/news"
    params = {
        'apikey': NEWSDATA_IO_KEY,
        'q': query,
        'language': 'en',
        'size': 15
    }
    
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.ok:
            data = r.json()
            out = []
            for article in data.get('results', []):
                out.append({
                    "type": "newsdata_io",
                    "title": article.get('title', ''),
                    "url": article.get('link', ''),
                    "source": article.get('source_id', ''),
                    "publishedAt": article.get('pubDate', ''),
                    "description": article.get('description', ''),
                    "category": article.get('category', []),
                    "confidence": "high"
                })
            return out
    except Exception:
        return []
    return []

def search_factcheck_google(query):
    """Google Fact Check Tools API"""
    if not FACTCHECK_API_KEY:
        return []
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {"query": query, "key": FACTCHECK_API_KEY, "pageSize": 10, "languageCode": "en"}
    try:
        r = requests.get(url, params=params, timeout=8)
        if r.ok:
            data = r.json()
            out = []
            for c in data.get("claims", []):
                claim_text = c.get("text", "")
                for rev in c.get("claimReview", []):
                    out.append({
                        "type": "factcheck",
                        "claim": claim_text,
                        "rating": rev.get("textualRating", ""),
                        "publisher": (rev.get("publisher") or {}).get("name", ""),
                        "url": rev.get("url", ""),
                        "confidence": "very_high"
                    })
            return out
    except Exception:
        pass
    return []

def search_bing_web(query):
    """Bing Web Search for additional verification"""
    if not BING_API_KEY:
        return []
    endpoint = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {"q": query, "mkt": "en-IN", "count": 15, "textDecorations": False}
    try:
        r = requests.get(endpoint, headers=headers, params=params, timeout=8)
        r.raise_for_status()
        js = r.json()
        results = []
        for it in (js.get("webPages", {}) or {}).get("value", []):
            results.append({
                "type": "bing",
                "title": it.get("name", ""),
                "url": it.get("url", ""),
                "snippet": it.get("snippet", ""),
                "source": it.get("displayUrl", ""),
                "confidence": "medium"
            })
        return results
    except Exception:
        return []

def search_newsapi(query):
    """Original NewsAPI for additional coverage"""
    if not NEWSAPI_KEY:
        return []
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 15,
        "apiKey": NEWSAPI_KEY
    }
    try:
        r = requests.get(url, params=params, timeout=8)
        if r.ok:
            js = r.json()
            out = []
            for a in js.get("articles", []):
                out.append({
                    "type": "newsapi",
                    "title": a.get("title", ""),
                    "url": a.get("url", ""),
                    "source": (a.get("source") or {}).get("name", ""),
                    "publishedAt": a.get("publishedAt", ""),
                    "description": a.get("description", ""),
                    "confidence": "medium"
                })
            return out
    except Exception:
        pass
    return []

# New function for Google Custom Search
def search_google_web(query):
    """Performs a Google web search for general verification."""
    if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
        return []
    
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': GOOGLE_API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
        'num': 10  # Number of results to return
    }
    
    try:
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
        results = []
        
        for item in data.get("items", []):
            results.append({
                "type": "google_search",
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "source": item.get("displayLink", ""),
                "confidence": "medium"
            })
        return results
    except Exception as e:
        print(f"Google Search Error: {e}")
        return []

# Enhanced trusted domains
TRUSTED_DOMAINS = [
    # Government sources
    "pib.gov.in", "pressinformationbureau.gov.in", "mha.gov.in", "mea.gov.in", "mohfw.gov.in",
    "eci.gov.in", "rbi.org.in", "isro.gov.in", "india.gov.in", "pmindia.gov.in",
    # Major Indian news
    "timesofindia.indiatimes.com", "indianexpress.com", "thehindu.com", "hindustantimes.com",
    "ndtv.com", "news18.com", "republicworld.com", "zeenews.india.com", "aajtak.in",
    "financialexpress.com", "businesstoday.in", "economictimes.indiatimes.com",
    # International trusted
    "bbc.com", "reuters.com", "apnews.com", "cnn.com", "bloomberg.com", "wsj.com",
    "aljazeera.com", "theguardian.com", "washingtonpost.com", "nytimes.com",
    # Legal/Court news
    "barandbench.com", "livelaw.in", "scobserver.in"
]

FACT_CHECK_DOMAINS = [
    "factcheck.org", "snopes.com", "politifact.com", "boomlive.in", "altnews.in",
    "vishvasnews.com", "fullfact.org", "checkyourfact.com", "factchecker.in"
]

def is_trusted(url):
    try:
        from urllib.parse import urlparse
        host = urlparse(url).netloc.lower()
        return any(dom in host for dom in TRUSTED_DOMAINS)
    except Exception:
        return False

def is_fact_checker(url):
    try:
        from urllib.parse import urlparse
        host = urlparse(url).netloc.lower()
        return any(dom in host for dom in FACT_CHECK_DOMAINS)
    except Exception:
        return False

def baseline_ml_label(text_en):
    try:
        proba = model.predict_proba([text_en])[0]
        classes = model.classes_
        best_idx = proba.argmax()
        return classes[best_idx], float(proba[best_idx])
    except Exception:
        return "real", 0.5

# Updated function to include the call to Google Search
def aggregate_evidence(query_en):
    """Collect evidence from multiple AI-powered sources"""
    evidence = []
    
    # Priority 1: Official fact-checks
    fc = search_factcheck_google(query_en)
    evidence.extend(fc)
    
    # Priority 2: AI-powered news sources
    ai_news = search_newsapi_ai(query_en)
    evidence.extend(ai_news)
    
    # Priority 3: Real-time news
    realtime_news = search_newsdata_io(query_en)
    evidence.extend(realtime_news)
    
    # Priority 4: Standard news APIs
    regular_news = search_newsapi(query_en)
    evidence.extend(regular_news)

    # Added call to new Google Search function
    google_results = search_google_web(query_en)
    evidence.extend(google_results)
    
    # Priority 5: General web search
    bing_results = search_bing_web(query_en)
    evidence.extend(bing_results)
    
    return evidence

def decide_verdict(text_en, evidence):
    """Enhanced verdict logic with AI-powered sources"""
    # Categorize evidence by type and quality
    fact_checks = [e for e in evidence if e.get("type") == "factcheck"]
    ai_news = [e for e in evidence if e.get("type") == "newsapi_ai"]
    realtime_news = [e for e in evidence if e.get("type") == "newsdata_io"]
    regular_news = [e for e in evidence if e.get("type") == "newsapi"]
    google_results = [e for e in evidence if e.get("type") == "google_search"]
    bing_results = [e for e in evidence if e.get("type") == "bing"]
    
    # All news sources combined
    all_news = ai_news + realtime_news + regular_news + bing_results + google_results
    trusted_sources = [e for e in all_news if is_trusted(e.get("url", ""))]
    fact_check_sources = [e for e in all_news if is_fact_checker(e.get("url", ""))]
    
    # Priority 1: Official fact-checks
    if fact_checks:
        ratings_text = " | ".join(f'{e.get("publisher","")}: {e.get("rating","")}' for e in fact_checks[:3])
        rating_blob = " ".join((e.get("rating") or "").lower() for e in fact_checks)
        
        true_indicators = ["true", "correct", "accurate", "verified", "legitimate"]
        false_indicators = ["false", "fake", "incorrect", "debunked", "misleading", "fabricated"]
        
        if any(indicator in rating_blob for indicator in true_indicators):
            return "Fact", f"✅ Official fact-checkers confirm this is TRUE. Sources: {ratings_text}"
        if any(indicator in rating_blob for indicator in false_indicators):
            return "Misconception", f"❌ Official fact-checkers confirm this is FALSE. Sources: {ratings_text}"
        return "Needs more proof", f"⚠️ Mixed fact-check results. Sources: {ratings_text}"
    
    # Priority 2: AI-powered news verification
    if len(ai_news) >= 2:
        trusted_ai = [e for e in ai_news if is_trusted(e.get('url', ''))]
        if len(trusted_ai) >= 1:
            return "Fact", f"✅ Verified by AI-powered news analysis from {len(ai_news)} sources including {len(trusted_ai)} trusted outlets"
    
    # Priority 3: Real-time news confirmation
    if len(realtime_news) >= 3:
        trusted_realtime = [e for e in realtime_news if is_trusted(e.get('url', ''))]
        if len(trusted_realtime) >= 2:
            return "Fact", f"✅ Confirmed by {len(trusted_realtime)} trusted real-time news sources"
    
    # Priority 4: Multiple trusted sources
    if len(trusted_sources) >= 3:
        return "Fact", f"✅ Reported by {len(trusted_sources)} trusted news sources"
    
    if len(trusted_sources) >= 2:
        return "Fact", f"✅ Confirmed by {len(trusted_sources)} credible sources"
    
    # Priority 5: Fact-checker sources
    if len(fact_check_sources) >= 1:
        return "Fact", f"✅ Corroborated by fact-checking organizations"
    
    # Priority 6: Official content detection
    official_indicators = ["supreme court", "election commission", "government announces", "ministry", 
                           "rbi", "isro", "parliament", "lok sabha", "rajya sabha", "high court"]
    if any(indicator in text_en.lower() for indicator in official_indicators):
        if len(all_news) >= 3:
            return "Fact", f"✅ Official government/institutional news with widespread coverage ({len(all_news)} sources)"
        elif len(trusted_sources) >= 1:
            return "Fact", f"✅ Official news confirmed by trusted sources"
    
    # Priority 7: Enhanced suspicious content detection
    lbl, conf = baseline_ml_label(text_en)
    suspicious_keywords = ["free money", "forward to", "share now", "breaking:", "urgent", 
                           "shocking", "died within hours", "whatsapp will charge", "click here"]
    
    if lbl == "fake" and conf >= 0.7:
        if any(keyword in text_en.lower() for keyword in suspicious_keywords):
            return "Misconception", f"🚨 High suspicion: Contains typical misinformation patterns (AI confidence: {conf:.1%})"
    
    # Priority 8: Coverage analysis
    total_sources = len(evidence)
    if total_sources == 0:
        return "Needs more proof", "📊 No verification sources found online"
    
    if len(trusted_sources) == 0 and total_sources >= 5:
        return "Needs more proof", f"⚠️ Found {total_sources} sources but none from verified outlets"
    
    if len(all_news) >= 1 and len(trusted_sources) == 0:
        return "Needs more proof", f"⚠️ Limited verification - found {len(all_news)} sources but need trusted confirmation"
    
    return "Needs more proof", "⚠️ Insufficient evidence for confident verdict"

def format_evidence_text(evidence, target_lang="auto"):
    """Enhanced evidence formatting with AI sources"""
    lines = []
    
    # Group evidence by type
    fact_checks = [e for e in evidence if e.get("type") == "factcheck"]
    ai_news = [e for e in evidence if e.get("type") == "newsapi_ai"]
    realtime_news = [e for e in evidence if e.get("type") == "newsdata_io"]
    regular_news = [e for e in evidence if e.get("type") == "newsapi"]
    google_results = [e for e in evidence if e.get("type") == "google_search"]
    bing_results = [e for e in evidence if e.get("type") == "bing"]
    
    if fact_checks:
        lines.append("🔍 Official Fact-Checks:")
        for e in fact_checks[:3]:
            lines.append(f"  • {e.get('publisher','Unknown')}: '{e.get('rating','')}' - {e.get('url','')}")
    
    if ai_news:
        lines.append(f"\n🤖 AI-Powered News Analysis ({len(ai_news)} sources):")
        for e in ai_news[:4]:
            trust_mark = "✓" if is_trusted(e.get('url','')) else "?"
            sentiment = e.get('sentiment', 0)
            sentiment_text = f"(Sentiment: {sentiment:.2f})" if sentiment != 0 else ""
            lines.append(f"  {trust_mark} {e.get('source','?')}: {e.get('title','').strip()[:80]}... {sentiment_text}")
    
    if realtime_news:
        lines.append(f"\n⚡ Real-Time News ({len(realtime_news)} sources):")
        for e in realtime_news[:4]:
            trust_mark = "✓" if is_trusted(e.get('url','')) else "?"
            lines.append(f"  {trust_mark} {e.get('source','?')}: {e.get('title','').strip()[:80]}...")
    
    if regular_news:
        lines.append(f"\n📰 News Coverage ({len(regular_news)} articles):")
        trusted_regular = [e for e in regular_news if is_trusted(e.get('url',''))][:3]
        for e in trusted_regular:
            lines.append(f"  ✓ {e.get('source','?')}: {e.get('title','').strip()[:80]}...")
    
    if google_results:
        lines.append(f"\n🌐 Google Web Search ({len(google_results)} articles):")
        trusted_google = [e for e in google_results if is_trusted(e.get('url',''))][:3]
        for e in trusted_google:
            lines.append(f"  ✓ {e.get('source','?')}: {e.get('title','').strip()[:80]}...")
            
    if bing_results:
        trusted_web = [e for e in bing_results if is_trusted(e.get('url',''))]
        if trusted_web:
            lines.append(f"\n🌐 Trusted Web Sources ({len(trusted_web)} verified):")
            for e in trusted_web[:3]:
                lines.append(f"  ✓ {e.get('source','?')}: {e.get('title','').strip()[:80]}...")
    
    text = "\n".join(lines) if lines else "No evidence found."
    
    if target_lang and target_lang != "auto":
        try:
            return translate_text(text, target_lang)
        except Exception:
            return text
    return text

# Main route
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        raw_text = request.form.get("news_text", "") or ""
        target_lang = request.form.get("target_lang", "auto")
        uploaded_file = request.files.get('file_upload')
        
        # Process uploaded file
        extracted_text = ""
        if uploaded_file and uploaded_file.filename:
            extracted_text = process_uploaded_file(uploaded_file)
            if extracted_text and not extracted_text.startswith("Error"):
                raw_text = extracted_text if not raw_text.strip() else raw_text + "\n\n[Extracted from file]:\n" + extracted_text

        if not raw_text.strip():
            return render_template("index.html", 
                                   result="Please enter some text or upload a file.", 
                                   original_text=raw_text, 
                                   target_lang=target_lang)

        # Process the text
        src_lang = safe_detect_lang(raw_text)
        text_en = raw_text if src_lang.startswith("en") else translate_text(raw_text, "en")

        query = normalize_query(text_en)
        evidence = aggregate_evidence(query)
        verdict, reason = decide_verdict(text_en, evidence)

        # Format results with enhanced display
        head = f"🎯 Verdict: {verdict}\n💭 Analysis: {reason}\n"
        evid_txt = format_evidence_text(evidence, target_lang=target_lang)
        head_disp = translate_text(head, target_lang) if target_lang != "auto" else head

        return render_template("index.html",
                               result=head_disp + "\n" + evid_txt,
                               original_text=raw_text,
                               target_lang=target_lang)

    return render_template("index.html", result=None, original_text="", target_lang="auto")

if __name__ == "__main__":
    app.run(debug=True)


# @app.route("/api/dashboard")
# def dashboard_data():
#     # Example data — replace with DB/logic
#     data = {
#         "pieData": [
#             {"name": "Real", "value": 55},
#             {"name": "Fake", "value": 30},
#             {"name": "Needs Proof", "value": 15},
#         ],
#         "barData": [
#             {"day": "Mon", "count": 20},
#             {"day": "Tue", "count": 35},
#             {"day": "Wed", "count": 25},
#             {"day": "Thu", "count": 40},
#             {"day": "Fri", "count": 30},
#             {"day": "Sat", "count": 22},
#             {"day": "Sun", "count": 15},
#         ],
#         "recentResults": [
#             {"id": 1, "text": "Climate summit news", "status": "Real"},
#             {"id": 2, "text": "Celebrity hoax", "status": "Fake"},
#             {"id": 3, "text": "Sports update", "status": "Real"},
#             {"id": 4, "text": "Misinformation tweet", "status": "Needs Proof"},
#             {"id": 5, "text": "Local festival report", "status": "Real"},
#         ]
#     }
#     return jsonify(data)