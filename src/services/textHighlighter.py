"""
Text Highlighter Service for plagiarism detection.
Highlights suspicious text passages and provides detailed analysis.
"""

import re
from typing import List, Dict, Tuple
from difflib import SequenceMatcher


class TextHighlighter:
    """Service for highlighting and analyzing suspicious text passages."""
    
    def __init__(self):
        """Initialize the text highlighter."""
        pass
    
    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences using a simple regex approach.
        Falls back to simple splitting if NLTK is not available.
        
        Args:
            text: Text to split into sentences
        
        Returns:
            List of sentences
        """
        try:
            # Try NLTK first
            from nltk.tokenize import sent_tokenize
            return sent_tokenize(text)
        except Exception:
            # Fallback to regex-based sentence splitting
            # Split on period, question mark, exclamation mark
            sentences = re.split(r'(?<=[.!?])\s+', text)
            # Filter out empty sentences
            sentences = [s.strip() for s in sentences if s.strip()]
            return sentences if sentences else [text]
    
    def highlight_suspicious_text(self, text1: str, text2: str, threshold: float = 0.7) -> Dict:
        """
        Highlight text passages from text1 that match text2 above threshold.
        
        Args:
            text1: Original text (the pasted content)
            text2: Reference text (uploaded document or comparison text)
            threshold: Similarity threshold for highlighting (0-1)
        
        Returns:
            Dictionary with highlighted text and analysis
        """
        try:
            sentences1 = self._split_sentences(text1)
            sentences2 = self._split_sentences(text2)
            
            # Find similar sentences
            similar_pairs = self._find_similar_sentences(sentences1, sentences2, threshold)
            
            # Create highlighted HTML
            highlighted_text = self._create_highlighted_text(text1, similar_pairs)
            
            # Generate summary
            summary = {
                'total_sentences': len(sentences1),
                'highlighted_sentences': len(similar_pairs),
                'plagiarism_percentage': (len(similar_pairs) / len(sentences1) * 100) if sentences1 else 0,
                'similarity_details': similar_pairs,
                'highlighted_html': highlighted_text
            }
            
            return summary
        
        except Exception as e:
            print(f"Error highlighting text: {e}")
            return {
                'error': str(e),
                'highlighted_html': text1,
                'similarity_details': []
            }
    
    def _find_similar_sentences(self, sentences1: List[str], sentences2: List[str], threshold: float) -> List[Dict]:
        """
        Find sentences from text1 that are similar to sentences in text2.
        
        Args:
            sentences1: List of sentences from original text
            sentences2: List of sentences from reference text
            threshold: Similarity threshold
        
        Returns:
            List of similar sentence pairs with their similarities
        """
        similar_pairs = []
        
        for i, sent1 in enumerate(sentences1):
            for j, sent2 in enumerate(sentences2):
                similarity = self._calculate_sentence_similarity(sent1, sent2)
                
                if similarity >= threshold:
                    similar_pairs.append({
                        'sentence': sent1,
                        'matched_sentence': sent2,
                        'similarity': round(similarity, 3),
                        'sentence_index': i,
                        'match_index': j
                    })
        
        # Remove duplicate highlighting (keep highest similarity)
        unique_pairs = {}
        for pair in similar_pairs:
            sent_idx = pair['sentence_index']
            if sent_idx not in unique_pairs or pair['similarity'] > unique_pairs[sent_idx]['similarity']:
                unique_pairs[sent_idx] = pair
        
        return list(unique_pairs.values())
    
    def _calculate_sentence_similarity(self, sent1: str, sent2: str) -> float:
        """
        Calculate similarity between two sentences using SequenceMatcher.
        
        Args:
            sent1: First sentence
            sent2: Second sentence
        
        Returns:
            Similarity score (0-1)
        """
        try:
            # Normalize text
            sent1_normalized = sent1.lower().strip()
            sent2_normalized = sent2.lower().strip()
            
            # Use SequenceMatcher for string similarity
            matcher = SequenceMatcher(None, sent1_normalized, sent2_normalized)
            similarity = matcher.ratio()
            
            return similarity
        
        except Exception as e:
            print(f"Error calculating sentence similarity: {e}")
            return 0.0
    
    def _create_highlighted_text(self, text: str, similar_pairs: List[Dict]) -> str:
        """
        Create HTML with highlighted suspicious passages.
        
        Args:
            text: Original text
            similar_pairs: List of similar sentence pairs
        
        Returns:
            HTML string with highlighted text
        """
        try:
            sentences = self._split_sentences(text)
            highlighted_sentences = {pair['sentence_index']: pair for pair in similar_pairs}
            
            html_parts = []
            html_parts.append('<div class="highlighted-text">')
            
            for i, sentence in enumerate(sentences):
                if i in highlighted_sentences:
                    pair = highlighted_sentences[i]
                    similarity_pct = int(pair['similarity'] * 100)
                    
                    # Color intensity based on similarity
                    if pair['similarity'] >= 0.95:
                        color_class = 'highlight-critical'  # Red
                    elif pair['similarity'] >= 0.85:
                        color_class = 'highlight-high'       # Orange
                    elif pair['similarity'] >= 0.75:
                        color_class = 'highlight-medium'     # Yellow
                    else:
                        color_class = 'highlight-low'        # Light yellow
                    
                    html_parts.append(
                        f'<span class="highlighted-sentence {color_class}" '
                        f'data-similarity="{pair["similarity"]}" '
                        f'title="Match: {similarity_pct}% - {pair["matched_sentence"][:50]}...">'
                        f'{sentence}</span> '
                    )
                else:
                    html_parts.append(f'<span class="normal-text">{sentence}</span> ')
            
            html_parts.append('</div>')
            
            return ''.join(html_parts)
        
        except Exception as e:
            print(f"Error creating highlighted text: {e}")
            return f'<div class="highlighted-text">{text}</div>'
    
    def highlight_passages(self, text: str, passages: List[str], case_sensitive: bool = False) -> str:
        """
        Highlight specific passages in text.
        
        Args:
            text: Text to highlight
            passages: List of passages to highlight
            case_sensitive: Whether to match case
        
        Returns:
            HTML string with highlighted passages
        """
        try:
            result = text
            
            for passage in passages:
                if case_sensitive:
                    pattern = re.escape(passage)
                else:
                    # Case-insensitive highlighting
                    pattern = re.escape(passage)
                    flags = re.IGNORECASE
                    result = re.sub(
                        pattern,
                        f'<mark class="passage-highlight">{passage}</mark>',
                        result,
                        flags=flags
                    )
                    continue
                
                result = re.sub(
                    pattern,
                    f'<mark class="passage-highlight">{passage}</mark>',
                    result
                )
            
            return result
        
        except Exception as e:
            print(f"Error highlighting passages: {e}")
            return text
    
    def get_highlight_statistics(self, highlighted_data: Dict) -> Dict:
        """
        Get statistics about highlighted text.
        
        Args:
            highlighted_data: Highlighted text data from highlight_suspicious_text
        
        Returns:
            Dictionary with statistics
        """
        try:
            similarity_scores = [pair['similarity'] for pair in highlighted_data.get('similarity_details', [])]
            
            if not similarity_scores:
                return {
                    'total_highlighted': 0,
                    'average_similarity': 0,
                    'max_similarity': 0,
                    'min_similarity': 0,
                    'high_similarity_count': 0,
                    'medium_similarity_count': 0,
                    'low_similarity_count': 0
                }
            
            return {
                'total_highlighted': len(similarity_scores),
                'average_similarity': round(sum(similarity_scores) / len(similarity_scores), 3),
                'max_similarity': round(max(similarity_scores), 3),
                'min_similarity': round(min(similarity_scores), 3),
                'high_similarity_count': len([s for s in similarity_scores if s >= 0.9]),
                'medium_similarity_count': len([s for s in similarity_scores if 0.8 <= s < 0.9]),
                'low_similarity_count': len([s for s in similarity_scores if s < 0.8])
            }
        
        except Exception as e:
            print(f"Error calculating highlight statistics: {e}")
            return {}
