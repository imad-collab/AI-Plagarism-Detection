"""
Document Validator utility for validating uploaded files and content.
"""

import os
import mimetypes
import magic
from werkzeug.datastructures import FileStorage

class DocumentValidator:
    """Utility class for validating documents and files."""
    
    def __init__(self):
        """Initialize the document validator."""
        self.allowed_extensions = {
            'txt', 'pdf', 'doc', 'docx', 'rtf'
        }
        
        self.allowed_mime_types = {
            'text/plain',
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/rtf',
            'text/rtf'
        }
        
        self.max_file_size = 16 * 1024 * 1024  # 16MB
        self.min_file_size = 10  # 10 bytes
        self.max_text_length = 1000000  # 1 million characters
        self.min_text_length = 10  # 10 characters
    
    def validate_file(self, file):
        """Validate uploaded file."""
        try:
            if not isinstance(file, FileStorage):
                return False
            
            if not file or not file.filename:
                return False
            
            # Check file extension
            if not self._validate_extension(file.filename):
                return False
            
            # Check file size
            if not self._validate_file_size(file):
                return False
            
            # Check MIME type
            if not self._validate_mime_type(file):
                return False
            
            return True
        
        except Exception as e:
            print(f"Error validating file: {e}")
            return False
    
    def _validate_extension(self, filename):
        """Validate file extension."""
        try:
            if '.' not in filename:
                return False
            
            extension = filename.rsplit('.', 1)[1].lower()
            return extension in self.allowed_extensions
        
        except Exception as e:
            print(f"Error validating extension: {e}")
            return False
    
    def _validate_file_size(self, file):
        """Validate file size."""
        try:
            # Seek to end to get file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)  # Reset to beginning
            
            return self.min_file_size <= file_size <= self.max_file_size
        
        except Exception as e:
            print(f"Error validating file size: {e}")
            return False
    
    def _validate_mime_type(self, file):
        """Validate MIME type."""
        try:
            # Get MIME type from filename
            mime_type, _ = mimetypes.guess_type(file.filename)
            
            if mime_type in self.allowed_mime_types:
                return True
            
            # Additional check using file content (if python-magic is available)
            try:
                file.seek(0)
                file_content = file.read(1024)  # Read first 1KB
                file.seek(0)  # Reset to beginning
                
                detected_mime = magic.from_buffer(file_content, mime=True)
                return detected_mime in self.allowed_mime_types
            
            except (ImportError, Exception):
                # Fall back to extension-based validation if python-magic is not available
                return self._validate_extension(file.filename)
        
        except Exception as e:
            print(f"Error validating MIME type: {e}")
            return False
    
    def validate_text_content(self, text):
        """Validate text content."""
        try:
            if not text or not isinstance(text, str):
                return {
                    'valid': False,
                    'error': 'Invalid text content'
                }
            
            text_length = len(text.strip())
            
            if text_length < self.min_text_length:
                return {
                    'valid': False,
                    'error': f'Text too short (minimum {self.min_text_length} characters)'
                }
            
            if text_length > self.max_text_length:
                return {
                    'valid': False,
                    'error': f'Text too long (maximum {self.max_text_length} characters)'
                }
            
            # Check for suspicious patterns
            suspicion_check = self._check_suspicious_patterns(text)
            
            return {
                'valid': True,
                'length': text_length,
                'suspicion_level': suspicion_check['level'],
                'warnings': suspicion_check['warnings']
            }
        
        except Exception as e:
            return {
                'valid': False,
                'error': f'Error validating text: {str(e)}'
            }
    
    def _check_suspicious_patterns(self, text):
        """Check for suspicious patterns in text."""
        try:
            warnings = []
            suspicion_score = 0
            
            # Check for excessive repetition
            words = text.split()
            if len(words) > 0:
                unique_words = len(set(words))
                repetition_ratio = unique_words / len(words)
                
                if repetition_ratio < 0.3:  # Less than 30% unique words
                    warnings.append("High repetition detected")
                    suspicion_score += 1
            
            # Check for unusual character patterns
            import re
            
            # Excessive special characters
            special_chars = re.findall(r'[^\w\s\.,;:!?\-()"\']', text)
            if len(special_chars) > len(text) * 0.05:  # More than 5% special characters
                warnings.append("Unusual character patterns detected")
                suspicion_score += 1
            
            # Very long words (might indicate encoding issues)
            long_words = re.findall(r'\b\w{30,}\b', text)
            if len(long_words) > 5:
                warnings.append("Unusually long words detected")
                suspicion_score += 1
            
            # Excessive URLs or email addresses
            urls = re.findall(r'https?://[^\s]+', text)
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
            
            if len(urls) > 10:
                warnings.append("Excessive URLs detected")
                suspicion_score += 1
            
            if len(emails) > 5:
                warnings.append("Excessive email addresses detected")
                suspicion_score += 1
            
            # Determine suspicion level
            if suspicion_score >= 3:
                level = 'high'
            elif suspicion_score >= 2:
                level = 'medium'
            elif suspicion_score >= 1:
                level = 'low'
            else:
                level = 'none'
            
            return {
                'level': level,
                'score': suspicion_score,
                'warnings': warnings
            }
        
        except Exception as e:
            return {
                'level': 'unknown',
                'score': 0,
                'warnings': [f"Error checking patterns: {str(e)}"]
            }
    
    def validate_comparison_text(self, text1, text2):
        """Validate two texts for comparison."""
        try:
            # Validate both texts individually
            text1_validation = self.validate_text_content(text1)
            text2_validation = self.validate_text_content(text2)
            
            if not text1_validation['valid']:
                return {
                    'valid': False,
                    'error': f"First text invalid: {text1_validation['error']}"
                }
            
            if not text2_validation['valid']:
                return {
                    'valid': False,
                    'error': f"Second text invalid: {text2_validation['error']}"
                }
            
            # Check if texts are too similar (might be duplicates)
            if text1.strip() == text2.strip():
                return {
                    'valid': False,
                    'error': 'Texts are identical'
                }
            
            # Check minimum difference
            from difflib import SequenceMatcher
            similarity = SequenceMatcher(None, text1, text2).ratio()
            
            if similarity > 0.95:  # More than 95% similar
                return {
                    'valid': True,
                    'warning': 'Texts are very similar',
                    'similarity': similarity
                }
            
            return {
                'valid': True,
                'text1_length': text1_validation['length'],
                'text2_length': text2_validation['length'],
                'similarity': similarity
            }
        
        except Exception as e:
            return {
                'valid': False,
                'error': f'Error validating comparison texts: {str(e)}'
            }
    
    def validate_file_path(self, file_path):
        """Validate file path and existence."""
        try:
            if not file_path or not isinstance(file_path, str):
                return False
            
            # Check if file exists
            if not os.path.exists(file_path):
                return False
            
            # Check if it's a file (not directory)
            if not os.path.isfile(file_path):
                return False
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if not (self.min_file_size <= file_size <= self.max_file_size):
                return False
            
            return True
        
        except Exception as e:
            print(f"Error validating file path: {e}")
            return False
    
    def get_file_info(self, file_path):
        """Get information about a file."""
        try:
            if not self.validate_file_path(file_path):
                return None
            
            file_stats = os.stat(file_path)
            mime_type, _ = mimetypes.guess_type(file_path)
            
            return {
                'path': file_path,
                'size': file_stats.st_size,
                'mime_type': mime_type,
                'modified_time': file_stats.st_mtime,
                'extension': os.path.splitext(file_path)[1].lower()
            }
        
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None