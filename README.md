# 🔍 AI Plagiarism Detection System

A comprehensive web-based plagiarism detection system that uses advanced machine learning and natural language processing techniques to identify text similarity and potential plagiarism.

## ✨ Features

- **Multi-format Document Support**: PDF, DOC, DOCX, TXT, RTF files
- **Advanced Similarity Detection**: Multiple algorithms including cosine similarity, Jaccard similarity, and Levenshtein distance
- **Web-based Interface**: Beautiful, responsive UI with drag-and-drop file upload
- **Real-time Analysis**: Fast processing with detailed results display
- **Comprehensive Statistics**: Document analysis with readability metrics and linguistic features
- **RESTful API**: Complete API endpoints for integration with other systems

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

#### Analyze Document
```bash
POST /api/analyze
Content-Type: application/json

{
  "file_id": "uploaded_file_id",
  "comparison_text": "optional comparison text"
}
```

#### Get Document Details
```bash
GET /api/documents/{file_id}
```

## 🔧 Technology Stack

### Backend
- **Flask**: Web framework
- **NLTK**: Natural language processing
- **scikit-learn**: Machine learning algorithms
- **NumPy & Pandas**: Data processing
- **TextDistance**: String similarity algorithms
- **PyPDF2**: PDF text extraction
- **python-docx**: Word document processing

### Frontend
- **HTML5**: Modern markup
- **CSS3**: Responsive design with gradients and animations
- **JavaScript**: Interactive functionality and API integration

### Algorithms
- **Cosine Similarity**: Vector-based text comparison
- **Jaccard Similarity**: Set-based similarity measurement
- **Levenshtein Distance**: Edit distance calculation
- **TF-IDF Vectorization**: Term frequency analysis

## 📁 Project Structure

```
plagiarism-detector/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── sample_document.txt            # Test document
├── templates/
│   └── index.html                 # Web interface
├── src/
│   ├── services/
│   │   ├── fileUploadService.py   # File handling and text extraction
│   │   ├── similarityService.py   # Plagiarism detection algorithms
│   │   └── textAnalysisService.py # Text analysis and statistics
│   └── utils/
│       ├── textProcessor.py       # Text preprocessing utilities
│       └── validators.py          # File and content validation
├── uploads/                       # Uploaded files storage
└── tests/                        # Test files
    ├── unit/
    └── integration/
```

## 🔬 How It Works

1. **Document Upload**: Files are securely uploaded and validated
2. **Text Extraction**: Text is extracted from various file formats
3. **Preprocessing**: Text is cleaned, tokenized, and normalized
4. **Similarity Analysis**: Multiple algorithms calculate similarity scores
5. **Statistical Analysis**: Document features and readability metrics are computed
6. **Results Compilation**: All analyses are combined into a comprehensive report

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