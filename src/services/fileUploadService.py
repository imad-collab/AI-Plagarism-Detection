"""
File Upload Service for handling document uploads and processing.
"""

import os
import uuid
from datetime import datetime
import mimetypes
from werkzeug.utils import secure_filename
import PyPDF2
import docx
import json

class FileUploadService:
    """Service for handling file uploads and processing."""
    
    def __init__(self, upload_folder=None):
        """Initialize the file upload service."""
        self.upload_folder = upload_folder or 'uploads'
        self.allowed_extensions = {
            'txt', 'pdf', 'doc', 'docx', 'rtf'
        }
        self.max_file_size = 16 * 1024 * 1024  # 16MB
        
        # Create upload folder if it doesn't exist
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def allowed_file(self, filename):
        """Check if file extension is allowed."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF file."""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def extract_text_from_docx(self, file_path):
        """Extract text from DOCX file."""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return ""
    
    def extract_text_from_txt(self, file_path):
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                print(f"Error extracting text from TXT: {e}")
                return ""
        except Exception as e:
            print(f"Error extracting text from TXT: {e}")
            return ""
    
    def extract_text(self, file_path, file_extension):
        """Extract text from file based on its extension."""
        try:
            if file_extension.lower() == 'pdf':
                return self.extract_text_from_pdf(file_path)
            elif file_extension.lower() in ['doc', 'docx']:
                return self.extract_text_from_docx(file_path)
            elif file_extension.lower() in ['txt', 'rtf']:
                return self.extract_text_from_txt(file_path)
            else:
                return ""
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    
    def save_file(self, file):
        """Save uploaded file and extract text."""
        try:
            if not file or not self.allowed_file(file.filename):
                return {
                    'success': False,
                    'error': 'Invalid file type'
                }
            
            # Generate unique file ID
            file_id = str(uuid.uuid4())
            
            # Secure the filename
            original_filename = secure_filename(file.filename)
            file_extension = original_filename.rsplit('.', 1)[1].lower()
            
            # Create file paths
            uploaded_file_path = os.path.join(self.upload_folder, f"{file_id}.{file_extension}")
            text_file_path = os.path.join(self.upload_folder, f"{file_id}.txt")
            metadata_file_path = os.path.join(self.upload_folder, f"{file_id}.json")
            
            # Save the uploaded file
            file.save(uploaded_file_path)
            
            # Extract text from the file
            extracted_text = self.extract_text(uploaded_file_path, file_extension)
            
            if not extracted_text:
                # Clean up and return error
                if os.path.exists(uploaded_file_path):
                    os.remove(uploaded_file_path)
                return {
                    'success': False,
                    'error': 'Could not extract text from file'
                }
            
            # Save extracted text
            with open(text_file_path, 'w', encoding='utf-8') as f:
                f.write(extracted_text)
            
            # Save metadata
            metadata = {
                'file_id': file_id,
                'original_filename': original_filename,
                'file_extension': file_extension,
                'upload_timestamp': datetime.now().isoformat(),
                'file_size': os.path.getsize(uploaded_file_path),
                'text_length': len(extracted_text),
                'word_count': len(extracted_text.split()),
                'status': 'processed'
            }
            
            with open(metadata_file_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            return {
                'success': True,
                'file_id': file_id,
                'filename': original_filename,
                'text_length': len(extracted_text),
                'word_count': len(extracted_text.split())
            }
        
        except Exception as e:
            print(f"Error saving file: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_file_data(self, file_id):
        """Get file data including text and metadata."""
        try:
            metadata = self.get_file_metadata(file_id)
            if not metadata:
                return None
            
            text = self.get_file_text(file_id)
            if text is None:
                return None
            
            return {
                'text': text,
                'filename': metadata.get('filename'),
                'file_type': metadata.get('file_type'),
                'upload_time': metadata.get('upload_time'),
                'file_id': file_id
            }
        except Exception as e:
            print(f"Error getting file data: {e}")
            return None
    
    def get_file_text(self, file_id):
        """Get extracted text for a file."""
        try:
            text_file_path = os.path.join(self.upload_folder, f"{file_id}.txt")
            
            if not os.path.exists(text_file_path):
                return None
            
            with open(text_file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        except Exception as e:
            print(f"Error getting file text: {e}")
            return None
    
    def get_file_metadata(self, file_id):
        """Get metadata for a file."""
        try:
            metadata_file_path = os.path.join(self.upload_folder, f"{file_id}.json")
            
            if not os.path.exists(metadata_file_path):
                return None
            
            with open(metadata_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        except Exception as e:
            print(f"Error getting file metadata: {e}")
            return None
    
    def list_documents(self):
        """List all uploaded documents."""
        try:
            documents = []
            
            if not os.path.exists(self.upload_folder):
                return documents
            
            # Find all metadata files
            for filename in os.listdir(self.upload_folder):
                if filename.endswith('.json'):
                    file_id = filename[:-5]  # Remove .json extension
                    metadata = self.get_file_metadata(file_id)
                    if metadata:
                        documents.append(metadata)
            
            # Sort by upload timestamp (newest first)
            documents.sort(key=lambda x: x.get('upload_timestamp', ''), reverse=True)
            
            return documents
        
        except Exception as e:
            print(f"Error listing documents: {e}")
            return []
    
    def delete_file(self, file_id):
        """Delete a file and its associated data."""
        try:
            files_to_delete = [
                f"{file_id}.txt",
                f"{file_id}.json"
            ]
            
            # Find and delete the original file
            for filename in os.listdir(self.upload_folder):
                if filename.startswith(file_id) and not filename.endswith(('.txt', '.json')):
                    files_to_delete.append(filename)
            
            deleted_count = 0
            for filename in files_to_delete:
                file_path = os.path.join(self.upload_folder, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_count += 1
            
            return {
                'success': True,
                'deleted_files': deleted_count
            }
        
        except Exception as e:
            print(f"Error deleting file: {e}")
            return {
                'success': False,
                'error': str(e)
            }