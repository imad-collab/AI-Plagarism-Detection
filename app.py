from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import logging
from werkzeug.utils import secure_filename
from src.services.fileUploadService import FileUploadService
from src.services.similarityService import SimilarityService
from src.services.textAnalysisService import TextAnalysisService

app = Flask(__name__, template_folder='templates', static_folder='public')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize services
file_upload_service = FileUploadService(app.config['UPLOAD_FOLDER'])
similarity_service = SimilarityService()
text_analysis_service = TextAnalysisService()

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Plagiarism Detector API is running',
        'version': '1.0.0'
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Upload and process file
        result = file_upload_service.save_file(file)
        
        if result['success']:
            logger.info(f"File uploaded successfully: {result['file_id']}")
            return jsonify({
                'success': True,
                'file_id': result['file_id'],
                'filename': result['filename'],
                'text_length': len(result['text']),
                'word_count': len(result['text'].split())
            })
        else:
            return jsonify({'success': False, 'error': result['error']}), 400
            
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_document():
    """Analyze document for plagiarism"""
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        comparison_text = data.get('comparison_text', '')
        
        if not file_id:
            return jsonify({'success': False, 'error': 'File ID required'}), 400
        
        # Get uploaded file data
        file_data = file_upload_service.get_file_data(file_id)
        if not file_data:
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        document_text = file_data['text']
        
        # Perform similarity analysis
        similarity_results = similarity_service.calculate_similarity(
            document_text, 
            comparison_text if comparison_text else None
        )
        
        # Perform text analysis
        text_stats = text_analysis_service.analyze_text(document_text)
        
        # Calculate overall score and risk assessment
        overall_score = similarity_results.get('overall_similarity', 0)
        risk_level = 'low'
        if overall_score > 0.7:
            risk_level = 'high'
        elif overall_score > 0.4:
            risk_level = 'medium'
        
        analysis_result = {
            'overall_score': overall_score,
            'risk_level': risk_level,
            'similarity_results': similarity_results.get('matches', []),
            'document_stats': text_stats,
            'analysis_timestamp': text_stats.get('timestamp'),
            'file_id': file_id
        }
        
        logger.info(f"Analysis completed for file: {file_id}")
        return jsonify({
            'success': True,
            'analysis': analysis_result
        })
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/documents/<file_id>')
def get_document(file_id):
    """Get document details"""
    try:
        file_data = file_upload_service.get_file_data(file_id)
        if not file_data:
            return jsonify({'success': False, 'error': 'Document not found'}), 404
        
        return jsonify({
            'success': True,
            'document': {
                'file_id': file_id,
                'filename': file_data['filename'],
                'text_length': len(file_data['text']),
                'upload_time': file_data.get('upload_time'),
                'file_type': file_data.get('file_type')
            }
        })
        
    except Exception as e:
        logger.error(f"Get document error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB.'
    }), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("Starting AI Plagiarism Detector...")
    print("Access the application at: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)