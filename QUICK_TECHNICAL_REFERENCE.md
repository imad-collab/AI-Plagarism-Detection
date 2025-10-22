# 📚 Quick Technical Reference

## At a Glance

**Language:** Python 3.11.13  
**Framework:** Flask 2.3.3  
**Core AI Engine:** LangChain 0.1.7  
**LLM Models:** HuggingFace RoBERTa + sentence-transformers  
**Vector Database:** FAISS  
**Frontend:** HTML5, CSS3, Vanilla JavaScript  
**Status:** Production Ready ✅

---

## Essential Stack

### Backend
```
Flask 2.3.3          → Web framework & API routing
Python 3.11.13       → Core language
LangChain 0.1.7      → ML orchestration & algorithms
```

### Machine Learning
```
HuggingFace          → Pre-trained transformer models
  - sentence-transformers/all-MiniLM-L6-v2 (embeddings)
  - roberta-base-openai-detector (AI detection)
LangChain            → 7 ML algorithms (cosine, Jaccard, etc.)
FAISS                → Vector similarity search
scikit-learn         → ML utilities
```

### NLP & Text Processing
```
NLTK                 → Sentence tokenization & NLP
difflib              → String similarity (SequenceMatcher)
regex (re module)    → Pattern matching & fallback tokenization
```

### File Processing
```
PyPDF2               → PDF text extraction
python-docx          → DOCX/Word document processing
```

### Frontend
```
HTML5/CSS3           → UI structure & styling
Vanilla JavaScript   → Interactive client-side logic
Fetch API            → REST communication
```

---

## Complete Dependencies

### Required Packages (from requirements.txt)
```
Flask==2.3.3
LangChain==0.1.7
transformers>=4.30.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.4
PyPDF2>=3.0
python-docx>=0.8.11
nltk>=3.8
scikit-learn>=1.3.0
numpy>=1.24.0
scipy>=1.11.0
requests>=2.31.0
```

### Transitive Dependencies (Automatically Installed)
```
pydantic
torch
joblib
tqdm
regex
lxml
filelock
tokenizers
safetensors
click
jinja2
werkzeug
```

---

## LLM Models Used

### 1. Sentence Embeddings
**Model:** `sentence-transformers/all-MiniLM-L6-v2`
- Type: Transformer-based embedding model
- Size: 90.9MB (lightweight!)
- Dimensions: 384
- Use: Semantic similarity, text embeddings
- Speed: Fast inference
- Accuracy: High-quality representations

### 2. AI-Generated Text Detection
**Model:** `roberta-base-openai-detector`
- Type: RoBERTa (Robustly Optimized BERT)
- Task: Binary classification (Human vs AI)
- Accuracy: 92% on academic content
- Training: Trained on GPT-2 generated text
- Use: Detecting AI-generated content

---

## 7 Machine Learning Algorithms

### Implemented via LangChain
1. **Cosine Similarity** - Vector-based similarity
2. **Jaccard Similarity** - Set-based overlap
3. **Token Overlap** - Word-level matching
4. **Sequence Matching** - String similarity (difflib)
5. **Bigram Analysis** - Two-word patterns
6. **Trigram Analysis** - Three-word patterns
7. **Sentence-Level Analysis** - Semantic comparison

**Ensemble Result:** Weighted voting of all 7 algorithms

---

## API Endpoints

### Core Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/upload` | POST | File upload |
| `/api/analyze` | POST | Plagiarism analysis |
| `/api/highlight` | POST | Text highlighting |
| `/api/langchain-analysis` | POST | Advanced ML analysis |
| `/api/documents/<id>` | GET | Document metadata |
| `/api/documents/<id>/content` | GET | Full document text |

### Debug Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/debug/highlight-test` | POST | Test highlighting |

---

## File Support

### Supported Formats
```
✓ PDF (.pdf)      → PyPDF2 extraction
✓ DOCX (.docx)    → python-docx extraction
✓ DOC (.doc)      → Limited support
✓ TXT (.txt)      → Direct reading
✓ RTF (.rtf)      → Text extraction
```

### Maximum File Size
```
16MB limit (configurable)
```

---

## Performance Specs

| Task | Time | Algorithm |
|------|------|-----------|
| File Upload | < 2s | Werkzeug |
| PDF Extraction | 0.5s/page | PyPDF2 |
| Model Loading | 30-60s | HuggingFace |
| Single Inference | < 1s | Transformers |
| 7-Algorithm Run | 2-5s | LangChain |
| Text Highlighting | < 0.5s | difflib |
| **Total Response** | **3-7s** | **Ensemble** |

---

## System Architecture

```
Frontend (HTML/CSS/JS)
        ↓ Fetch API (JSON)
REST API (Flask) - 12 endpoints
        ↓
Business Logic Layer
        ↓
┌─────────────────────────────┐
│  ML & NLP Processing         │
├──────────┬──────────┬────────┤
│LangChain │HuggingFace│NLTK   │
└──────────┴──────────┴────────┘
        ↓
File Processing (PyPDF2, python-docx)
        ↓
Storage (File System + JSON Metadata)
```

---

## Key Features by Technology

### LangChain Features
- 7 ML algorithms in ensemble
- Semantic analysis pipeline
- Lazy model initialization
- Result aggregation & voting

### HuggingFace Features
- Pre-trained models (no training required)
- Fast inference
- Automatic caching
- Multiple model options

### Flask Features
- RESTful API routing
- File upload handling
- JSON response formatting
- Error handling middleware

### NLTK Features
- Sentence tokenization (PUNKT)
- Word tokenization (fallback)
- Linguistic analysis

### difflib Features
- SequenceMatcher for string comparison
- Similarity ratio calculation
- Efficient string matching

---

## Configuration

### Default Settings
```python
# Flask
DEBUG = False                    # Production mode
HOST = 127.0.0.1
PORT = 5001

# File Upload
UPLOAD_FOLDER = 'uploads/'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# LangChain
LAZY_LOAD_MODELS = True         # Optimize startup
MODEL_CACHE_DIR = '.cache/'

# Similarity
DEFAULT_THRESHOLD = 0.60        # 60% minimum
```

---

## Development Tools

### Testing
```
pytest              → Unit testing (optional)
curl                → API testing
Browser DevTools    → Frontend debugging
```

### Monitoring
```
logging module      → Application logging
print statements    → Debug output
Browser console     → Frontend logs
```

---

## Deployment Options

### Development
```bash
python app.py                    # Flask development server
```

### Production
```bash
gunicorn app:app                 # WSGI server
docker build -t plagiarism .     # Docker containerization
```

### Cloud
```
AWS EC2             → Direct deployment
Google Cloud Run    → Serverless
Azure App Service   → Managed service
Heroku              → Simple deployment
```

---

## Memory & Resource Usage

| Component | Memory | Disk |
|-----------|--------|------|
| Python Runtime | ~50MB | - |
| Flask + Dependencies | ~200MB | ~800MB |
| HuggingFace Models | ~500MB | ~1.5GB |
| Inference (running) | ~1-2GB | - |
| **Total Required** | **2-4GB** | **2-3GB** |

---

## Security Features

### Implemented
```
✓ Secure filename generation (Werkzeug)
✓ File type validation
✓ Input sanitization
✓ Error message hiding (production)
✓ No data persistence by default
✓ File size limits
```

### Recommended for Production
```
□ HTTPS/SSL encryption
□ API authentication (API keys)
□ Rate limiting
□ CORS configuration
□ Database encryption
□ Audit logging
```

---

## Environment Setup

### Requirements
```
Operating System    → macOS, Linux, Windows (WSL2)
Python Version      → 3.11+
Virtual Environment → venv (recommended)
Internet            → Yes (for model download)
```

### Installation
```bash
# Clone repository
git clone https://github.com/imad-collab/AI-Plagarism-Detection.git
cd AI-Plagarism-Detection

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Access
open http://127.0.0.1:5001
```

---

## Monitoring & Logging

### Log Locations
```
Console Output      → Real-time logs during development
app.log             → Application logs (if configured)
Browser Console     → Frontend logs (F12)
```

### Key Metrics to Monitor
```
✓ API response time
✓ File upload size
✓ Model inference time
✓ Error rates
✓ Memory usage
✓ File system space
```

---

## Version Compatibility

| Component | Supported | Tested |
|-----------|-----------|--------|
| Python | 3.11+ | 3.11.13 ✓ |
| Flask | 2.3.x | 2.3.3 ✓ |
| LangChain | 0.1.x+ | 0.1.7 ✓ |
| HuggingFace | Latest | 4.33+ ✓ |
| Node.js | N/A | N/A |

---

## Troubleshooting

### Common Issues

**Issue:** Model download on first run takes long
- **Solution:** Pre-download with `transformers-cli download roberta-base-openai-detector`

**Issue:** Out of memory during inference
- **Solution:** Increase RAM or use CPU-only version (`faiss-cpu`)

**Issue:** File upload fails
- **Solution:** Check file size (max 16MB), supported format (.pdf, .docx, .txt)

**Issue:** Slow response time
- **Solution:** Use SSD for file storage, increase RAM

---

## Best Practices

### Development
```
✓ Use virtual environment
✓ Install from requirements.txt
✓ Test API with curl/Postman
✓ Use browser DevTools for frontend
✓ Enable debug mode for development
```

### Production
```
✓ Use WSGI server (Gunicorn)
✓ Enable HTTPS/SSL
✓ Set DEBUG = False
✓ Implement authentication
✓ Monitor resource usage
✓ Use database for persistence
✓ Enable logging
✓ Set up error alerting
```

---

## Resources

### Official Documentation
- Flask: https://flask.palletsprojects.com/
- LangChain: https://docs.langchain.com/
- HuggingFace: https://huggingface.co/docs
- NLTK: https://www.nltk.org/
- scikit-learn: https://scikit-learn.org/

### GitHub Repository
- https://github.com/imad-collab/AI-Plagarism-Detection

### Community Support
- Stack Overflow (tag: flask, langchain, huggingface)
- GitHub Issues
- Slack communities

---

**Last Updated:** October 22, 2025  
**Status:** Production Ready  
**For Questions:** Check GitHub Issues or reach out to maintainers
