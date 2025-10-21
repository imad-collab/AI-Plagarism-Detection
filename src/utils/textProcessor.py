"""
Text Processor utility for text preprocessing and manipulation.
"""

import re
import string
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.chunk import ne_chunk
from nltk.tag import pos_tag
import unicodedata

class TextProcessor:
    """Utility class for text processing operations."""
    
    def __init__(self):
        """Initialize the text processor."""
        # Download required NLTK data
        required_downloads = [
            'punkt', 'stopwords', 'averaged_perceptron_tagger',
            'wordnet', 'omw-1.4', 'maxent_ne_chunker', 'words'
        ]
        
        for download in required_downloads:
            try:
                nltk.data.find(f'tokenizers/{download}')
            except LookupError:
                try:
                    nltk.data.find(f'corpora/{download}')
                except LookupError:
                    try:
                        nltk.data.find(f'taggers/{download}')
                    except LookupError:
                        try:
                            nltk.data.find(f'chunkers/{download}')
                        except LookupError:
                            try:
                                nltk.download(download, quiet=True)
                            except:
                                pass
        
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
    
    def clean_text(self, text):
        """Clean and normalize text."""
        try:
            # Normalize unicode characters
            text = unicodedata.normalize('NFKD', text)
            
            # Remove extra whitespace
            text = ' '.join(text.split())
            
            # Remove non-printable characters
            text = ''.join(char for char in text if char.isprintable())
            
            return text
        
        except Exception as e:
            print(f"Error cleaning text: {e}")
            return text
    
    def remove_punctuation(self, text):
        """Remove punctuation from text."""
        try:
            # Create translation table to remove punctuation
            translator = str.maketrans('', '', string.punctuation)
            return text.translate(translator)
        
        except Exception as e:
            print(f"Error removing punctuation: {e}")
            return text
    
    def normalize_text(self, text, lowercase=True, remove_punct=True, remove_digits=False):
        """Normalize text with various options."""
        try:
            if lowercase:
                text = text.lower()
            
            if remove_punct:
                text = self.remove_punctuation(text)
            
            if remove_digits:
                text = re.sub(r'\d+', '', text)
            
            # Remove extra whitespace
            text = ' '.join(text.split())
            
            return text
        
        except Exception as e:
            print(f"Error normalizing text: {e}")
            return text
    
    def tokenize_words(self, text):
        """Tokenize text into words."""
        try:
            return word_tokenize(text)
        except Exception as e:
            print(f"Error tokenizing words: {e}")
            return text.split()
    
    def tokenize_sentences(self, text):
        """Tokenize text into sentences."""
        try:
            return sent_tokenize(text)
        except Exception as e:
            print(f"Error tokenizing sentences: {e}")
            return text.split('.')
    
    def remove_stopwords(self, words):
        """Remove stopwords from list of words."""
        try:
            return [word for word in words if word.lower() not in self.stop_words]
        except Exception as e:
            print(f"Error removing stopwords: {e}")
            return words
    
    def stem_words(self, words):
        """Apply stemming to list of words."""
        try:
            return [self.stemmer.stem(word) for word in words]
        except Exception as e:
            print(f"Error stemming words: {e}")
            return words
    
    def lemmatize_words(self, words):
        """Apply lemmatization to list of words."""
        try:
            return [self.lemmatizer.lemmatize(word) for word in words]
        except Exception as e:
            print(f"Error lemmatizing words: {e}")
            return words
    
    def extract_entities(self, text):
        """Extract named entities from text."""
        try:
            words = word_tokenize(text)
            pos_tags = pos_tag(words)
            entities = ne_chunk(pos_tags)
            
            named_entities = []
            for chunk in entities:
                if hasattr(chunk, 'label'):
                    entity_name = ' '.join([token for token, pos in chunk.leaves()])
                    entity_type = chunk.label()
                    named_entities.append((entity_name, entity_type))
            
            return named_entities
        
        except Exception as e:
            print(f"Error extracting entities: {e}")
            return []
    
    def get_word_frequency(self, text, top_n=10):
        """Get word frequency distribution."""
        try:
            words = self.tokenize_words(self.normalize_text(text))
            words = self.remove_stopwords(words)
            
            from collections import Counter
            word_freq = Counter(words)
            
            return word_freq.most_common(top_n)
        
        except Exception as e:
            print(f"Error getting word frequency: {e}")
            return []
    
    def extract_ngrams(self, text, n=2):
        """Extract n-grams from text."""
        try:
            words = self.tokenize_words(self.normalize_text(text))
            words = self.remove_stopwords(words)
            
            ngrams = []
            for i in range(len(words) - n + 1):
                ngram = ' '.join(words[i:i+n])
                ngrams.append(ngram)
            
            return ngrams
        
        except Exception as e:
            print(f"Error extracting n-grams: {e}")
            return []
    
    def get_sentence_similarity_matrix(self, sentences):
        """Create similarity matrix for sentences."""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            
            # Preprocess sentences
            processed_sentences = [
                self.normalize_text(sent, remove_punct=True) 
                for sent in sentences
            ]
            
            # Create TF-IDF matrix
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(processed_sentences)
            
            # Calculate similarity matrix
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            return similarity_matrix
        
        except Exception as e:
            print(f"Error creating similarity matrix: {e}")
            return None
    
    def find_repeated_phrases(self, text, min_length=3, min_occurrences=2):
        """Find repeated phrases in text."""
        try:
            sentences = self.tokenize_sentences(text)
            repeated_phrases = []
            
            for sentence in sentences:
                words = self.tokenize_words(self.normalize_text(sentence))
                
                # Generate phrases of different lengths
                for phrase_length in range(min_length, min(len(words) + 1, 10)):
                    phrases = []
                    for i in range(len(words) - phrase_length + 1):
                        phrase = ' '.join(words[i:i+phrase_length])
                        phrases.append(phrase)
                    
                    # Count phrase occurrences
                    from collections import Counter
                    phrase_counts = Counter(phrases)
                    
                    for phrase, count in phrase_counts.items():
                        if count >= min_occurrences:
                            repeated_phrases.append({
                                'phrase': phrase,
                                'occurrences': count,
                                'length': phrase_length
                            })
            
            # Sort by number of occurrences
            repeated_phrases.sort(key=lambda x: x['occurrences'], reverse=True)
            
            return repeated_phrases
        
        except Exception as e:
            print(f"Error finding repeated phrases: {e}")
            return []
    
    def calculate_text_statistics(self, text):
        """Calculate comprehensive text statistics."""
        try:
            # Basic counts
            char_count = len(text)
            word_count = len(self.tokenize_words(text))
            sentence_count = len(self.tokenize_sentences(text))
            
            # Advanced statistics
            words = self.tokenize_words(self.normalize_text(text))
            unique_words = len(set(words))
            
            # Average lengths
            avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
            avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
            
            # Vocabulary richness
            vocabulary_richness = unique_words / word_count if word_count > 0 else 0
            
            return {
                'character_count': char_count,
                'word_count': word_count,
                'sentence_count': sentence_count,
                'unique_word_count': unique_words,
                'average_word_length': round(avg_word_length, 2),
                'average_sentence_length': round(avg_sentence_length, 2),
                'vocabulary_richness': round(vocabulary_richness, 3)
            }
        
        except Exception as e:
            print(f"Error calculating text statistics: {e}")
            return {}
    
    def preprocess_for_similarity(self, text):
        """Preprocess text for similarity comparison."""
        try:
            # Clean and normalize
            text = self.clean_text(text)
            text = self.normalize_text(text, lowercase=True, remove_punct=True)
            
            # Tokenize and remove stopwords
            words = self.tokenize_words(text)
            words = self.remove_stopwords(words)
            
            # Apply lemmatization
            words = self.lemmatize_words(words)
            
            return ' '.join(words)
        
        except Exception as e:
            print(f"Error preprocessing for similarity: {e}")
            return text