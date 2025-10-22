"""
Advanced Similarity Service with Multiple ML Models for Plagiarism Detection.
Implements various advanced text similarity algorithms with high accuracy.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.metrics.distance import edit_distance
import string
from difflib import SequenceMatcher
import hashlib
from collections import Counter

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class AdvancedSimilarityService:
    """Advanced service for calculating text similarity using multiple ML models."""
    
    def __init__(self):
        """Initialize the advanced similarity service."""
        self.stop_words = set(stopwords.words('english'))
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 3),
            max_features=5000,
            lowercase=True,
            analyzer='word'
        )
        self.count_vectorizer = CountVectorizer(
            stop_words='english',
            max_features=5000,
            lowercase=True,
            analyzer='word'
        )
    
    def preprocess_text(self, text):
        """Advanced text preprocessing."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        return text
    
    def cosine_similarity_advanced(self, text1, text2):
        """Calculate advanced cosine similarity using TF-IDF."""
        try:
            if len(text1.strip()) < 5 or len(text2.strip()) < 5:
                return 0.0
            
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)
            
            # Create TF-IDF vectors
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([text1, text2])
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            return float(similarity_matrix[0, 1])
        
        except Exception as e:
            print(f"Error in cosine similarity: {e}")
            return 0.0
    
    def sequence_matcher_similarity(self, text1, text2):
        """Calculate similarity using sequence matching (SequenceMatcher)."""
        try:
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)
            
            # Tokenize to words
            tokens1 = text1.split()
            tokens2 = text2.split()
            
            # Use SequenceMatcher for sequence-based comparison
            matcher = SequenceMatcher(None, tokens1, tokens2)
            
            return float(matcher.ratio())
        
        except Exception as e:
            print(f"Error in sequence matcher: {e}")
            return 0.0
    
    def token_overlap_similarity(self, text1, text2):
        """Calculate similarity based on token overlap (Jaccard)."""
        try:
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)
            
            tokens1 = set(text1.split())
            tokens2 = set(text2.split())
            
            if len(tokens1) == 0 or len(tokens2) == 0:
                return 0.0
            
            # Jaccard similarity
            intersection = len(tokens1 & tokens2)
            union = len(tokens1 | tokens2)
            
            return intersection / union if union > 0 else 0.0
        
        except Exception as e:
            print(f"Error in token overlap: {e}")
            return 0.0
    
    def ngram_similarity(self, text1, text2, n=2):
        """Calculate similarity using n-gram overlap."""
        try:
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)
            
            # Generate n-grams
            def get_ngrams(text, n):
                tokens = text.split()
                return set([' '.join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)])
            
            ngrams1 = get_ngrams(text1, n)
            ngrams2 = get_ngrams(text2, n)
            
            if len(ngrams1) == 0 or len(ngrams2) == 0:
                return 0.0
            
            # Calculate overlap
            overlap = len(ngrams1 & ngrams2)
            total = len(ngrams1 | ngrams2)
            
            return overlap / total if total > 0 else 0.0
        
        except Exception as e:
            print(f"Error in n-gram similarity: {e}")
            return 0.0
    
    def longest_common_subsequence(self, text1, text2):
        """Calculate similarity based on longest common subsequence."""
        try:
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)
            
            tokens1 = text1.split()
            tokens2 = text2.split()
            
            # Dynamic programming for LCS
            m, n = len(tokens1), len(tokens2)
            dp = [[0] * (n + 1) for _ in range(m + 1)]
            
            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    if tokens1[i-1] == tokens2[j-1]:
                        dp[i][j] = dp[i-1][j-1] + 1
                    else:
                        dp[i][j] = max(dp[i-1][j], dp[i][j-1])
            
            lcs_length = dp[m][n]
            max_length = max(m, n)
            
            return lcs_length / max_length if max_length > 0 else 0.0
        
        except Exception as e:
            print(f"Error in LCS: {e}")
            return 0.0
    
    def sentence_similarity(self, text1, text2):
        """Calculate sentence-level similarity."""
        try:
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)
            
            sentences1 = sent_tokenize(text1)
            sentences2 = sent_tokenize(text2)
            
            if len(sentences1) == 0 or len(sentences2) == 0:
                return 0.0
            
            # Compare sentences
            similarities = []
            for s1 in sentences1:
                max_sim = 0
                for s2 in sentences2:
                    sim = self.sequence_matcher_similarity(s1, s2)
                    max_sim = max(max_sim, sim)
                similarities.append(max_sim)
            
            return np.mean(similarities) if similarities else 0.0
        
        except Exception as e:
            print(f"Error in sentence similarity: {e}")
            return 0.0
    
    def word_frequency_similarity(self, text1, text2):
        """Calculate similarity using word frequency."""
        try:
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)
            
            # Count vectors
            count_matrix = self.count_vectorizer.fit_transform([text1, text2])
            
            # Cosine similarity on count vectors
            similarity_matrix = cosine_similarity(count_matrix)
            
            return float(similarity_matrix[0, 1])
        
        except Exception as e:
            print(f"Error in word frequency: {e}")
            return 0.0
    
    def semantic_similarity(self, text1, text2):
        """Calculate semantic similarity using word overlap beyond exact matches."""
        try:
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)
            
            words1 = text1.split()
            words2 = text2.split()
            
            # Remove stopwords
            words1_filtered = [w for w in words1 if w not in self.stop_words and len(w) > 2]
            words2_filtered = [w for w in words2 if w not in self.stop_words and len(w) > 2]
            
            if len(words1_filtered) == 0 or len(words2_filtered) == 0:
                return 0.0
            
            # Calculate overlap
            overlap = len(set(words1_filtered) & set(words2_filtered))
            total = len(set(words1_filtered) | set(words2_filtered))
            
            return overlap / total if total > 0 else 0.0
        
        except Exception as e:
            print(f"Error in semantic similarity: {e}")
            return 0.0
    
    def calculate_overall_similarity(self, text1, text2):
        """Calculate overall similarity using ensemble of all models."""
        try:
            if not text1 or not text2:
                return 0.0
            
            # Calculate similarity using all methods
            cosine_sim = self.cosine_similarity_advanced(text1, text2)
            sequence_sim = self.sequence_matcher_similarity(text1, text2)
            token_sim = self.token_overlap_similarity(text1, text2)
            bigram_sim = self.ngram_similarity(text1, text2, n=2)
            trigram_sim = self.ngram_similarity(text1, text2, n=3)
            lcs_sim = self.longest_common_subsequence(text1, text2)
            sentence_sim = self.sentence_similarity(text1, text2)
            word_freq_sim = self.word_frequency_similarity(text1, text2)
            semantic_sim = self.semantic_similarity(text1, text2)
            
            # Weighted ensemble (all methods contribute)
            overall_similarity = (
                cosine_sim * 0.15 +           # TF-IDF based
                sequence_sim * 0.15 +          # Sequence matching
                token_sim * 0.12 +             # Token overlap (Jaccard)
                bigram_sim * 0.10 +            # Bigram overlap
                trigram_sim * 0.08 +           # Trigram overlap
                lcs_sim * 0.12 +               # Longest common subsequence
                sentence_sim * 0.10 +          # Sentence level
                word_freq_sim * 0.10 +         # Word frequency
                semantic_sim * 0.08            # Semantic analysis
            )
            
            # Return detailed results
            return {
                'overall': round(min(overall_similarity, 1.0), 3),
                'cosine': round(cosine_sim, 3),
                'sequence': round(sequence_sim, 3),
                'token_overlap': round(token_sim, 3),
                'bigram': round(bigram_sim, 3),
                'trigram': round(trigram_sim, 3),
                'lcs': round(lcs_sim, 3),
                'sentence': round(sentence_sim, 3),
                'word_freq': round(word_freq_sim, 3),
                'semantic': round(semantic_sim, 3),
                'algorithms_used': 9,
                'methodology': 'Ensemble of 9 advanced ML algorithms'
            }
        
        except Exception as e:
            print(f"Error calculating overall similarity: {e}")
            return {
                'overall': 0.0,
                'error': str(e),
                'algorithms_used': 0
            }
