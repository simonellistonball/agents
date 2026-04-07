"""Writing quality analysis module for MCP tools."""

import re
from typing import Dict, List, Optional

try:
    import textstat
    TEXTSTAT_AVAILABLE = True
except ImportError:
    TEXTSTAT_AVAILABLE = False


class WritingAnalyzer:
    """Analyzes text for clarity, readability, and quality issues."""
    
    def __init__(self):
        self.vague_phrases = [
            "might", "could", "possibly", "potentially", "somewhat",
            "arguably", "it is believed", "it seems", "appears to",
            "tends to", "generally", "usually", "often", "sometimes",
            "fairly", "quite", "rather", "very", "really"
        ]
        
        self.jargon_indicators = [
            "utilize", "leverage", "synergize", "paradigm", "framework",
            "methodology", "implementation", "optimization", "enhance",
            "facilitate", "enable", "empower", "streamline", "aforementioned"
        ]
        
        self.weak_verbs = ["is", "are", "was", "were", "been", "being", "be"]
        
    def analyze(self, text: str) -> Dict:
        """Perform comprehensive analysis of the text."""
        if not text or not text.strip():
            return {"error": "Empty or invalid text provided"}
        
        try:
            results = {
                "readability": self._analyze_readability(text),
                "clarity": self._analyze_clarity(text),
                "structure": self._analyze_structure(text),
                "evidence": self._analyze_evidence(text),
                "grammar": self._analyze_grammar(text),
                "recommendations": [],
                "overall_score": 0
            }
            
            results["recommendations"] = self._generate_recommendations(results)
            results["overall_score"] = self._calculate_overall_score(results)
            
            return results
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_readability(self, text: str) -> Dict:
        """Calculate readability metrics."""
        if not TEXTSTAT_AVAILABLE:
            # Fallback metrics without textstat
            sentences = self._split_sentences(text)
            words = text.split()
            
            avg_sentence_length = len(words) / len(sentences) if sentences else 0
            long_words = [w for w in words if len(w) > 6]
            
            # Simple readability estimate
            complexity_score = (avg_sentence_length * 0.4) + (len(long_words) / len(words) * 100 * 0.6)
            flesch_estimate = max(0, min(100, 100 - complexity_score))
            
            return {
                "flesch_reading_ease": round(flesch_estimate, 1),
                "flesch_kincaid_grade": round(complexity_score / 10, 1),
                "avg_sentence_length": round(avg_sentence_length, 1),
                "difficult_words": len(long_words),
                "reading_time_seconds": len(text) * 0.2,  # Rough estimate
                "textstat_available": False
            }
        
        return {
            "flesch_reading_ease": round(textstat.flesch_reading_ease(text), 1),
            "flesch_kincaid_grade": round(textstat.flesch_kincaid_grade(text), 1),
            "gunning_fog": round(textstat.gunning_fog(text), 1),
            "avg_sentence_length": round(textstat.avg_sentence_length(text), 1),
            "avg_syllables_per_word": round(textstat.avg_syllables_per_word(text), 2),
            "difficult_words": textstat.difficult_words(text),
            "reading_time_seconds": round(textstat.reading_time(text, ms_per_char=14.69), 0),
            "textstat_available": True
        }
    
    def _analyze_clarity(self, text: str) -> Dict:
        """Analyze clarity issues in the text."""
        sentences = self._split_sentences(text)
        words = text.lower().split()
        
        vague_count = sum(1 for word in words if any(phrase in text.lower() for phrase in self.vague_phrases if phrase == word))
        jargon_count = sum(1 for word in words if word in self.jargon_indicators)
        
        passive_sentences = self._detect_passive_voice(sentences)
        complex_sentences = [s for s in sentences if len(s.split()) > 25]
        
        return {
            "vague_phrases_count": vague_count,
            "vague_phrases_percentage": round((vague_count / len(words) * 100) if words else 0, 1),
            "jargon_count": jargon_count,
            "jargon_percentage": round((jargon_count / len(words) * 100) if words else 0, 1),
            "passive_voice_count": len(passive_sentences),
            "passive_voice_percentage": round((len(passive_sentences) / len(sentences) * 100) if sentences else 0, 1),
            "complex_sentences_count": len(complex_sentences),
            "avg_words_per_sentence": round(sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0, 1),
            "passive_sentences": passive_sentences[:3]  # First 3 examples
        }
    
    def _analyze_structure(self, text: str) -> Dict:
        """Analyze the structural elements of the text."""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        sentences = self._split_sentences(text)
        
        # Analyze transitions
        transition_words = [
            "however", "therefore", "furthermore", "moreover", "consequently",
            "additionally", "nevertheless", "thus", "hence", "accordingly",
            "first", "second", "third", "finally", "next", "then"
        ]
        
        transition_count = sum(1 for word in text.lower().split() if word.rstrip('.,!?') in transition_words)
        
        return {
            "paragraph_count": len(paragraphs),
            "sentence_count": len(sentences),
            "avg_sentences_per_paragraph": round(len(sentences) / len(paragraphs) if paragraphs else 0, 1),
            "transition_words_count": transition_count,
            "has_clear_introduction": self._has_clear_introduction(paragraphs),
            "has_clear_conclusion": self._has_clear_conclusion(paragraphs),
            "longest_paragraph_sentences": max(len(self._split_sentences(p)) for p in paragraphs) if paragraphs else 0
        }
    
    def _analyze_evidence(self, text: str) -> Dict:
        """Analyze evidence and support for claims."""
        sentences = self._split_sentences(text)
        
        # Look for assertion patterns
        assertion_patterns = [
            r'\b(research shows|studies indicate|data suggests|evidence demonstrates)\b',
            r'\b(according to|as reported by|as stated in)\b',
            r'\b\d+%\b',  # Percentages
            r'\b\d+\s*(million|billion|thousand)\b',  # Numbers with scale
            r'\([^)]+\d{4}[^)]*\)',  # Citations with years
        ]
        
        evidence_sentences = []
        unsupported_claims = []
        
        for sentence in sentences:
            has_evidence = any(re.search(pattern, sentence, re.I) for pattern in assertion_patterns)
            
            # Check if sentence makes a claim
            claim_patterns = [
                r'\b(improves|increases|decreases|causes|leads to|results in)\b',
                r'\b(better|worse|more|less|higher|lower) than\b',
                r'\b(always|never|all|none|every)\b'
            ]
            
            has_claim = any(re.search(pattern, sentence, re.I) for pattern in claim_patterns)
            
            if has_evidence:
                evidence_sentences.append(sentence[:100] + "..." if len(sentence) > 100 else sentence)
            elif has_claim:
                unsupported_claims.append(sentence[:100] + "..." if len(sentence) > 100 else sentence)
        
        return {
            "evidence_sentences_count": len(evidence_sentences),
            "unsupported_claims_count": len(unsupported_claims),
            "evidence_ratio": round(len(evidence_sentences) / len(sentences) if sentences else 0, 2),
            "contains_statistics": bool(re.search(r'\b\d+%\b|\b\d+\s*(million|billion)', text)),
            "contains_citations": bool(re.search(r'\([^)]+\d{4}[^)]*\)', text)),
            "unsupported_claims_examples": unsupported_claims[:3],  # First 3 examples
            "evidence_examples": evidence_sentences[:3]  # First 3 examples
        }
    
    def _analyze_grammar(self, text: str) -> Dict:
        """Basic grammar analysis."""
        sentences = self._split_sentences(text)
        
        issues = {
            "sentence_fragments": 0,
            "run_on_sentences": 0,
            "potential_issues": []
        }
        
        for sentence in sentences:
            words = sentence.split()
            
            # Detect potential sentence fragments
            if len(words) < 4 and not any(verb in sentence.lower() for verb in self.weak_verbs):
                issues["sentence_fragments"] += 1
                issues["potential_issues"].append(f"Fragment: {sentence[:50]}...")
            
            # Detect potential run-on sentences
            if len(words) > 35 and sentence.count(',') > 4:
                issues["run_on_sentences"] += 1
                issues["potential_issues"].append(f"Run-on: {sentence[:50]}...")
        
        return issues
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _detect_passive_voice(self, sentences: List[str]) -> List[str]:
        """Detect sentences with passive voice."""
        passive_sentences = []
        passive_indicators = [
            r'\b(was|were|been|being|is|are|am)\s+\w+ed\b',
            r'\b(was|were|been|being|is|are|am)\s+\w+en\b'
        ]
        
        for sentence in sentences:
            if any(re.search(pattern, sentence, re.I) for pattern in passive_indicators):
                passive_sentences.append(sentence[:100] + "..." if len(sentence) > 100 else sentence)
        
        return passive_sentences
    
    def _has_clear_introduction(self, paragraphs: List[str]) -> bool:
        """Check if text has a clear introduction."""
        if not paragraphs:
            return False
        
        intro = paragraphs[0].lower()
        intro_patterns = [
            r'\b(this article|this paper|this document|we will|i will)\b',
            r'\b(introduction|overview|purpose|objective)\b',
            r'\b(explore|examine|discuss|analyze|present)\b'
        ]
        
        return any(re.search(pattern, intro) for pattern in intro_patterns)
    
    def _has_clear_conclusion(self, paragraphs: List[str]) -> bool:
        """Check if text has a clear conclusion."""
        if not paragraphs:
            return False
        
        conclusion = paragraphs[-1].lower()
        conclusion_patterns = [
            r'\b(in conclusion|to conclude|in summary|to summarize)\b',
            r'\b(therefore|thus|hence|consequently)\b',
            r'\b(demonstrates|shows|proves|indicates)\b'
        ]
        
        return any(re.search(pattern, conclusion) for pattern in conclusion_patterns)
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate specific recommendations based on analysis."""
        recommendations = []
        
        # Readability recommendations
        flesch_score = analysis["readability"]["flesch_reading_ease"]
        if flesch_score < 50:
            recommendations.append("Text is too difficult (Flesch < 50). Simplify sentences and use shorter words.")
        elif flesch_score > 70:
            recommendations.append("Text might be too simple for professional content (Flesch > 70).")
        
        # Clarity recommendations
        if analysis["clarity"]["passive_voice_percentage"] > 20:
            recommendations.append(f"Reduce passive voice usage (currently {analysis['clarity']['passive_voice_percentage']}%)")
        
        if analysis["clarity"]["vague_phrases_percentage"] > 5:
            recommendations.append(f"Replace vague phrases with specific language ({analysis['clarity']['vague_phrases_count']} found)")
        
        if analysis["clarity"]["jargon_count"] > 10:
            recommendations.append(f"Consider replacing jargon with plain language ({analysis['clarity']['jargon_count']} instances)")
        
        # Structure recommendations
        if analysis["structure"]["avg_sentences_per_paragraph"] > 6:
            recommendations.append("Break up long paragraphs for better readability")
        
        if analysis["structure"]["transition_words_count"] < 3:
            recommendations.append("Add transition words to improve flow")
        
        # Evidence recommendations
        if analysis["evidence"]["unsupported_claims_count"] > 3:
            recommendations.append(f"Add evidence to support {analysis['evidence']['unsupported_claims_count']} unsupported claims")
        
        if not analysis["evidence"]["contains_statistics"]:
            recommendations.append("Consider adding statistics or data to strengthen arguments")
        
        return recommendations
    
    def _calculate_overall_score(self, analysis: Dict) -> int:
        """Calculate an overall writing quality score (0-100)."""
        score = 100
        
        # Readability penalty
        flesch_score = analysis["readability"]["flesch_reading_ease"]
        if flesch_score < 30 or flesch_score > 80:
            score -= 15
        elif flesch_score < 50 or flesch_score > 70:
            score -= 5
        
        # Clarity penalties
        score -= min(20, analysis["clarity"]["passive_voice_percentage"])
        score -= min(10, analysis["clarity"]["vague_phrases_percentage"] * 2)
        score -= min(10, analysis["clarity"]["jargon_percentage"])
        
        # Structure penalties
        if analysis["structure"]["avg_sentences_per_paragraph"] > 7:
            score -= 10
        if analysis["structure"]["transition_words_count"] == 0:
            score -= 5
        
        # Evidence penalties
        if analysis["evidence"]["unsupported_claims_count"] > 5:
            score -= 15
        elif analysis["evidence"]["unsupported_claims_count"] > 2:
            score -= 8
        
        return max(0, min(100, round(score)))