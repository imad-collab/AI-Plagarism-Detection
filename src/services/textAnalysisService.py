"""
Text Analysis Service for analyzing document characteristics and patterns.
"""

import re
import numpy as np
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from textstat import flesch_reading_ease, flesch_kincaid_grade
import string

class TextAnalysisService:
    """Service for analyzing text characteristics and patterns."""
    
    def __init__(self):
        """Initialize the text analysis service."""
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))
        
        # Download required NLTK data
        try:
            nltk.data.find('averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')
    
    def analyze_text(self, text):
        """Perform comprehensive text analysis."""
        try:
            # Basic statistics
            basic_stats = self._get_basic_statistics(text)
            
            # Linguistic features
            linguistic_features = self._get_linguistic_features(text)
            
            # Readability metrics
            readability = self._get_readability_metrics(text)
            
            # Vocabulary analysis
            vocabulary = self._analyze_vocabulary(text)
            
            # Pattern analysis
            patterns = self._analyze_patterns(text)
            
            return {
                'basic_statistics': basic_stats,
                'linguistic_features': linguistic_features,
                'readability': readability,
                'vocabulary': vocabulary,
                'patterns': patterns,
                'analysis_timestamp': nltk.datetime.datetime.now().isoformat()
            }
        
        except Exception as e:
            print(f"Error in text analysis: {e}")
            return {}
    
    def _get_basic_statistics(self, text):
        """Get basic text statistics."""
        try:
            sentences = sent_tokenize(text)
            words = word_tokenize(text)
            paragraphs = [p for p in text.split('\n\n') if p.strip()]
            
            # Character counts
            char_count = len(text)
            char_count_no_spaces = len(text.replace(' ', ''))
            
            # Word statistics
            word_count = len(words)
            unique_words = len(set(word.lower() for word in words if word.isalpha()))
            
            # Sentence statistics
            sentence_count = len(sentences)
            avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
            
            # Paragraph statistics
            paragraph_count = len(paragraphs)
            avg_paragraph_length = sentence_count / paragraph_count if paragraph_count > 0 else 0
            
            return {
                'character_count': char_count,
                'character_count_no_spaces': char_count_no_spaces,
                'word_count': word_count,
                'unique_word_count': unique_words,
                'sentence_count': sentence_count,
                'paragraph_count': paragraph_count,
                'average_sentence_length': round(avg_sentence_length, 2),
                'average_paragraph_length': round(avg_paragraph_length, 2),
                'lexical_diversity': round(unique_words / word_count, 3) if word_count > 0 else 0
            }
        
        except Exception as e:
            print(f"Error getting basic statistics: {e}")
            return {}
    
    def _get_linguistic_features(self, text):
        """Analyze linguistic features."""
        try:
            words = word_tokenize(text)
            words_alpha = [word.lower() for word in words if word.isalpha()]
            
            # Part-of-speech tagging
            pos_tags = pos_tag(words)
            pos_counts = Counter([tag for word, tag in pos_tags])
            
            # Most common POS tags as percentages
            total_pos = len(pos_tags)
            pos_percentages = {
                'nouns': (pos_counts.get('NN', 0) + pos_counts.get('NNS', 0) + 
                         pos_counts.get('NNP', 0) + pos_counts.get('NNPS', 0)) / total_pos * 100,
                'verbs': (pos_counts.get('VB', 0) + pos_counts.get('VBD', 0) + 
                         pos_counts.get('VBG', 0) + pos_counts.get('VBN', 0) + 
                         pos_counts.get('VBP', 0) + pos_counts.get('VBZ', 0)) / total_pos * 100,
                'adjectives': (pos_counts.get('JJ', 0) + pos_counts.get('JJR', 0) + 
                              pos_counts.get('JJS', 0)) / total_pos * 100,
                'adverbs': (pos_counts.get('RB', 0) + pos_counts.get('RBR', 0) + 
                           pos_counts.get('RBS', 0)) / total_pos * 100
            }
            
            # Function words (articles, prepositions, etc.)
            function_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
            function_word_count = sum(1 for word in words_alpha if word in function_words)
            function_word_ratio = function_word_count / len(words_alpha) if words_alpha else 0
            
            return {
                'pos_distribution': {k: round(v, 2) for k, v in pos_percentages.items()},
                'function_word_ratio': round(function_word_ratio, 3),
                'total_pos_tags': len(set(tag for word, tag in pos_tags))
            }
        
        except Exception as e:
            print(f"Error getting linguistic features: {e}")
            return {}
    
    def _get_readability_metrics(self, text):
        """Calculate readability metrics."""
        try:
            # Using textstat library for standard readability metrics
            flesch_ease = flesch_reading_ease(text)
            flesch_grade = flesch_kincaid_grade(text)
            
            # Custom metrics
            sentences = sent_tokenize(text)
            words = word_tokenize(text)
            
            # Average word length
            word_lengths = [len(word) for word in words if word.isalpha()]
            avg_word_length = np.mean(word_lengths) if word_lengths else 0
            
            # Syllable approximation (rough estimate)
            def count_syllables(word):
                word = word.lower()
                vowels = 'aeiouy'
                syllables = 0
                previous_was_vowel = False
                
                for char in word:
                    if char in vowels:
                        if not previous_was_vowel:
                            syllables += 1
                        previous_was_vowel = True
                    else:
                        previous_was_vowel = False
                
                # Handle silent 'e'
                if word.endswith('e') and syllables > 1:
                    syllables -= 1
                
                return max(1, syllables)  # Every word has at least one syllable
            
            total_syllables = sum(count_syllables(word) for word in words if word.isalpha())
            avg_syllables_per_word = total_syllables / len(words) if words else 0
            
            return {
                'flesch_reading_ease': round(flesch_ease, 2),
                'flesch_kincaid_grade': round(flesch_grade, 2),
                'average_word_length': round(avg_word_length, 2),
                'average_syllables_per_word': round(avg_syllables_per_word, 2),
                'reading_level': self._interpret_flesch_score(flesch_ease)
            }
        
        except Exception as e:
            print(f"Error calculating readability metrics: {e}")
            return {}
    
    def _interpret_flesch_score(self, score):
        """Interpret Flesch Reading Ease score."""
        if score >= 90:
            return "Very Easy"
        elif score >= 80:
            return "Easy"
        elif score >= 70:
            return "Fairly Easy"
        elif score >= 60:
            return "Standard"
        elif score >= 50:
            return "Fairly Difficult"
        elif score >= 30:
            return "Difficult"
        else:
            return "Very Difficult"
    
    def _analyze_vocabulary(self, text):
        """Analyze vocabulary usage."""
        try:
            words = word_tokenize(text.lower())
            words_alpha = [word for word in words if word.isalpha()]
            
            # Word frequency
            word_freq = Counter(words_alpha)
            most_common = word_freq.most_common(10)
            
            # Stopword ratio
            stopword_count = sum(1 for word in words_alpha if word in self.stop_words)
            stopword_ratio = stopword_count / len(words_alpha) if words_alpha else 0
            
            # Rare words (words that appear only once)
            rare_words = sum(1 for count in word_freq.values() if count == 1)
            rare_word_ratio = rare_words / len(word_freq) if word_freq else 0
            
            return {
                'most_common_words': most_common,
                'stopword_ratio': round(stopword_ratio, 3),
                'rare_word_ratio': round(rare_word_ratio, 3),
                'vocabulary_size': len(word_freq)
            }
        
        except Exception as e:
            print(f"Error analyzing vocabulary: {e}")
            return {}
    
    def _analyze_patterns(self, text):
        """Analyze text patterns that might indicate plagiarism."""
        try:
            patterns = {}
            
            # Detect potential citation patterns
            citation_patterns = [
                r'\([^)]*\d{4}[^)]*\)',  # (Author, 2023)
                r'\[[^\]]*\d+[^\]]*\]',  # [1], [Smith et al.]
                r'according to [A-Z][a-z]+',  # according to Smith
                r'as stated by [A-Z][a-z]+',  # as stated by Johnson
            ]
            
            citation_count = 0
            for pattern in citation_patterns:
                citation_count += len(re.findall(pattern, text))
            
            patterns['citation_count'] = citation_count
            
            # Detect quotations
            quote_pattern = r'"[^"]{10,}"'  # Quoted text longer than 10 characters
            quotes = re.findall(quote_pattern, text)
            patterns['quote_count'] = len(quotes)
            
            # Detect URLs
            url_pattern = r'https?://[^\s]+'
            urls = re.findall(url_pattern, text)
            patterns['url_count'] = len(urls)
            
            # Detect inconsistent formatting (different fonts, sizes might indicate copy-paste)
            # This is a simplified check for unusual character patterns
            unusual_chars = re.findall(r'[^\w\s\.,;:!?\-()"\']', text)
            patterns['unusual_character_count'] = len(unusual_chars)
            
            # Detect very long sentences (might indicate copy-paste)
            sentences = sent_tokenize(text)
            sentence_lengths = [len(word_tokenize(sent)) for sent in sentences]
            avg_sentence_length = np.mean(sentence_lengths) if sentence_lengths else 0
            long_sentences = sum(1 for length in sentence_lengths if length > 40)
            
            patterns['long_sentence_count'] = long_sentences
            patterns['average_sentence_length'] = round(avg_sentence_length, 2)
            
            # Calculate suspicion score
            suspicion_score = 0
            if citation_count > 5:
                suspicion_score += 1
            if len(quotes) > 3:
                suspicion_score += 1
            if long_sentences > 2:
                suspicion_score += 1
            if len(unusual_chars) > 10:
                suspicion_score += 1
            
            patterns['suspicion_score'] = suspicion_score
            patterns['suspicion_level'] = 'high' if suspicion_score >= 3 else 'medium' if suspicion_score >= 2 else 'low'
            
            return patterns
        
        except Exception as e:
            print(f"Error analyzing patterns: {e}")
            return {}