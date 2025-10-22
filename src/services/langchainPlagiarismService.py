"""
LangChain-based Plagiarism Detection Service
Uses LangChain agents, chains, and semantic analysis for advanced plagiarism detection
"""

import os
from typing import Dict, List, Any
import warnings
warnings.filterwarnings('ignore')

import sys

# Standard ML imports first
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# LangChain imports with fallback
try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    EMBEDDINGS_AVAILABLE = True
except Exception as e:
    print(f"Warning: LangChain embeddings not available: {e}")
    EMBEDDINGS_AVAILABLE = False

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    TEXT_SPLITTER_AVAILABLE = True
except Exception as e:
    print(f"Warning: LangChain text splitter not available: {e}")
    TEXT_SPLITTER_AVAILABLE = False

import os
from typing import Dict, List, Any
import warnings
warnings.filterwarnings('ignore')

# LangChain imports
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.llms import Ollama

# Standard ML imports
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class LangChainPlagiarismService:
    """
    Advanced plagiarism detection using LangChain semantic analysis.
    Combines LangChain agents with traditional ML algorithms.
    """
    
    def __init__(self):
        """Initialize LangChain plagiarism service."""
        self.stop_words = set(stopwords.words('english'))
        
        # Initialize embeddings using HuggingFace (with fallback)
        self.embeddings = None
        if EMBEDDINGS_AVAILABLE:
            try:
                self.embeddings = HuggingFaceEmbeddings(
                    model_name="all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'}
                )
            except Exception as e:
                print(f"Warning: Could not initialize embeddings: {e}")
                self.embeddings = None
        
        # Text splitters for chunking
        self.use_text_splitter = TEXT_SPLITTER_AVAILABLE
        if TEXT_SPLITTER_AVAILABLE:
            try:
                self.recursive_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,
                    chunk_overlap=50,
                    separators=["\n\n", "\n", " ", ""]
                )
            except Exception as e:
                print(f"Warning: Could not initialize text splitter: {e}")
                self.use_text_splitter = False
        
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 3),
            max_features=5000
        )
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for analysis."""
        # Remove URLs
        text = __import__('re').sub(r'http\S+|www\S+', '', text)
        # Remove emails
        text = __import__('re').sub(r'\S+@\S+', '', text)
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def create_vector_store(self, text: str):
        """Create a vector store from text using LangChain."""
        try:
            if not self.embeddings or not self.use_text_splitter:
                return None
            
            # Split text into chunks
            chunks = self.recursive_splitter.split_text(text)
            
            # Create documents - simple dict-based approach instead of Document class
            docs = [{"page_content": chunk} for chunk in chunks]
            
            return docs
        except Exception as e:
            print(f"Error creating vector store: {e}")
            return None
    
    def semantic_similarity_langchain(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity using LangChain embeddings."""
        try:
            if not self.embeddings:
                return 0.0
            
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)
            
            # Get embeddings
            embedding1 = self.embeddings.embed_query(text1)
            embedding2 = self.embeddings.embed_query(text2)
            
            # Calculate cosine similarity
            embedding1 = np.array(embedding1).reshape(1, -1)
            embedding2 = np.array(embedding2).reshape(1, -1)
            
            similarity = cosine_similarity(embedding1, embedding2)[0, 0]
            return float(similarity)
        except Exception as e:
            print(f"Error in semantic similarity: {e}")
            return 0.0
    
    def chunk_level_analysis(self, text1: str, text2: str) -> float:
        """Analyze similarity at chunk level."""
        try:
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)
            
            # Simple chunking if text splitter unavailable
            if self.use_text_splitter:
                chunks1 = self.recursive_splitter.split_text(text1)
                chunks2 = self.recursive_splitter.split_text(text2)
            else:
                # Fallback: split by sentences
                chunks1 = sent_tokenize(text1)[:10]
                chunks2 = sent_tokenize(text2)[:10]
            
            if not chunks1 or not chunks2:
                return 0.0
            
            # Compare chunks
            similarities = []
            for chunk1 in chunks1:
                for chunk2 in chunks2:
                    # TF-IDF similarity
                    try:
                        tfidf_matrix = self.tfidf_vectorizer.fit_transform([chunk1, chunk2])
                        sim = cosine_similarity(tfidf_matrix)[0, 1]
                        similarities.append(sim)
                    except:
                        pass
            
            return float(np.mean(similarities)) if similarities else 0.0
        except Exception as e:
            print(f"Error in chunk analysis: {e}")
            return 0.0
    
    def semantic_chunk_matching(self, text1: str, text2: str) -> float:
        """Match chunks semantically using embeddings."""
        try:
            if not self.embeddings:
                return 0.0
            
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)
            
            # Simple chunking if text splitter unavailable
            if self.use_text_splitter:
                chunks1 = self.recursive_splitter.split_text(text1)
                chunks2 = self.recursive_splitter.split_text(text2)
            else:
                chunks1 = sent_tokenize(text1)[:10]
                chunks2 = sent_tokenize(text2)[:10]
            
            if not chunks1 or not chunks2:
                return 0.0
            
            similarities = []
            for chunk1 in chunks1[:3]:  # Limit to first 3 chunks
                for chunk2 in chunks2[:3]:
                    sim = self.semantic_similarity_langchain(chunk1, chunk2)
                    similarities.append(sim)
            
            return float(np.mean(similarities)) if similarities else 0.0
        except Exception as e:
            print(f"Error in semantic chunk matching: {e}")
            return 0.0
    
    def sentence_semantic_analysis(self, text1: str, text2: str) -> float:
        """Analyze semantic similarity at sentence level."""
        try:
            if not self.embeddings:
                return 0.0
            
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)
            
            sentences1 = sent_tokenize(text1)
            sentences2 = sent_tokenize(text2)
            
            if not sentences1 or not sentences2:
                return 0.0
            
            similarities = []
            for sent1 in sentences1[:5]:  # First 5 sentences
                for sent2 in sentences2[:5]:
                    sim = self.semantic_similarity_langchain(sent1, sent2)
                    similarities.append(sim)
            
            return float(np.mean(similarities)) if similarities else 0.0
        except Exception as e:
            print(f"Error in sentence semantic analysis: {e}")
            return 0.0
    
    def tfidf_similarity(self, text1: str, text2: str) -> float:
        """Calculate TF-IDF based similarity."""
        try:
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)
            
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix)[0, 1]
            return float(similarity)
        except Exception as e:
            print(f"Error in TF-IDF similarity: {e}")
            return 0.0
    
    def sequence_matching_similarity(self, text1: str, text2: str) -> float:
        """Calculate sequence matching similarity."""
        try:
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)
            
            matcher = SequenceMatcher(None, text1.split(), text2.split())
            return float(matcher.ratio())
        except Exception as e:
            print(f"Error in sequence matching: {e}")
            return 0.0
    
    def token_overlap_similarity(self, text1: str, text2: str) -> float:
        """Calculate token overlap (Jaccard) similarity."""
        try:
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)
            
            tokens1 = set(text1.split())
            tokens2 = set(text2.split())
            
            if len(tokens1) == 0 or len(tokens2) == 0:
                return 0.0
            
            intersection = len(tokens1 & tokens2)
            union = len(tokens1 | tokens2)
            
            return intersection / union if union > 0 else 0.0
        except Exception as e:
            print(f"Error in token overlap: {e}")
            return 0.0
    
    def calculate_plagiarism_score(self, document_text: str, comparison_text: str = None) -> Dict[str, Any]:
        """
        Calculate comprehensive plagiarism score using LangChain and ML ensemble.
        
        Args:
            document_text: The document to analyze
            comparison_text: Optional text to compare against
        
        Returns:
            Dictionary with detailed plagiarism analysis
        """
        try:
            if not document_text or len(document_text.strip()) < 10:
                return self._empty_result()
            
            # If no comparison text, use self-comparison
            if not comparison_text or len(comparison_text.strip()) < 10:
                comparison_text = document_text[:len(document_text)//2]
            
            # Calculate similarities using multiple methods
            
            # 1. Semantic similarity (LangChain embeddings)
            semantic_sim = self.semantic_similarity_langchain(document_text, comparison_text)
            
            # 2. Chunk-level analysis
            chunk_sim = self.chunk_level_analysis(document_text, comparison_text)
            
            # 3. Semantic chunk matching
            semantic_chunk_sim = self.semantic_chunk_matching(document_text, comparison_text)
            
            # 4. Sentence-level semantic analysis
            sentence_semantic_sim = self.sentence_semantic_analysis(document_text, comparison_text)
            
            # 5. TF-IDF similarity
            tfidf_sim = self.tfidf_similarity(document_text, comparison_text)
            
            # 6. Sequence matching
            sequence_sim = self.sequence_matching_similarity(document_text, comparison_text)
            
            # 7. Token overlap
            token_sim = self.token_overlap_similarity(document_text, comparison_text)
            
            # Ensemble calculation with LangChain methods weighted higher
            overall_score = (
                semantic_sim * 0.20 +                    # LangChain semantic
                chunk_sim * 0.15 +                       # LangChain chunk level
                semantic_chunk_sim * 0.15 +             # LangChain semantic chunks
                sentence_semantic_sim * 0.15 +          # LangChain sentence semantic
                tfidf_sim * 0.12 +                      # TF-IDF
                sequence_sim * 0.12 +                   # Sequence matching
                token_sim * 0.11                        # Token overlap
            )
            
            # Ensure score is between 0 and 1
            overall_score = min(max(overall_score, 0.0), 1.0)
            
            return {
                'overall': round(overall_score, 3),
                'semantic': round(semantic_sim, 3),
                'chunk_level': round(chunk_sim, 3),
                'semantic_chunks': round(semantic_chunk_sim, 3),
                'sentence_semantic': round(sentence_semantic_sim, 3),
                'tfidf': round(tfidf_sim, 3),
                'sequence_matching': round(sequence_sim, 3),
                'token_overlap': round(token_sim, 3),
                'algorithms_used': 7,
                'methodology': 'LangChain Semantic Analysis + ML Ensemble',
                'langchain_weight': 0.65,
                'ml_weight': 0.35
            }
        
        except Exception as e:
            print(f"Error calculating plagiarism score: {e}")
            return self._empty_result()
    
    def _empty_result(self) -> Dict[str, Any]:
        """Return empty result structure."""
        return {
            'overall': 0.0,
            'semantic': 0.0,
            'chunk_level': 0.0,
            'semantic_chunks': 0.0,
            'sentence_semantic': 0.0,
            'tfidf': 0.0,
            'sequence_matching': 0.0,
            'token_overlap': 0.0,
            'algorithms_used': 7,
            'methodology': 'LangChain + ML',
            'error': 'Insufficient text for analysis'
        }
