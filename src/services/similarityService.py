"""
Similarity Service for plagiarism detection.
Implements various text similarity algorithms.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import requests
from bs4 import BeautifulSoup
from textdistance import jaccard, levenshtein
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import string

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class SimilarityService:
    """Service for calculating text similarity and detecting plagiarism."""
    
    def __init__(self):
        """Initialize the similarity service."""
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 3),
            max_features=5000
        )
    
    def preprocess_text(self, text):
        """Preprocess text for similarity analysis."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation and special characters
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Tokenize and remove stopwords
        tokens = word_tokenize(text)
        tokens = [token for token in tokens if token not in self.stop_words]
        
        return ' '.join(tokens)
    
    def calculate_cosine_similarity(self, text1, text2):
        """Calculate cosine similarity between two texts."""
        try:
            # Preprocess texts
            processed_text1 = self.preprocess_text(text1)
            processed_text2 = self.preprocess_text(text2)
            
            # Create TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform([processed_text1, processed_text2])
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            return float(similarity_matrix[0, 1])
        
        except Exception as e:
            print(f"Error calculating cosine similarity: {e}")
            return 0.0
    
    def calculate_jaccard_similarity(self, text1, text2):
        """Calculate Jaccard similarity between two texts."""
        try:
            # Preprocess and tokenize
            tokens1 = set(word_tokenize(self.preprocess_text(text1)))
            tokens2 = set(word_tokenize(self.preprocess_text(text2)))
            
            # Calculate Jaccard similarity
            return float(jaccard(tokens1, tokens2))
        
        except Exception as e:
            print(f"Error calculating Jaccard similarity: {e}")
            return 0.0
    
    def calculate_levenshtein_similarity(self, text1, text2):
        """Calculate normalized Levenshtein similarity between two texts."""
        try:
            # Calculate Levenshtein distance
            distance = levenshtein(text1, text2)
            max_length = max(len(text1), len(text2))
            
            # Normalize to similarity score (0-1)
            if max_length == 0:
                return 1.0
            
            return 1.0 - (distance / max_length)
        
        except Exception as e:
            print(f"Error calculating Levenshtein similarity: {e}")
            return 0.0
    
    def calculate_similarity(self, text1, text2):
        """Calculate overall similarity using multiple algorithms."""
        try:
            # Calculate different similarity metrics
            cosine_sim = self.calculate_cosine_similarity(text1, text2)
            jaccard_sim = self.calculate_jaccard_similarity(text1, text2)
            levenshtein_sim = self.calculate_levenshtein_similarity(text1, text2)
            
            # Weighted average (cosine similarity gets more weight for semantic similarity)
            overall_similarity = (
                cosine_sim * 0.5 +
                jaccard_sim * 0.3 +
                levenshtein_sim * 0.2
            )
            
            return {
                'overall': round(overall_similarity, 3),
                'cosine': round(cosine_sim, 3),
                'jaccard': round(jaccard_sim, 3),
                'levenshtein': round(levenshtein_sim, 3)
            }
        
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return {
                'overall': 0.0,
                'cosine': 0.0,
                'jaccard': 0.0,
                'levenshtein': 0.0
            }
    
    def find_similar_sentences(self, text1, text2, threshold=0.7):
        """Find similar sentences between two texts."""
        try:
            sentences1 = sent_tokenize(text1)
            sentences2 = sent_tokenize(text2)
            
            similar_pairs = []
            
            for i, sent1 in enumerate(sentences1):
                for j, sent2 in enumerate(sentences2):
                    similarity = self.calculate_cosine_similarity(sent1, sent2)
                    if similarity >= threshold:
                        similar_pairs.append({
                            'sentence1': sent1,
                            'sentence2': sent2,
                            'similarity': round(similarity, 3),
                            'position1': i,
                            'position2': j
                        })
            
            # Sort by similarity score
            similar_pairs.sort(key=lambda x: x['similarity'], reverse=True)
            
            return similar_pairs
        
        except Exception as e:
            print(f"Error finding similar sentences: {e}")
            return []
    
    def search_web_matches(self, text_snippet, max_results=5):
        """Search for potential web matches (simplified implementation)."""
        try:
            # This is a simplified implementation
            # In a production system, you would use proper search APIs
            
            # For demo purposes, return mock results
            mock_results = [
                {
                    'url': 'https://example.com/document1',
                    'title': 'Similar Document Found',
                    'snippet': text_snippet[:100] + '...',
                    'similarity_score': 0.75,
                    'source_type': 'web'
                },
                {
                    'url': 'https://example.com/academic-paper',
                    'title': 'Academic Paper with Similar Content',
                    'snippet': 'This document contains similar content...',
                    'similarity_score': 0.68,
                    'source_type': 'academic'
                }
            ]
            
            return mock_results[:max_results]
        
        except Exception as e:
            print(f"Error searching web matches: {e}")
            return []
    
    def analyze_document_structure(self, text):
        """Analyze document structure for potential plagiarism patterns."""
        try:
            sentences = sent_tokenize(text)
            paragraphs = text.split('\n\n')
            
            analysis = {
                'sentence_count': len(sentences),
                'paragraph_count': len(paragraphs),
                'avg_sentence_length': np.mean([len(s.split()) for s in sentences]),
                'avg_paragraph_length': np.mean([len(p.split()) for p in paragraphs if p.strip()]),
                'unique_words': len(set(word_tokenize(text.lower()))),
                'total_words': len(word_tokenize(text))
            }
            
            # Calculate readability metrics
            analysis['vocabulary_diversity'] = analysis['unique_words'] / analysis['total_words'] if analysis['total_words'] > 0 else 0
            
            return analysis
        
        except Exception as e:
            print(f"Error analyzing document structure: {e}")
            return {}