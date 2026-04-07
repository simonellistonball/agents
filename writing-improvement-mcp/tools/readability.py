"""Reading quality and readability metrics module for MCP tools."""

import re
import math
from typing import Dict, List, Tuple

try:
    import textstat
    TEXTSTAT_AVAILABLE = True
except ImportError:
    TEXTSTAT_AVAILABLE = False


class ReadabilityAnalyzer:
    """Specialized analyzer for reading quality metrics and readability scoring."""
    
    def __init__(self):
        # Common syllable patterns for syllable counting
        self.vowel_groups = re.compile(r'[aeiouyAEIOUY]+')
        self.ending_e = re.compile(r'[^aeiouAEIOUY]e\b')
        self.ending_le = re.compile(r'[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]le\b')
        
        # Reading speed constants (words per minute)
        self.reading_speeds = {
            'elementary': 150,      # Elementary school
            'middle_school': 175,   # Middle school  
            'high_school': 200,     # High school
            'college': 250,         # College level
            'graduate': 300,        # Graduate level
            'professional': 350     # Professional/speed reading
        }
        
    def comprehensive_readability_analysis(self, text: str) -> Dict:
        """Perform comprehensive readability analysis with multiple metrics."""
        if not text or not text.strip():
            return {"error": "Empty or invalid text provided"}
        
        try:
            # Basic text statistics
            basic_stats = self._calculate_basic_stats(text)
            
            # Readability scores
            readability_scores = self._calculate_readability_scores(text, basic_stats)
            
            # Reading time estimates
            reading_times = self._calculate_reading_times(basic_stats['word_count'])
            
            # Sentence complexity analysis
            complexity_analysis = self._analyze_sentence_complexity(text)
            
            # Vocabulary analysis
            vocabulary_analysis = self._analyze_vocabulary(text)
            
            # Overall assessment
            overall_assessment = self._assess_readability(readability_scores, complexity_analysis)
            
            return {
                "basic_stats": basic_stats,
                "readability_scores": readability_scores,
                "reading_times": reading_times,
                "complexity_analysis": complexity_analysis,
                "vocabulary_analysis": vocabulary_analysis,
                "overall_assessment": overall_assessment,
                "textstat_available": TEXTSTAT_AVAILABLE
            }
            
        except Exception as e:
            return {"error": f"Readability analysis failed: {str(e)}"}
    
    def flesch_reading_ease_detailed(self, text: str) -> Dict:
        """Detailed Flesch Reading Ease analysis with interpretation."""
        if not text or not text.strip():
            return {"error": "Empty or invalid text provided"}
        
        try:
            basic_stats = self._calculate_basic_stats(text)
            
            if TEXTSTAT_AVAILABLE:
                flesch_score = textstat.flesch_reading_ease(text)
            else:
                # Manual calculation: 206.835 - (1.015 × ASL) - (84.6 × ASW)
                asl = basic_stats['avg_sentence_length']
                asw = basic_stats['avg_syllables_per_word']
                flesch_score = 206.835 - (1.015 * asl) - (84.6 * asw)
            
            # Interpret the score
            interpretation = self._interpret_flesch_score(flesch_score)
            
            # Recommendations for improvement
            recommendations = self._flesch_score_recommendations(flesch_score, basic_stats)
            
            return {
                "flesch_reading_ease": round(flesch_score, 1),
                "interpretation": interpretation,
                "target_range": "50-70 (standard adult reading level)",
                "basic_stats": basic_stats,
                "recommendations": recommendations,
                "score_breakdown": {
                    "base_score": 206.835,
                    "sentence_length_penalty": round(1.015 * basic_stats['avg_sentence_length'], 2),
                    "syllable_complexity_penalty": round(84.6 * basic_stats['avg_syllables_per_word'], 2)
                }
            }
            
        except Exception as e:
            return {"error": f"Flesch Reading Ease analysis failed: {str(e)}"}
    
    def grade_level_analysis(self, text: str) -> Dict:
        """Comprehensive grade level analysis using multiple formulas."""
        if not text or not text.strip():
            return {"error": "Empty or invalid text provided"}
        
        try:
            basic_stats = self._calculate_basic_stats(text)
            grade_levels = {}
            
            if TEXTSTAT_AVAILABLE:
                grade_levels = {
                    "flesch_kincaid": textstat.flesch_kincaid_grade(text),
                    "gunning_fog": textstat.gunning_fog(text),
                    "smog": textstat.smog_index(text),
                    "automated_readability": textstat.automated_readability_index(text),
                    "coleman_liau": textstat.coleman_liau_index(text),
                    "linsear_write": textstat.linsear_write_formula(text)
                }
            else:
                # Manual calculations for key metrics
                grade_levels = {
                    "flesch_kincaid": self._calculate_flesch_kincaid(basic_stats),
                    "gunning_fog": self._calculate_gunning_fog(text, basic_stats),
                    "automated_readability": self._calculate_ari(basic_stats)
                }
            
            # Calculate average and consensus
            valid_scores = [score for score in grade_levels.values() if isinstance(score, (int, float)) and score > 0]
            average_grade = sum(valid_scores) / len(valid_scores) if valid_scores else 0
            
            # Interpret grade levels
            interpretation = self._interpret_grade_level(average_grade)
            
            return {
                "grade_levels": {k: round(v, 1) if isinstance(v, (int, float)) else v for k, v in grade_levels.items()},
                "average_grade_level": round(average_grade, 1),
                "interpretation": interpretation,
                "target_grade_level": "8-12 (high school level)",
                "basic_stats": basic_stats,
                "recommendations": self._grade_level_recommendations(average_grade, basic_stats)
            }
            
        except Exception as e:
            return {"error": f"Grade level analysis failed: {str(e)}"}
    
    def reading_time_analysis(self, text: str) -> Dict:
        """Detailed reading time analysis for different skill levels."""
        if not text or not text.strip():
            return {"error": "Empty or invalid text provided"}
        
        try:
            basic_stats = self._calculate_basic_stats(text)
            word_count = basic_stats['word_count']
            
            # Calculate reading times for different levels
            reading_times = {}
            for level, wpm in self.reading_speeds.items():
                time_minutes = word_count / wpm
                reading_times[level] = {
                    "minutes": round(time_minutes, 1),
                    "seconds": round(time_minutes * 60, 0),
                    "words_per_minute": wpm
                }
            
            # Average reading time (college level)
            avg_time = reading_times['college']['minutes']
            
            # Reading difficulty assessment
            difficulty = self._assess_reading_difficulty(basic_stats)
            
            return {
                "word_count": word_count,
                "reading_times_by_level": reading_times,
                "average_reading_time": f"{avg_time} minutes",
                "difficulty_assessment": difficulty,
                "basic_stats": basic_stats,
                "recommendations": self._reading_time_recommendations(avg_time, difficulty)
            }
            
        except Exception as e:
            return {"error": f"Reading time analysis failed: {str(e)}"}
    
    def sentence_complexity_analysis(self, text: str) -> Dict:
        """Detailed analysis of sentence complexity and structure."""
        if not text or not text.strip():
            return {"error": "Empty or invalid text provided"}
        
        try:
            sentences = self._split_sentences(text)
            
            complexity_metrics = {
                "total_sentences": len(sentences),
                "sentence_lengths": [],
                "complexity_distribution": {
                    "simple": 0,      # < 15 words
                    "moderate": 0,    # 15-25 words
                    "complex": 0,     # 25-35 words
                    "very_complex": 0 # > 35 words
                },
                "structural_analysis": {
                    "questions": 0,
                    "exclamations": 0,
                    "compound_sentences": 0,
                    "sentences_with_commas": 0,
                    "sentences_with_semicolons": 0
                }
            }
            
            for sentence in sentences:
                words = sentence.split()
                word_count = len(words)
                complexity_metrics["sentence_lengths"].append(word_count)
                
                # Categorize by complexity
                if word_count < 15:
                    complexity_metrics["complexity_distribution"]["simple"] += 1
                elif word_count < 25:
                    complexity_metrics["complexity_distribution"]["moderate"] += 1
                elif word_count < 35:
                    complexity_metrics["complexity_distribution"]["complex"] += 1
                else:
                    complexity_metrics["complexity_distribution"]["very_complex"] += 1
                
                # Structural analysis
                if '?' in sentence:
                    complexity_metrics["structural_analysis"]["questions"] += 1
                if '!' in sentence:
                    complexity_metrics["structural_analysis"]["exclamations"] += 1
                if ' and ' in sentence.lower() or ' but ' in sentence.lower() or ' or ' in sentence.lower():
                    complexity_metrics["structural_analysis"]["compound_sentences"] += 1
                if ',' in sentence:
                    complexity_metrics["structural_analysis"]["sentences_with_commas"] += 1
                if ';' in sentence:
                    complexity_metrics["structural_analysis"]["sentences_with_semicolons"] += 1
            
            # Calculate statistics
            if complexity_metrics["sentence_lengths"]:
                complexity_metrics["average_sentence_length"] = round(sum(complexity_metrics["sentence_lengths"]) / len(complexity_metrics["sentence_lengths"]), 1)
                complexity_metrics["min_sentence_length"] = min(complexity_metrics["sentence_lengths"])
                complexity_metrics["max_sentence_length"] = max(complexity_metrics["sentence_lengths"])
                
                # Calculate percentages
                total = complexity_metrics["total_sentences"]
                for category in complexity_metrics["complexity_distribution"]:
                    count = complexity_metrics["complexity_distribution"][category]
                    complexity_metrics["complexity_distribution"][category] = {
                        "count": count,
                        "percentage": round((count / total) * 100, 1)
                    }
            
            # Assessment and recommendations
            assessment = self._assess_sentence_complexity(complexity_metrics)
            
            return {
                "complexity_metrics": complexity_metrics,
                "assessment": assessment,
                "recommendations": self._sentence_complexity_recommendations(complexity_metrics)
            }
            
        except Exception as e:
            return {"error": f"Sentence complexity analysis failed: {str(e)}"}
    
    # Helper methods
    def _calculate_basic_stats(self, text: str) -> Dict:
        """Calculate basic text statistics."""
        sentences = self._split_sentences(text)
        words = text.split()
        characters = len(re.sub(r'\s', '', text))
        
        # Syllable counting
        total_syllables = sum(self._count_syllables(word) for word in words)
        
        return {
            "character_count": len(text),
            "character_count_no_spaces": characters,
            "word_count": len(words),
            "sentence_count": len(sentences),
            "syllable_count": total_syllables,
            "avg_sentence_length": round(len(words) / len(sentences) if sentences else 0, 1),
            "avg_word_length": round(characters / len(words) if words else 0, 1),
            "avg_syllables_per_word": round(total_syllables / len(words) if words else 0, 2)
        }
    
    def _calculate_readability_scores(self, text: str, basic_stats: Dict) -> Dict:
        """Calculate various readability scores."""
        scores = {}
        
        if TEXTSTAT_AVAILABLE:
            scores = {
                "flesch_reading_ease": round(textstat.flesch_reading_ease(text), 1),
                "flesch_kincaid_grade": round(textstat.flesch_kincaid_grade(text), 1),
                "gunning_fog": round(textstat.gunning_fog(text), 1),
                "smog_index": round(textstat.smog_index(text), 1),
                "automated_readability_index": round(textstat.automated_readability_index(text), 1),
                "coleman_liau_index": round(textstat.coleman_liau_index(text), 1)
            }
        else:
            # Manual calculations
            asl = basic_stats['avg_sentence_length']
            asw = basic_stats['avg_syllables_per_word']
            
            scores = {
                "flesch_reading_ease": round(206.835 - (1.015 * asl) - (84.6 * asw), 1),
                "flesch_kincaid_grade": round((0.39 * asl) + (11.8 * asw) - 15.59, 1),
                "automated_readability_index": round((4.71 * basic_stats['avg_word_length']) + (0.5 * asl) - 21.43, 1)
            }
        
        return scores
    
    def _calculate_reading_times(self, word_count: int) -> Dict:
        """Calculate reading times for different skill levels."""
        times = {}
        for level, wpm in self.reading_speeds.items():
            minutes = word_count / wpm
            times[level] = {
                "minutes": round(minutes, 1),
                "seconds": round(minutes * 60, 0)
            }
        return times
    
    def _analyze_sentence_complexity(self, text: str) -> Dict:
        """Analyze sentence complexity patterns."""
        sentences = self._split_sentences(text)
        
        complexity_scores = []
        for sentence in sentences:
            words = len(sentence.split())
            clauses = sentence.count(',') + sentence.count(';') + 1
            complexity_score = words * (1 + (clauses - 1) * 0.5)
            complexity_scores.append(complexity_score)
        
        return {
            "average_complexity": round(sum(complexity_scores) / len(complexity_scores) if complexity_scores else 0, 1),
            "max_complexity": max(complexity_scores) if complexity_scores else 0,
            "complexity_variance": round(self._calculate_variance(complexity_scores), 1)
        }
    
    def _analyze_vocabulary(self, text: str) -> Dict:
        """Analyze vocabulary complexity and diversity."""
        words = re.findall(r'\b\w+\b', text.lower())
        unique_words = set(words)
        
        # Simple vocabulary complexity (words > 6 characters)
        complex_words = [word for word in words if len(word) > 6]
        
        return {
            "total_words": len(words),
            "unique_words": len(unique_words),
            "vocabulary_diversity": round(len(unique_words) / len(words) if words else 0, 3),
            "complex_words": len(complex_words),
            "complex_word_percentage": round(len(complex_words) / len(words) * 100 if words else 0, 1)
        }
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word using pattern matching."""
        word = word.lower()
        
        # Remove punctuation
        word = re.sub(r'[^a-z]', '', word)
        
        if not word:
            return 0
        
        # Count vowel groups
        syllables = len(self.vowel_groups.findall(word))
        
        # Subtract silent e
        if self.ending_e.search(word):
            syllables -= 1
        
        # Add back for words ending in 'le'
        if self.ending_le.search(word):
            syllables += 1
        
        # Every word has at least one syllable
        return max(1, syllables)
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _calculate_variance(self, numbers: List[float]) -> float:
        """Calculate variance of a list of numbers."""
        if not numbers:
            return 0
        mean = sum(numbers) / len(numbers)
        return sum((x - mean) ** 2 for x in numbers) / len(numbers)
    
    def _interpret_flesch_score(self, score: float) -> Dict:
        """Interpret Flesch Reading Ease score."""
        if score >= 90:
            return {"level": "Very Easy", "description": "5th grade level", "audience": "Very easy to read"}
        elif score >= 80:
            return {"level": "Easy", "description": "6th grade level", "audience": "Easy to read"}
        elif score >= 70:
            return {"level": "Fairly Easy", "description": "7th grade level", "audience": "Fairly easy to read"}
        elif score >= 60:
            return {"level": "Standard", "description": "8th-9th grade level", "audience": "Plain English, easily understood"}
        elif score >= 50:
            return {"level": "Fairly Difficult", "description": "10th-12th grade level", "audience": "Fairly difficult to read"}
        elif score >= 30:
            return {"level": "Difficult", "description": "College level", "audience": "Difficult to read"}
        else:
            return {"level": "Very Difficult", "description": "Graduate level", "audience": "Very difficult to read"}
    
    def _interpret_grade_level(self, grade: float) -> Dict:
        """Interpret grade level score."""
        if grade <= 6:
            return {"level": "Elementary", "description": "Elementary school level"}
        elif grade <= 8:
            return {"level": "Middle School", "description": "Middle school level"}
        elif grade <= 12:
            return {"level": "High School", "description": "High school level"}
        elif grade <= 16:
            return {"level": "College", "description": "College level"}
        else:
            return {"level": "Graduate", "description": "Graduate school level"}
    
    def _flesch_score_recommendations(self, score: float, basic_stats: Dict) -> List[str]:
        """Generate recommendations based on Flesch score."""
        recommendations = []
        
        if score < 50:
            recommendations.append("Text is too difficult. Shorten sentences and use simpler words.")
            if basic_stats['avg_sentence_length'] > 20:
                recommendations.append(f"Reduce average sentence length from {basic_stats['avg_sentence_length']} words")
            if basic_stats['avg_syllables_per_word'] > 1.6:
                recommendations.append("Replace complex words with simpler alternatives")
        elif score > 70:
            recommendations.append("Text might be too simple for professional content")
        else:
            recommendations.append("Readability is in the target range for general adult audience")
        
        return recommendations
    
    def _grade_level_recommendations(self, grade: float, basic_stats: Dict) -> List[str]:
        """Generate recommendations based on grade level."""
        recommendations = []
        
        if grade > 12:
            recommendations.append("Text is above high school level. Consider simplifying for broader audience.")
            recommendations.append("Break up complex sentences and reduce technical vocabulary")
        elif grade < 8:
            recommendations.append("Text might be too simple for professional content")
        else:
            recommendations.append("Grade level is appropriate for general adult audience")
        
        return recommendations
    
    def _reading_time_recommendations(self, avg_time: float, difficulty: Dict) -> List[str]:
        """Generate recommendations based on reading time."""
        recommendations = []
        
        if avg_time > 10:
            recommendations.append("Consider breaking into shorter sections for better readability")
        if difficulty['level'] == 'high':
            recommendations.append("High complexity may increase actual reading time")
        
        return recommendations
    
    def _sentence_complexity_recommendations(self, metrics: Dict) -> List[str]:
        """Generate recommendations based on sentence complexity."""
        recommendations = []
        
        complex_pct = metrics['complexity_distribution']['complex']['percentage']
        very_complex_pct = metrics['complexity_distribution']['very_complex']['percentage']
        
        if complex_pct + very_complex_pct > 30:
            recommendations.append("Consider breaking up complex sentences for better readability")
        
        if metrics['average_sentence_length'] > 25:
            recommendations.append(f"Average sentence length ({metrics['average_sentence_length']} words) is quite high")
        
        return recommendations
    
    def _assess_readability(self, scores: Dict, complexity: Dict) -> Dict:
        """Provide overall readability assessment."""
        flesch_score = scores.get('flesch_reading_ease', 0)
        
        if flesch_score >= 60:
            level = "Good"
        elif flesch_score >= 50:
            level = "Acceptable"
        else:
            level = "Needs Improvement"
        
        return {
            "overall_level": level,
            "primary_score": flesch_score,
            "target_met": 50 <= flesch_score <= 70
        }
    
    def _assess_reading_difficulty(self, basic_stats: Dict) -> Dict:
        """Assess reading difficulty based on basic statistics."""
        difficulty_score = 0
        
        if basic_stats['avg_sentence_length'] > 20:
            difficulty_score += 2
        elif basic_stats['avg_sentence_length'] > 15:
            difficulty_score += 1
        
        if basic_stats['avg_syllables_per_word'] > 1.6:
            difficulty_score += 2
        elif basic_stats['avg_syllables_per_word'] > 1.4:
            difficulty_score += 1
        
        if difficulty_score <= 1:
            return {"level": "low", "description": "Easy to read"}
        elif difficulty_score <= 3:
            return {"level": "medium", "description": "Moderate difficulty"}
        else:
            return {"level": "high", "description": "Difficult to read"}
    
    def _assess_sentence_complexity(self, metrics: Dict) -> Dict:
        """Assess overall sentence complexity."""
        complex_pct = metrics['complexity_distribution']['complex']['percentage']
        very_complex_pct = metrics['complexity_distribution']['very_complex']['percentage']
        
        total_complex = complex_pct + very_complex_pct
        
        if total_complex < 20:
            return {"level": "low", "description": "Most sentences are simple to moderate"}
        elif total_complex < 40:
            return {"level": "medium", "description": "Balanced mix of sentence complexities"}
        else:
            return {"level": "high", "description": "Many complex sentences may impact readability"}
    
    # Manual calculation methods (fallbacks when textstat unavailable)
    def _calculate_flesch_kincaid(self, basic_stats: Dict) -> float:
        """Manual Flesch-Kincaid calculation."""
        asl = basic_stats['avg_sentence_length']
        asw = basic_stats['avg_syllables_per_word']
        return (0.39 * asl) + (11.8 * asw) - 15.59
    
    def _calculate_gunning_fog(self, text: str, basic_stats: Dict) -> float:
        """Manual Gunning Fog calculation."""
        words = text.split()
        complex_words = sum(1 for word in words if self._count_syllables(word) >= 3)
        complex_word_pct = (complex_words / len(words)) * 100 if words else 0
        
        return 0.4 * (basic_stats['avg_sentence_length'] + complex_word_pct)
    
    def _calculate_ari(self, basic_stats: Dict) -> float:
        """Manual Automated Readability Index calculation."""
        return (4.71 * basic_stats['avg_word_length']) + (0.5 * basic_stats['avg_sentence_length']) - 21.43