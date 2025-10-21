from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import sys
import json
from datetime import datetime

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import our custom modules
from services.similarityService import SimilarityService
from services.fileUploadService import FileUploadService
from services.textAnalysisService import TextAnalysisService
from utils.textProcessor import TextProcessor
from utils.validators import DocumentValidator

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize services
similarity_service = SimilarityService()
file_service = FileUploadService()
text_analysis_service = TextAnalysisService()
text_processor = TextProcessor()
validator = DocumentValidator()

@app.route('/')
def index():
    """Serve the main application page."""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/upload', methods=['POST'])
def upload_document():
    """Handle document upload."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file
        if not validator.validate_file(file):
            return jsonify({'error': 'Invalid file type or size'}), 400
        
        # Save and process file
        result = file_service.save_file(file, app.config['UPLOAD_FOLDER'])
        
        if result['success']:
            return jsonify({
                'success': True,
                'file_id': result['file_id'],
                'filename': result['filename'],
                'message': 'File uploaded successfully'
            })
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_plagiarism():
    """Analyze document for plagiarism."""
    try:
        data = request.get_json()
        
        if not data or 'file_id' not in data:
            return jsonify({'error': 'No file ID provided'}), 400
        
        file_id = data['file_id']
        comparison_text = data.get('comparison_text', '')
        
        # Get the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}.txt")
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Read the document content
        with open(file_path, 'r', encoding='utf-8') as f:
            document_text = f.read()
        
        # Perform analysis
        analysis_result = text_analysis_service.analyze_text(document_text)
        
        # If comparison text is provided, calculate similarity
        similarity_results = []
        if comparison_text:
            similarity_score = similarity_service.calculate_similarity(
                document_text, comparison_text
            )
            similarity_results.append({
                'source': 'User provided text',
                'similarity_score': similarity_score,
                'match_type': 'exact' if similarity_score > 0.9 else 'partial'
            })
        
        # Web search for potential matches (simplified for demo)
        web_matches = similarity_service.search_web_matches(document_text[:500])
        
        return jsonify({
            'success': True,
            'analysis': {
                'document_stats': analysis_result,
                'similarity_results': similarity_results,
                'web_matches': web_matches,
                'overall_score': max([r['similarity_score'] for r in similarity_results] + [0]),
                'risk_level': _calculate_risk_level(similarity_results)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def _calculate_risk_level(similarity_results):
    """Calculate risk level based on similarity scores."""
    if not similarity_results:
        return 'low'
    
    max_score = max([r['similarity_score'] for r in similarity_results])
    
    if max_score >= 0.8:
        return 'high'
    elif max_score >= 0.5:
        return 'medium'
    else:
        return 'low'

@app.route('/api/documents', methods=['GET'])
def list_documents():
    """List all uploaded documents."""
    try:
        documents = file_service.list_documents(app.config['UPLOAD_FOLDER'])
        return jsonify({
            'success': True,
            'documents': documents
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large'}), 413

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)