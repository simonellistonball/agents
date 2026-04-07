"""Writing improvement module for MCP tools."""

import re
from typing import List, Tuple, Dict
from .analyzer import WritingAnalyzer


class WritingImprover:
    """Improves text based on clarity, readability, and evidence principles."""
    
    def __init__(self):
        self.analyzer = WritingAnalyzer()
        
        # Mapping of complex words to simpler alternatives
        self.simplifications = {
            "utilize": "use",
            "implement": "put in place",
            "facilitate": "help",
            "leverage": "use",
            "optimize": "improve",
            "enhance": "improve",
            "methodology": "method",
            "framework": "structure",
            "paradigm": "model",
            "synergize": "work together",
            "aforementioned": "mentioned",
            "subsequently": "then",
            "consequently": "so",
            "furthermore": "also",
            "notwithstanding": "despite",
            "nevertheless": "however",
            "therefore": "so",
            "accordingly": "so"
        }
        
        # Vague phrases to replace
        self.vague_replacements = {
            "might potentially": "may",
            "could possibly": "may",
            "it is believed that": "",
            "it seems that": "",
            "appears to be": "is",
            "tends to": "often",
            "in order to": "to",
            "due to the fact that": "because",
            "in the event that": "if",
            "at this point in time": "now",
            "in the near future": "soon",
            "for the purpose of": "to",
            "with regard to": "about",
            "in connection with": "about"
        }
    
    def improve(self, text: str, target_flesch_score: int = 60) -> Dict:
        """Improve the text and return both improved version and changes made."""
        if not text or not text.strip():
            return {"error": "Empty or invalid text provided"}
        
        try:
            # Analyze original text
            original_analysis = self.analyzer.analyze(text)
            if "error" in original_analysis:
                return original_analysis
            
            # Apply improvements
            improved_text = text
            changes_made = []
            
            # 1. Simplify language
            improved_text, simplification_changes = self._simplify_language(improved_text)
            changes_made.extend(simplification_changes)
            
            # 2. Remove vague phrases
            improved_text, vague_changes = self._remove_vague_phrases(improved_text)
            changes_made.extend(vague_changes)
            
            # 3. Convert passive to active voice (conservative approach)
            improved_text, voice_changes = self._convert_passive_to_active(improved_text)
            changes_made.extend(voice_changes)
            
            # 4. Break up complex sentences
            improved_text, sentence_changes = self._simplify_sentences(improved_text)
            changes_made.extend(sentence_changes)
            
            # 5. Improve paragraph structure
            improved_text, structure_changes = self._improve_structure(improved_text)
            changes_made.extend(structure_changes)
            
            # 6. Mark unsupported claims that need evidence
            improved_text, evidence_changes = self._mark_unsupported_claims(improved_text)
            changes_made.extend(evidence_changes)
            
            # Analyze improved text
            improved_analysis = self.analyzer.analyze(improved_text)
            if "error" in improved_analysis:
                return {"error": f"Analysis of improved text failed: {improved_analysis['error']}"}
            
            return {
                "original_text": text,
                "improved_text": improved_text,
                "changes_made": changes_made,
                "changes_count": len(changes_made),
                "metrics": {
                    "original": {
                        "flesch_score": original_analysis["readability"]["flesch_reading_ease"],
                        "grade_level": original_analysis["readability"]["flesch_kincaid_grade"],
                        "word_count": len(text.split()),
                        "sentence_count": original_analysis["structure"]["sentence_count"],
                        "passive_voice_percentage": original_analysis["clarity"]["passive_voice_percentage"],
                        "overall_score": original_analysis["overall_score"]
                    },
                    "improved": {
                        "flesch_score": improved_analysis["readability"]["flesch_reading_ease"],
                        "grade_level": improved_analysis["readability"]["flesch_kincaid_grade"],
                        "word_count": len(improved_text.split()),
                        "sentence_count": improved_analysis["structure"]["sentence_count"],
                        "passive_voice_percentage": improved_analysis["clarity"]["passive_voice_percentage"],
                        "overall_score": improved_analysis["overall_score"]
                    },
                    "improvements": {
                        "flesch_score_change": round(improved_analysis["readability"]["flesch_reading_ease"] - original_analysis["readability"]["flesch_reading_ease"], 1),
                        "grade_level_change": round(improved_analysis["readability"]["flesch_kincaid_grade"] - original_analysis["readability"]["flesch_kincaid_grade"], 1),
                        "passive_voice_reduction": round(original_analysis["clarity"]["passive_voice_percentage"] - improved_analysis["clarity"]["passive_voice_percentage"], 1),
                        "overall_score_change": improved_analysis["overall_score"] - original_analysis["overall_score"]
                    }
                },
                "success": True
            }
            
        except Exception as e:
            return {"error": f"Improvement failed: {str(e)}"}
    
    def _simplify_language(self, text: str) -> Tuple[str, List[str]]:
        """Replace complex words with simpler alternatives."""
        changes = []
        improved = text
        
        for complex_word, simple_word in self.simplifications.items():
            pattern = r'\b' + re.escape(complex_word) + r'\b'
            matches = re.findall(pattern, improved, re.IGNORECASE)
            
            if matches:
                improved = re.sub(pattern, simple_word, improved, flags=re.IGNORECASE)
                changes.append(f"Simplified '{complex_word}' → '{simple_word}' ({len(matches)} instances)")
        
        return improved, changes
    
    def _remove_vague_phrases(self, text: str) -> Tuple[str, List[str]]:
        """Remove or replace vague phrases."""
        changes = []
        improved = text
        
        for vague_phrase, replacement in self.vague_replacements.items():
            pattern = re.escape(vague_phrase)
            matches = re.findall(pattern, improved, re.IGNORECASE)
            
            if matches:
                improved = re.sub(pattern, replacement, improved, flags=re.IGNORECASE)
                action = "removed" if not replacement else f"replaced with '{replacement}'"
                changes.append(f"Vague phrase '{vague_phrase}' {action} ({len(matches)} instances)")
        
        # Clean up extra spaces
        improved = re.sub(r'\s+', ' ', improved)
        improved = re.sub(r'\s+([,.!?])', r'\1', improved)
        
        return improved, changes
    
    def _convert_passive_to_active(self, text: str) -> Tuple[str, List[str]]:
        """Convert simple passive voice constructions to active voice."""
        changes = []
        sentences = self._split_into_sentences(text)
        improved_sentences = []
        
        for sentence in sentences:
            # Look for simple passive constructions with "by" clause
            passive_pattern = r'(\w+)\s+(was|were|is|are)\s+(\w+ed|given|shown|made|done)\s+by\s+(\w+(?:\s+\w+)*)'
            match = re.search(passive_pattern, sentence, re.IGNORECASE)
            
            if match and len(sentence.split()) < 20:  # Only convert shorter sentences
                object_word = match.group(1)
                tense = match.group(2).lower()
                past_participle = match.group(3)
                subject = match.group(4)
                
                # Simple conversion for common cases
                if past_participle.endswith('ed'):
                    verb_base = past_participle[:-2]
                    if tense in ['was', 'were']:
                        active_verb = verb_base + 'ed'
                    else:
                        active_verb = verb_base + 's' if subject.lower() not in ['they', 'we', 'you'] else verb_base
                    
                    # Construct active sentence
                    before_match = sentence[:match.start()]
                    after_match = sentence[match.end():]
                    active_sentence = f"{before_match}{subject} {active_verb} {object_word}{after_match}".strip()
                    
                    improved_sentences.append(active_sentence)
                    changes.append(f"Converted passive to active voice: '{sentence[:50]}...'")
                else:
                    improved_sentences.append(sentence)
            else:
                improved_sentences.append(sentence)
        
        return ' '.join(improved_sentences), changes
    
    def _simplify_sentences(self, text: str) -> Tuple[str, List[str]]:
        """Break up overly complex sentences."""
        changes = []
        sentences = self._split_into_sentences(text)
        improved_sentences = []
        
        for sentence in sentences:
            words = sentence.split()
            
            # If sentence is very long, try to split it
            if len(words) > 30:
                # Look for good split points
                split_conjunctions = ['however', 'therefore', 'moreover', 'furthermore', 'additionally', 'nevertheless']
                split_phrases = [', which', ', and', ', but']
                
                split_point = None
                split_word = None
                
                # Try conjunctions first
                for i, word in enumerate(words):
                    if word.lower() in split_conjunctions and i > 8:  # Don't split too early
                        split_point = i
                        split_word = word
                        break
                
                # Try phrases if no conjunction found
                if not split_point:
                    for phrase in split_phrases:
                        phrase_index = sentence.lower().find(phrase)
                        if phrase_index > 50:  # Don't split too early
                            word_index = len(sentence[:phrase_index].split())
                            if word_index > 8:
                                split_point = word_index
                                split_word = phrase
                                break
                
                if split_point:
                    first_part = ' '.join(words[:split_point]).rstrip('.,')
                    second_part = ' '.join(words[split_point:])
                    
                    # Ensure both parts are complete sentences
                    if not first_part.endswith('.'):
                        first_part += '.'
                    
                    # Capitalize second part if needed
                    if second_part and not second_part[0].isupper():
                        second_part = second_part[0].upper() + second_part[1:]
                    
                    improved_sentences.extend([first_part, second_part])
                    changes.append(f"Split long sentence ({len(words)} words) at '{split_word}'")
                else:
                    improved_sentences.append(sentence)
            else:
                improved_sentences.append(sentence)
        
        return ' '.join(improved_sentences), changes
    
    def _improve_structure(self, text: str) -> Tuple[str, List[str]]:
        """Improve paragraph structure for better readability."""
        changes = []
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        improved_paragraphs = []
        
        for i, paragraph in enumerate(paragraphs):
            sentences = self._split_into_sentences(paragraph)
            
            # Split paragraphs that are too long
            if len(sentences) > 7:
                # Find a good split point around the middle
                mid_point = len(sentences) // 2
                
                # Adjust split point to avoid splitting related sentences
                # Look for transition words that indicate a new topic
                transition_indicators = ['however', 'furthermore', 'additionally', 'moreover', 'on the other hand']
                
                for j in range(mid_point - 1, min(mid_point + 2, len(sentences))):
                    sentence_start = sentences[j].lower().split()[:3]
                    if any(word in sentence_start for word in transition_indicators):
                        mid_point = j
                        break
                
                first_para = ' '.join(sentences[:mid_point])
                second_para = ' '.join(sentences[mid_point:])
                
                improved_paragraphs.extend([first_para, second_para])
                changes.append(f"Split paragraph {i+1} ({len(sentences)} sentences) for better readability")
            else:
                improved_paragraphs.append(paragraph)
        
        return '\n\n'.join(improved_paragraphs), changes
    
    def _mark_unsupported_claims(self, text: str) -> Tuple[str, List[str]]:
        """Mark claims that need supporting evidence."""
        changes = []
        sentences = self._split_into_sentences(text)
        improved_sentences = []
        
        claim_patterns = [
            r'\b(significantly improves|dramatically increases|substantially decreases)\b',
            r'\b(always|never|all|none|every|completely|entirely)\b',
            r'\b(causes|leads to|results in|proves that)\b'
        ]
        
        evidence_patterns = [
            r'\b(research shows|studies indicate|data suggests|according to)\b',
            r'\b\d+%\b',
            r'\([^)]+\d{4}[^)]*\)',
            r'\b(source:|ref:|see:)\b'
        ]
        
        for sentence in sentences:
            has_strong_claim = any(re.search(pattern, sentence, re.I) for pattern in claim_patterns)
            has_evidence = any(re.search(pattern, sentence, re.I) for pattern in evidence_patterns)
            
            if has_strong_claim and not has_evidence and len(sentence) > 30:
                # Only mark substantial claims, not brief statements
                improved_sentence = sentence.rstrip('.') + " [Citation needed]."
                improved_sentences.append(improved_sentence)
                changes.append(f"Marked unsupported claim: '{sentence[:50]}...'")
            else:
                improved_sentences.append(sentence)
        
        return ' '.join(improved_sentences), changes
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences while preserving structure."""
        # More sophisticated sentence splitting that preserves meaning
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        return [s.strip() for s in sentences if s.strip()]