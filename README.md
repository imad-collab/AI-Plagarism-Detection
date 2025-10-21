# AI Plagiarism Detection System

A comprehensive web-based plagiarism detection tool that uses advanced natural language processing and machine learning algorithms to analyze documents for similarity and potential plagiarism.

## Features

- **Multi-format Document Support**: Upload PDF, DOC, DOCX, and TXT files
- **Advanced Similarity Detection**: Multiple algorithms including cosine similarity, Jaccard similarity, and Levenshtein distance
- **Text Analysis**: Comprehensive document statistics and linguistic analysis
- **Web Interface**: User-friendly drag-and-drop interface
- **Real-time Analysis**: Instant plagiarism detection and scoring
- **Risk Assessment**: Automatic categorization of plagiarism risk levels

## Technology Stack

- **Backend**: Flask (Python)
- **NLP Libraries**: NLTK, scikit-learn, textdistance
- **Document Processing**: PyPDF2, python-docx
- **Frontend**: HTML5, CSS3, JavaScript
- **File Handling**: Secure upload and processing

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/imad-collab/AI-Plagarism-Detection.git
   cd AI-Plagarism-Detection
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data** (first time only):
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
   ```

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Access the web interface**:
   Open your browser and navigate to `http://localhost:5000`

3. **Upload and analyze documents**:
   - Drag and drop or select a document file
   - Optionally add comparison text
   - Click "Analyze for Plagiarism"
   - View detailed results with similarity scores and statistics

## API Endpoints

### Upload Document
```
POST /api/upload
Content-Type: multipart/form-data

Response:
{
  "success": true,
  "file_id": "unique_file_identifier",
  "filename": "document.pdf",
  "text_length": 1500,
  "word_count": 250
}
```

### Analyze Document
```
POST /api/analyze
Content-Type: application/json

{
  "file_id": "unique_file_identifier",
  "comparison_text": "optional text to compare against"
}

Response:
{
  "success": true,
  "analysis": {
    "overall_score": 0.25,
    "risk_level": "low",
    "similarity_results": [...],
    "document_stats": {...}
  }
}
```

### Health Check
```
GET /api/health

Response:
{
  "status": "healthy",
  "message": "AI Plagiarism Detector API is running",
  "version": "1.0.0"
}
```

## Project Structure

```
plagiarism-detector/
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── README.md                 # Project documentation
├── templates/
│   └── index.html            # Web interface
├── src/
│   ├── services/
│   │   ├── fileUploadService.py      # File upload and processing
│   │   ├── similarityService.py     # Plagiarism detection algorithms
│   │   └── textAnalysisService.py   # Text analysis and statistics
│   └── utils/
│       ├── textProcessor.py         # Text preprocessing utilities
│       └── validators.py            # Input validation
├── uploads/                  # Uploaded files storage
└── tests/                    # Unit and integration tests
```

## Algorithm Details

### Similarity Detection
- **Cosine Similarity**: Measures document similarity using TF-IDF vectors
- **Jaccard Similarity**: Compares document overlap using set operations
- **Levenshtein Distance**: Character-level edit distance calculation
- **Weighted Scoring**: Combines multiple algorithms for accurate results

### Text Analysis
- Document statistics (word count, character count, paragraphs)
- Lexical diversity and vocabulary analysis
- Readability metrics
- Suspicious pattern detection

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation
- Review the API endpoints

## Future Enhancements

- [ ] Database integration for result storage
- [ ] User authentication and session management
- [ ] Batch document processing
- [ ] Advanced reporting and analytics
- [ ] Integration with external plagiarism databases
- [ ] Real-time collaboration features

## Features
- Text input and file upload
- Multiple similarity algorithms
- Real-time analysis
- Detailed reports
- Export functionality

## Setup
```bash
npm install
npm start
```
