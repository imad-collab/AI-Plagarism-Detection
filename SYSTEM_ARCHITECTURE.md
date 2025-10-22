# 🏗️ System Architecture & Deployment Guide

## Complete System Architecture

### Overview
The AI Plagiarism Detection System is built using a modern, scalable architecture with clear separation of concerns across multiple layers.

---

## Architecture Layers

### 1. Presentation Layer (Frontend)

**Technologies:** HTML5, CSS3, Vanilla JavaScript

**Components:**
```
┌─────────────────────────────────────────┐
│      Web Interface (Browser)            │
├─────────────────────────────────────────┤
│  • File Upload UI (drag & drop)         │
│  • Multi-tab Results Display            │
│  • Color-coded Text Highlighting        │
│  • Progress Indicators                  │
│  • Error Messaging                      │
└─────────────────────────────────────────┘
        ↓ HTTP Requests (JSON)
   Fetch API Calls
```

**Files:**
- `templates/index.html` - Main UI
- `public/css/style.css` - Styling
- `public/js/main.js` - Interactivity

**Key Features:**
- Real-time form validation
- Asynchronous file upload
- Multi-tab navigation
- Color-coded result highlighting (Red/Orange/Yellow)
- Interactive UI elements

---

### 2. API Layer (REST Endpoints)

**Framework:** Flask 2.3.3

**Structure:**
```python
@app.route('/api/upload', methods=['POST'])
@app.route('/api/analyze', methods=['POST'])
@app.route('/api/highlight', methods=['POST'])
@app.route('/api/langchain-analysis', methods=['POST'])
@app.route('/api/documents/<file_id>', methods=['GET'])
@app.route('/api/documents/<file_id>/content', methods=['GET'])
```

**API Contract:**
```
Request Format:  JSON
Response Format: JSON with HTTP status codes
Authentication: Currently open (production: add tokens)
Rate Limiting: Optional (recommended for production)
```

**Response Structure:**
```json
{
  "success": true/false,
  "data": {...},
  "error": "error message if applicable",
  "timestamp": "ISO 8601 timestamp"
}
```

---

### 3. Business Logic Layer

**Components:**

#### Controllers (Request Handlers)
- `controllers/documentController.js` - Document management
- `controllers/plagiarismController.js` - Analysis orchestration

#### Services (Core Logic)
```
┌────────────────────────────────────────┐
│       Business Logic Services          │
├────────────────────────────────────────┤
│ • FileUploadService                    │
│ • AdvancedSimilarityService            │
│ • LangChainPlagiarismService           │
│ • TextHighlighter                      │
│ • TextAnalysisService                  │
└────────────────────────────────────────┘
```

#### Models (Data Structures)
- `models/document.js` - Document metadata
- `models/plagiarismResult.js` - Analysis results

---

### 4. Data Processing Layer

**File Processing:**
```
Input File → Format Detection → Parser → Text Extraction → Cleanup
   │
   ├─→ PDF → PyPDF2 → Page iteration → Text aggregation
   ├─→ DOCX → python-docx → Paragraph extraction
   ├─→ TXT → Direct read → Encoding check
   └─→ RTF → Text extraction → Normalization
```

**Text Normalization:**
```
Raw Text → Remove extra whitespace → Lowercase conversion → 
Tokenization → Stop word consideration → Output
```

---

### 5. Machine Learning & NLP Layer

**Architecture:**
```
┌──────────────────────────────────────────────┐
│     LangChain Orchestration Framework        │
├──────────────────────────────────────────────┤
│  Manages 7 Parallel Algorithms               │
└─────────────────┬──────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌────────┐  ┌────────┐  ┌────────┐
│Cosine  │  │Jaccard │  │Sequence│
│Similar │  │Similar │  │Matching│
└────────┘  └────────┘  └────────┘
    │             │             │
    └─────────────┼─────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌────────┐  ┌────────┐  ┌────────┐
│Bigram  │  │Trigram │  │Sentence│
│Analysis│  │Analysis│  │-Level  │
└────────┘  └────────┘  └────────┘
    │             │             │
    └─────────────┼─────────────┘
                  │
            ┌─────▼─────┐
            │  Ensemble │
            │   Voting  │
            └───────────┘
                  │
            Final Score
```

**Component Details:**

#### Text Embedding Pipeline
```
Input Text
    ↓
HuggingFace Tokenizer
    ↓
Transformer Encoding
    ↓
384-D Vector (all-MiniLM-L6-v2)
    ↓
FAISS Indexing (optional)
    ↓
Similarity Computation
```

#### Algorithm Implementation
```
1. Cosine Similarity
   - Vector-based comparison
   - Range: 0-1
   
2. Jaccard Similarity
   - Set-based comparison
   - Formula: |A∩B| / |A∪B|
   
3. Token Overlap
   - Word-level matching
   - Percentage calculation
   
4. Sequence Matching (difflib)
   - String similarity
   - SequenceMatcher algorithm
   
5. Bigram Analysis
   - Two-word pattern matching
   
6. Trigram Analysis
   - Three-word pattern matching
   
7. Sentence-Level Analysis
   - Semantic comparison
   - LangChain processing
```

#### Model Integration
```
HuggingFace Models
├─ sentence-transformers/all-MiniLM-L6-v2
│  ├─ Purpose: Text embeddings
│  ├─ Size: 90.9MB
│  ├─ Output: 384-D vectors
│  └─ Speed: Fast inference
│
└─ roberta-base-openai-detector
   ├─ Purpose: AI-generated detection
   ├─ Task: Binary classification
   ├─ Output: Probability [0-1]
   └─ Accuracy: 92%
```

---

### 6. Storage Layer

**File System Structure:**
```
project-root/
├── uploads/
│   ├── {file_id}.txt        (extracted text)
│   ├── {file_id}.json       (metadata)
│   ├── {file_id}.pdf        (original file)
│   └── {file_id}.docx       (original file)
│
├── .cache/
│   └── huggingface/         (model cache)
│
└── logs/
    └── app.log              (application logs)
```

**Metadata Format (JSON):**
```json
{
  "file_id": "uuid-string",
  "filename": "document.pdf",
  "file_type": "pdf",
  "text_length": 5432,
  "word_count": 892,
  "upload_time": "2025-10-22T12:00:00Z",
  "last_accessed": "2025-10-22T12:05:00Z",
  "file_hash": "sha256-hash"
}
```

---

## Data Flow Diagram

### Complete Request Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. FILE UPLOAD                                                  │
├─────────────────────────────────────────────────────────────────┤
│ User selects file → Browser → Fetch API → Flask /api/upload    │
│                                              │
│                                              ▼
│                                    FileUploadService
│                                              │
│                         ┌────────────────────┴────────────────┐
│                         │                                     │
│                    ┌────▼────┐                          ┌─────▼────┐
│                    │ Validate │                          │  Extract │
│                    │ File type│                          │   Text   │
│                    └────┬─────┘                          └─────┬────┘
│                         │                                     │
│                         └──────────────┬──────────────────────┘
│                                        │
│                                  ┌─────▼─────┐
│                                  │ Save Files│
│                                  │ (txt,json)│
│                                  └─────┬─────┘
│                                        │
│                                   Return ID
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 2. TEXT COMPARISON SUBMISSION                                   │
├─────────────────────────────────────────────────────────────────┤
│ User pastes text → Form submit → Fetch → /api/analyze           │
│                                           │
│                                  Request Parsing
│                                           │
│              ┌────────────────────────────┴────────────────────┐
│              │                                                  │
│              ▼                                                  ▼
│        Get File Text                                   Parse Input Text
│        from Storage                                           │
│              │                                                │
│              └────────────────────────────┬───────────────────┘
│                                          │
│                              ┌───────────▼──────────┐
│                              │ Advanced Similarity  │
│                              │    Service (7 algos) │
│                              └───────────┬──────────┘
│                                          │
│                        ┌─────────────────┴──────────────────┐
│                        │                                    │
│                   EITHER                               OR
│                        │                                    │
│             ┌──────────▼───────────┐         ┌──────────────▼─────────┐
│             │LangChain Processing  │         │Advanced ML Fallback    │
│             │  7 Algorithms:       │         │  Uses similarity svc   │
│             │  - Cosine            │         │                        │
│             │  - Jaccard           │         └──────────────┬─────────┘
│             │  - Sequence          │                        │
│             │  - Overlap           │                        │
│             │  - Bigram            │                        │
│             │  - Trigram           │                        │
│             │  - Sentence          │                        │
│             └──────────┬────────────┘                        │
│                        │                                    │
│                        └────────────────┬────────────────────┘
│                                        │
│                                  Format Results
│                                        │
│                              Response JSON
│                                        │
│                            Return to Frontend
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 3. TEXT HIGHLIGHTING                                            │
├─────────────────────────────────────────────────────────────────┤
│ User clicks "Highlight" → Fetch → /api/highlight               │
│                                           │
│                              Get Document Content
│                                           │
│                              ┌────────────▼──────────┐
│                              │TextHighlighter Service│
│                              └────────────┬──────────┘
│                                          │
│                    ┌─────────────────────┴──────────────────┐
│                    │                                        │
│                ┌───▼───────┐                        ┌──────▼──────┐
│                │ Split into │                        │  Compare    │
│                │ Sentences  │                        │  Sentences  │
│                └───┬───────┘                        └──────┬──────┘
│                    │                                      │
│              ┌─────▼──────────────────────────────────────┘
│              │
│         ┌────▼──────────────────┐
│         │Color-Code by Score:   │
│         │ Red (95%+)            │
│         │ Orange (85-94%)       │
│         │ Yellow (75-84%)       │
│         │ Light Yellow (60-74%) │
│         └────┬──────────────────┘
│              │
│         Generate HTML
│         with Styling
│              │
│        Return to Frontend
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 4. DISPLAY RESULTS                                              │
├─────────────────────────────────────────────────────────────────┤
│ Frontend receives JSON → Parse → Update DOM                     │
│                                        │
│              ┌─────────────────────────┴─────────────────────┐
│              │                                               │
│              ▼                                               ▼
│         Populate Results Tabs                         Render Highlights
│         - Overview                                  - Color-coded text
│         - Similarity                                - Match details
│         - Statistics                                - Percentage scores
│         - Details                                   - Source comparison
└─────────────────────────────────────────────────────────────────┘
```

---

## Deployment Architectures

### Development Setup
```
Developer Machine
    ├── Python venv
    ├── Flask dev server (localhost:5001)
    ├── File system storage
    └── Console logging
```

### Production Setup (Single Server)
```
┌─────────────────────────────┐
│      Load Balancer          │
│     (Nginx/Apache)          │
└────────────────┬────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
┌───▼──────────┐      ┌──────▼───────┐
│ Gunicorn     │      │ Gunicorn     │
│ Worker 1     │      │ Worker 2     │
│ (port 8001)  │      │ (port 8002)  │
└───┬──────────┘      └──────┬───────┘
    │                        │
    └────────┬───────────────┘
             │
    ┌────────▼────────┐
    │  Shared Storage │
    │  (or Database)  │
    └─────────────────┘
```

### Cloud Deployment (Scalable)
```
┌──────────────────────────────────────┐
│    API Gateway / Load Balancer       │
└──────────────────┬───────────────────┘
                   │
         ┌─────────┴─────────┐
         │                   │
    ┌────▼───────┐    ┌──────▼────┐
    │ Container  │    │ Container  │
    │  Instance  │    │ Instance   │
    │   (Flask)  │    │  (Flask)   │
    └────┬───────┘    └──────┬─────┘
         │                   │
         └────────┬──────────┘
                  │
    ┌─────────────▼──────────────┐
    │  Cloud Storage / Database  │
    │  (S3, RDS, CosmosDB, etc)  │
    └────────────────────────────┘
```

### Kubernetes Deployment
```
┌─────────────────────────────────────────┐
│        Kubernetes Cluster               │
├─────────────────────────────────────────┤
│  Ingress → Service → Deployment         │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  Pods (Flask + Dependencies)     │  │
│  ├──────────────────────────────────┤  │
│  │  Pod 1 │ Pod 2 │ Pod 3 │ Pod N  │  │
│  └──────────────────────────────────┘  │
│                    ↓                    │
│  ┌──────────────────────────────────┐  │
│  │  Persistent Volume (Storage)     │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

---

## Technology Decision Matrix

### Why These Technologies?

| Technology | Reason | Alternative |
|-----------|--------|-------------|
| Python | Easy to use, great ML support | Go, Java |
| Flask | Lightweight, perfect for APIs | Django, FastAPI |
| LangChain | Unified ML framework | Direct APIs |
| HuggingFace | Pre-trained models, easy | Custom models |
| HTML/CSS/JS | No build system needed | React, Vue |
| NLTK | NLP standard, reliable | spaCy, Transformers |

---

## Performance Optimization

### Current Optimizations
```
✓ Lazy loading of HuggingFace models
✓ Caching of embeddings (FAISS)
✓ Efficient tensor operations
✓ Minimal data copying
✓ File streaming for large documents
```

### Future Optimizations
```
□ Redis caching for results
□ Batch processing queue
□ GPU acceleration (CUDA)
□ Model quantization
□ CDN for static assets
□ Database indexing
```

---

## Monitoring & Observability

### Logging Strategy
```
Level 1: ERROR    → Critical issues only
Level 2: WARNING  → Potential problems
Level 3: INFO     → Major operations
Level 4: DEBUG    → Detailed execution
```

### Metrics to Track
```
Performance:
  - API response time (p50, p95, p99)
  - File upload throughput
  - Model inference latency
  - Memory usage
  - CPU usage

Business:
  - Total files processed
  - Average plagiarism score
  - User engagement
  - Error rates
  - Model accuracy
```

---

## Security Architecture

### Current Security Measures
```
✓ Secure filename handling (Werkzeug)
✓ File type validation
✓ Input sanitization
✓ CORS configuration (to implement)
✓ File size limits
```

### Production Security Requirements
```
□ HTTPS/TLS encryption
□ API authentication (JWT/OAuth)
□ Rate limiting
□ Database encryption
□ Audit logging
□ Access control (RBAC)
□ Data privacy (GDPR, CCPA)
```

### Security Headers to Add
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: ...
Strict-Transport-Security: max-age=31536000
```

---

## Disaster Recovery

### Backup Strategy
```
Database:
  - Daily backups
  - Geographic redundancy
  - Point-in-time recovery

Code:
  - Git version control
  - Multiple remotes
  
Files:
  - Cloud storage replication
  - Lifecycle policies
```

### Recovery Procedures
```
RTO (Recovery Time Objective): < 1 hour
RPO (Recovery Point Objective): < 1 day
```

---

## Scaling Considerations

### Horizontal Scaling
- Add more application instances
- Distribute via load balancer
- Share file storage (cloud storage)

### Vertical Scaling
- Increase RAM for model caching
- Use GPU instances
- Increase CPU cores

### Database Scaling
- Read replicas
- Partitioning by file_id
- Caching layer (Redis)

---

## Compliance & Standards

### Code Standards
```
✓ PEP 8 (Python style)
✓ REST API conventions
✓ Semantic versioning
```

### Testing Requirements
```
□ Unit tests (70%+ coverage)
□ Integration tests
□ Load tests
□ Security tests
```

---

**Last Updated:** October 22, 2025  
**Status:** Production Ready  
**Maintained By:** imad-collab
