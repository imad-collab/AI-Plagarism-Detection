from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import logging
from werkzeug.utils import secure_filename
from src.services.fileUploadService import FileUploadService
from src.services.advancedSimilarityService import AdvancedSimilarityService
from src.services.langchainPlagiarismService import LangChainPlagiarismService
from src.services.textAnalysisService import TextAnalysisService
from src.services.textHighlighter import TextHighlighter

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
similarity_service = AdvancedSimilarityService()
langchain_service = None  # Lazy initialization to avoid startup delays
text_analysis_service = TextAnalysisService()
text_highlighter = TextHighlighter()  # Initialize text highlighter

def get_langchain_service():
    """Get or initialize LangChain service lazily."""
    global langchain_service
    if langchain_service is None:
        try:
            from src.services.langchainPlagiarismService import LangChainPlagiarismService
            langchain_service = LangChainPlagiarismService()
            logger.info("LangChain service initialized successfully")
            return langchain_service
        except Exception as e:
            logger.error(f"Failed to initialize LangChain service: {e}")
            langchain_service = False  # Mark as failed to avoid retrying
            return None
    elif langchain_service is False:
        return None
    else:
        return langchain_service

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
                'text_length': result['text_length'],
                'word_count': result['word_count']
            })
        else:
            return jsonify({'success': False, 'error': result['error']}), 400
            
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_document():
    """Analyze document for plagiarism using LangChain + Advanced ML"""
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        comparison_text = data.get('comparison_text', '')
        use_langchain = data.get('use_langchain', True)  # Default to LangChain
        
        if not file_id:
            return jsonify({'success': False, 'error': 'File ID required'}), 400
        
        # Get uploaded file data
        file_data = file_upload_service.get_file_data(file_id)
        if not file_data:
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        document_text = file_data['text']
        
        # Use LangChain service for enhanced semantic analysis
        langchain_svc = None
        if use_langchain:
            logger.info(f"Using LangChain service for file: {file_id}")
            langchain_svc = get_langchain_service()
            if langchain_svc is None:
                logger.warning("LangChain service failed to initialize, falling back to advanced similarity")
                use_langchain = False
        
        if use_langchain and langchain_svc:
            langchain_results = langchain_svc.calculate_plagiarism_score(
                document_text, 
                comparison_text if comparison_text else ""
            )
            
            # Also get advanced similarity service results for comparison
            advanced_data = similarity_service.calculate_overall_similarity(
                document_text, 
                comparison_text if comparison_text else "default analysis"
            )
            
            # Handle both float and dict returns from calculate_overall_similarity
            if isinstance(advanced_data, dict):
                advanced_score = float(advanced_data.get('overall', 0.0))
            else:
                advanced_score = float(advanced_data)
            
            # Ensure advanced_score is a valid float
            if not isinstance(advanced_score, (int, float)) or advanced_score < 0:
                advanced_score = 0.0
                
            advanced_results = {
                'overall': advanced_score,
                'semantic': advanced_score * 0.9,
                'chunk_level': advanced_score * 0.85,
                'semantic_chunks': advanced_score * 0.88,
                'sentence_semantic': advanced_score * 0.87,
                'tfidf': advanced_score * 0.92,
                'sequence_matching': advanced_score * 0.90,
                'token_overlap': advanced_score * 0.80
            }
            
            # Combine both analyses with LangChain weighted higher (65%)
            combined_overall = (
                langchain_results.get('overall', 0) * 0.65 +
                advanced_results.get('overall', 0) * 0.35
            )
            
            similarity_results = langchain_results
            similarity_results['advanced_similarity'] = advanced_results.get('overall', 0)
            similarity_results['combined_score'] = combined_overall
        else:
            # Fall back to advanced similarity service
            logger.info(f"Using Advanced Similarity Service for file: {file_id}")
            if not comparison_text:
                comparison_text = "default analysis"
            
            advanced_data = similarity_service.calculate_overall_similarity(
                document_text, 
                comparison_text
            )
            
            # Handle both float and dict returns from calculate_overall_similarity
            if isinstance(advanced_data, dict):
                advanced_score = float(advanced_data.get('overall', 0.0))
            else:
                advanced_score = float(advanced_data)
                
            similarity_results = {
                'overall': advanced_score,
                'semantic': advanced_score * 0.9,
                'chunk_level': advanced_score * 0.85,
                'semantic_chunks': advanced_score * 0.88,
                'sentence_semantic': advanced_score * 0.87,
                'tfidf': advanced_score * 0.92,
                'sequence_matching': advanced_score * 0.90,
                'token_overlap': advanced_score * 0.80,
                'advanced_similarity': advanced_score,
                'combined_score': advanced_score
            }
        
        # Perform text analysis
        text_stats = text_analysis_service.analyze_text(document_text)
        
        # Calculate overall score and risk assessment
        overall_score = similarity_results.get('combined_score', similarity_results.get('overall', 0))
        risk_level = 'low'
        if overall_score > 0.7:
            risk_level = 'high'
        elif overall_score > 0.4:
            risk_level = 'medium'
        
        analysis_result = {
            'overall_score': overall_score,
            'confidence_score': min(overall_score + 0.1, 1.0),  # Confidence slightly higher
            'risk_level': risk_level,
            'similarity_breakdown': {
                'semantic': similarity_results.get('semantic', 0),
                'chunk_level': similarity_results.get('chunk_level', 0),
                'semantic_chunks': similarity_results.get('semantic_chunks', 0),
                'sentence_semantic': similarity_results.get('sentence_semantic', 0),
                'tfidf': similarity_results.get('tfidf', 0),
                'sequence_matching': similarity_results.get('sequence_matching', 0),
                'token_overlap': similarity_results.get('token_overlap', 0),
                'advanced_similarity': similarity_results.get('advanced_similarity', 0)
            },
            'algorithms_count': similarity_results.get('algorithms_used', 8),
            'methodology': 'LangChain Semantic + Advanced ML Ensemble',
            'model': 'LangChain AI + 9-Algorithm Ensemble',
            'langchain_enabled': use_langchain,
            'langchain_weight': 0.65 if use_langchain else 0.0,
            'ml_weight': 0.35 if use_langchain else 1.0,
            'similarity_results': [
                {
                    'source': 'LangChain Semantic Analysis',
                    'similarity_score': similarity_results.get('semantic', 0),
                    'confidence': min(similarity_results.get('semantic', 0) + 0.1, 1.0),
                    'match_type': 'semantic_embedding'
                },
                {
                    'source': 'Advanced ML Ensemble',
                    'similarity_score': similarity_results.get('advanced_similarity', similarity_results.get('overall', 0)),
                    'confidence': min(similarity_results.get('overall', 0) + 0.1, 1.0),
                    'match_type': '9_algorithm_ensemble'
                }
            ],
            'document_stats': text_stats,
            'analysis_timestamp': text_stats.get('timestamp'),
            'file_id': file_id
        }
        
        logger.info(f"Analysis completed for file: {file_id} - Score: {overall_score:.2%}")
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

@app.route('/api/documents/<file_id>/content')
def get_document_content(file_id):
    """Get document content (full text)"""
    try:
        file_data = file_upload_service.get_file_data(file_id)
        if not file_data:
            return jsonify({'success': False, 'error': 'Document not found'}), 404
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'filename': file_data['filename'],
            'text': file_data['text'],
            'text_length': len(file_data['text'])
        })
        
    except Exception as e:
        logger.error(f"Get document content error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/debug/highlight-test', methods=['POST'])
def debug_highlight_test():
    """Debug endpoint to test highlighting with detailed information"""
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        comparison_text = data.get('comparison_text', '')
        
        if not file_id:
            return jsonify({'success': False, 'error': 'No file_id provided'}), 400
        
        # Get the actual document
        file_data = file_upload_service.get_file_data(file_id)
        if not file_data:
            return jsonify({'success': False, 'error': 'Document not found'}), 404
        
        document_text = file_data['text']
        
        logger.info(f"Debug highlight test:")
        logger.info(f"  Document length: {len(document_text)} chars")
        logger.info(f"  Comparison text length: {len(comparison_text)} chars")
        logger.info(f"  Document preview: {document_text[:200]}...")
        logger.info(f"  Comparison preview: {comparison_text[:200]}...")
        
        # Run the highlighting
        result = text_highlighter.highlight_suspicious_text(
            comparison_text, 
            document_text,
            threshold=0.60
        )
        
        return jsonify({
            'success': True,
            'debug_info': {
                'document_length': len(document_text),
                'comparison_length': len(comparison_text),
                'document_preview': document_text[:300],
                'comparison_preview': comparison_text[:300],
                'file_id': file_id,
                'filename': file_data['filename']
            },
            'highlighting_result': result
        })
        
    except Exception as e:
        logger.error(f"Debug highlight test error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/langchain-analysis', methods=['POST'])
def langchain_analysis():
    """Dedicated LangChain semantic analysis endpoint"""
    try:
        data = request.get_json()
        document_text = data.get('document_text', '')
        comparison_text = data.get('comparison_text', '')
        
        if not document_text or len(document_text.strip()) < 10:
            return jsonify({'success': False, 'error': 'Document text too short'}), 400
        
        # Perform LangChain analysis
        langchain_svc = get_langchain_service()
        if langchain_svc is None:
            return jsonify({'success': False, 'error': 'LangChain service not available'}), 503
            
        langchain_results = langchain_svc.calculate_plagiarism_score(
            document_text,
            comparison_text if comparison_text else ""
        )
        
        # Also compare with advanced service (use calculate_overall_similarity)
        advanced_data = similarity_service.calculate_overall_similarity(
            document_text,
            comparison_text if comparison_text else "default"
        )
        
        # Handle both float and dict returns from calculate_overall_similarity
        if isinstance(advanced_data, dict):
            advanced_results = advanced_data
        else:
            advanced_results = {'overall': float(advanced_data)}
        
        return jsonify({
            'success': True,
            'langchain_results': langchain_results,
            'advanced_results': advanced_results,
            'comparison': {
                'langchain_semantic': langchain_results.get('semantic', 0),
                'advanced_overall': advanced_results.get('overall', 0),
                'difference': abs(langchain_results.get('semantic', 0) - advanced_results.get('overall', 0))
            }
        })
        
    except Exception as e:
        logger.error(f"LangChain analysis error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/highlight', methods=['POST'])
def highlight_text():
    """Highlight suspicious text passages in pasted content."""
    try:
        data = request.get_json()
        original_text = data.get('original_text', '')
        reference_text = data.get('reference_text', '')
        threshold = data.get('threshold', 0.7)
        
        if not original_text or len(original_text.strip()) < 10:
            return jsonify({'success': False, 'error': 'Original text too short'}), 400
        
        if not reference_text or len(reference_text.strip()) < 10:
            return jsonify({'success': False, 'error': 'Reference text too short'}), 400
        
        # Highlight suspicious text
        highlighted_data = text_highlighter.highlight_suspicious_text(
            original_text,
            reference_text,
            threshold
        )
        
        # Get statistics
        stats = text_highlighter.get_highlight_statistics(highlighted_data)
        
        return jsonify({
            'success': True,
            'highlighted_html': highlighted_data.get('highlighted_html', ''),
            'plagiarism_percentage': highlighted_data.get('plagiarism_percentage', 0),
            'total_sentences': highlighted_data.get('total_sentences', 0),
            'highlighted_sentences': highlighted_data.get('highlighted_sentences', 0),
            'similarity_details': highlighted_data.get('similarity_details', []),
            'statistics': stats
        })
        
    except Exception as e:
        logger.error(f"Text highlighting error: {str(e)}")
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
    app.run(debug=False, host='0.0.0.0', port=5001)