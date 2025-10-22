# 🔍 AI Plagiarism Detection System

A comprehensive web-based plagiarism detection system powered by **LangChain** and advanced machine learning. Uses semantic embeddings and multi-algorithm ensemble for highly accurate plagiarism detection.

---

## 🔗 Quick Links

### 📌 **Access the Project**
- **GitHub Repository:** https://github.com/imad-collab/AI-Plagarism-Detection
- **Live Application:** Run locally on `http://127.0.0.1:5001`
- **Issue Tracker:** https://github.com/imad-collab/AI-Plagarism-Detection/issues

### 📖 **Documentation**
- [📄 Feature Overview](./HIGHLIGHTING_FEATURE.md)
- [🧪 Testing Guide](./HIGHLIGHTING_TEST_GUIDE.md)
- [⚡ Quick Start](./TEXT_HIGHLIGHTING_QUICKSTART.md)
- [✅ Implementation Summary](./IMPLEMENTATION_COMPLETE.md)

### 🎯 **Share This Project**

#### GitHub Badge
```markdown
[![AI Plagiarism Detector](https://img.shields.io/badge/AI-Plagiarism%20Detector-brightgreen)](https://github.com/imad-collab/AI-Plagarism-Detection)
```

#### Simple Link for PDF
```
https://github.com/imad-collab/AI-Plagarism-Detection
```

#### QR Code Ready Link
The repository URL can be converted to a QR code for easy mobile access:
```
https://github.com/imad-collab/AI-Plagarism-Detection
```

---

## ✨ Features

- **🤖 LangChain Integration**: AI-powered semantic analysis using HuggingFace embeddings
- **Multi-format Document Support**: PDF, DOC, DOCX, TXT, RTF files
- **🧠 Advanced Similarity Detection**: 7+ algorithms including:
  - Semantic embeddings (LangChain)
  - TF-IDF similarity
  - Cosine similarity
  - Jaccard similarity
  - Sequence matching
  - Token overlap
  - Sentence-level semantic analysis
- **Web-based Interface**: Beautiful, responsive UI with drag-and-drop file upload
- **Real-time Analysis**: Fast processing with detailed results display
- **Comprehensive Statistics**: Document analysis with readability metrics and linguistic features
- **RESTful API**: Complete API endpoints for integration with other systems
- **Ensemble Approach**: Combines LangChain semantic analysis with traditional ML for maximum accuracy

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/imad-collab/AI-Plagarism-Detection.git
   cd AI-Plagarism-Detection
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   
   # On macOS/Linux:
   source .venv/bin/activate
   
   # On Windows:
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and go to: `http://localhost:5001`

## 🎯 Usage

### Web Interface

1. **Upload Document**: Drag and drop or click to select a document (PDF, DOC, DOCX, TXT)
2. **Optional Comparison**: Enter text in the comparison field to check against specific content
3. **Analyze**: Click "Analyze for Plagiarism" to start the detection process
4. **View Results**: See detailed results in organized tabs:
   - **Overview**: Overall similarity score and risk level
   - **Similarity**: Detailed match results
   - **Statistics**: Document statistics and metrics
   - **Details**: Complete analysis data

### API Endpoints

#### Health Check
```bash
GET /api/health
```

#### Upload Document
```bash
POST /api/upload
Content-Type: multipart/form-data

# Form data:
# file: [document file]
```

#### Analyze Document (with LangChain)
```bash
POST /api/analyze
Content-Type: application/json

{
  "file_id": "uploaded_file_id",
  "comparison_text": "optional comparison text",
  "use_langchain": true  # Enable LangChain semantic analysis
}
```

#### LangChain Semantic Analysis
```bash
POST /api/langchain-analysis
Content-Type: application/json

{
  "document_text": "Your document text",
  "comparison_text": "Text to compare against"
}
```

#### Get Document Details
```bash
GET /api/documents/{file_id}
```

## 🔧 Technology Stack

### Backend
- **LangChain**: Agentic AI framework with semantic embeddings
- **Flask**: Web framework
- **HuggingFace Embeddings**: Semantic text understanding (all-MiniLM-L6-v2)
- **NLTK**: Natural language processing
- **scikit-learn**: Machine learning algorithms
- **Sentence Transformers**: Advanced text embeddings
- **NumPy & Pandas**: Data processing
- **TextDistance**: String similarity algorithms
## 🤖 LangChain Integration

The system now integrates **LangChain** for advanced semantic analysis and agentic capabilities.

### LangChain-Powered Features

1. **Semantic Embeddings**: HuggingFace embeddings for deep semantic understanding
2. **Text Chunking**: Intelligent document segmentation for analysis
3. **Vector Similarity**: Advanced semantic similarity calculations
4. **Multi-level Analysis**: Sentence, chunk, and document-level analysis
5. **Ensemble Scoring**: Combines LangChain semantic analysis (65%) with traditional ML (35%)

### LangChain Algorithms (7 Methods)

- **Semantic Similarity** (20%): Deep semantic understanding via embeddings
- **Chunk-Level Analysis** (15%): TF-IDF similarity at chunk boundaries
- **Semantic Chunks** (15%): Semantic matching of text chunks
- **Sentence Semantic** (15%): LangChain sentence-level semantics
- **TF-IDF Similarity** (12%): Traditional n-gram matching
- **Sequence Matching** (12%): Difflib-based sequence comparison
- **Token Overlap** (11%): Jaccard index for word overlap

### Example Usage

```python
from src.services.langchainPlagiarismService import LangChainPlagiarismService

service = LangChainPlagiarismService()
results = service.calculate_plagiarism_score(
    document_text="Your document...",
    comparison_text="Text to compare..."
)

print(f"Overall Score: {results['overall']}")
print(f"Semantic Similarity: {results['semantic']}")
print(f"Methodology: {results['methodology']}")
```

**For detailed LangChain documentation, see: [LANGCHAIN_INTEGRATION.md](LANGCHAIN_INTEGRATION.md)**

## 📁 Project Structure

```
plagiarism-detector/
├── app.py                               # Main Flask application
├── requirements.txt                     # Python dependencies
├── LANGCHAIN_INTEGRATION.md            # LangChain documentation
├── sample_document.txt                 # Test document
├── templates/
│   └── index.html                      # Web interface
├── src/
│   ├── services/
│   │   ├── langchainPlagiarismService.py    # NEW: LangChain semantic analysis
│   │   ├── advancedSimilarityService.py     # 9-algorithm ensemble
│   │   ├── fileUploadService.py             # File handling and text extraction
│   │   ├── similarityService.py             # Original similarity algorithms
│   │   └── textAnalysisService.py           # Text analysis and statistics
│   └── utils/
│       ├── textProcessor.py            # Text preprocessing utilities
│       └── validators.py               # File and content validation
├── uploads/                            # Uploaded files storage
└── tests/                              # Test files
    ├── unit/
    └── integration/
```

## 🔬 How It Works

1. **Document Upload**: Files are securely uploaded and validated
2. **Text Extraction**: Text is extracted from various file formats
3. **Preprocessing**: Text is cleaned, tokenized, and normalized
4. **LangChain Analysis**:
   - Text is split into chunks using RecursiveCharacterTextSplitter
   - HuggingFace embeddings generate semantic representations
   - Multiple similarity metrics are calculated
5. **Ensemble Scoring**: Results from LangChain and traditional ML are combined
6. **Statistical Analysis**: Document features and readability metrics are computed
7. **Results Compilation**: All analyses are combined into a comprehensive report

## 🎨 Features in Detail

### Multi-Algorithm Detection
- **Cosine Similarity**: Measures angle between document vectors
- **Jaccard Index**: Compares set overlap of words/n-grams
- **Levenshtein Distance**: Character-level edit distance
- **Weighted Scoring**: Combines algorithms for comprehensive analysis

### Document Processing
- **PDF**: Text extraction with PyPDF2
- **Word Documents**: DOCX processing with python-docx
- **Plain Text**: Direct text file reading
- **Validation**: File type, size, and content validation

### Text Analysis
- **Readability Metrics**: Flesch-Kincaid, Gunning Fog Index
- **Linguistic Features**: POS tagging, vocabulary richness
- **Statistical Measures**: Word count, sentence count, lexical diversity

## 🛡️ Security Features

- **File Validation**: MIME type checking and extension validation
- **Size Limits**: Maximum file size enforcement (16MB)
- **Secure Filenames**: Filename sanitization
- **Content Scanning**: Suspicious pattern detection

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production
For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

## 📊 Performance

- **File Processing**: Handles documents up to 16MB
- **Speed**: Real-time analysis for most documents
- **Accuracy**: Multi-algorithm approach for reliable detection
- **Scalability**: Stateless design for horizontal scaling

## 🔍 Testing

Try the system with the included sample document:
```bash
# Use sample_document.txt for testing
# Upload through web interface or API
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/imad-collab/AI-Plagarism-Detection/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## 🎉 Acknowledgments

- Built with modern web technologies
- Uses state-of-the-art NLP algorithms
- Inspired by academic integrity tools
- Community-driven development

---

**🚀 Ready to detect plagiarism? Start by uploading a document and see the AI in action!**