"""SEO analysis and content optimization tools."""
from typing import List, Dict
from keybert import KeyBERT
import spacy
from collections import Counter
import re


class SEOAnalyzer:
    """SEO tools for content optimization."""

    def __init__(self):
        # Initialize KeyBERT for keyword extraction
        self.kw_model = KeyBERT()

        # Try to load spaCy model (if not available, fall back to basic)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            self.nlp = None
            print("Warning: spaCy model not loaded. Run: python -m spacy download en_core_web_sm")

    def extract_keywords(self, text: str, top_n: int = 10) -> List[Dict[str, float]]:
        """Extract SEO keywords from text.

        Args:
            text: Input text
            top_n: Number of keywords to extract

        Returns:
            List of {keyword, score} dicts
        """
        try:
            keywords = self.kw_model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 3),
                stop_words='english',
                top_n=top_n,
                use_maxsum=True
            )

            return [{"keyword": kw, "score": round(score, 3)} for kw, score in keywords]
        except Exception as e:
            print(f"Keyword extraction error: {e}")
            return []

    def generate_seo_outline(self, topic: str, target_keywords: List[str] = None) -> Dict:
        """Generate SEO-optimized content outline.

        Args:
            topic: Main topic/title
            target_keywords: Optional list of keywords to include

        Returns:
            Dict with outline structure
        """
        outline = {
            "title": f"{topic}: Complete Guide for 2026",
            "meta_description": f"Discover everything about {topic}. Expert insights, practical tips, and latest trends.",
            "structure": [
                {
                    "type": "h1",
                    "text": f"{topic}: Complete Guide",
                    "keywords": target_keywords[:2] if target_keywords else []
                },
                {
                    "type": "intro",
                    "text": "Introduction paragraph with hook",
                    "guidelines": [
                        "Address reader's pain point",
                        "Include primary keyword in first 100 words",
                        "Promise value/solution"
                    ]
                },
                {
                    "type": "h2",
                    "text": f"What is {topic}?",
                    "keywords": target_keywords[:1] if target_keywords else []
                },
                {
                    "type": "h2",
                    "text": f"Key Benefits of {topic}",
                    "keywords": ["benefits", topic.lower()]
                },
                {
                    "type": "h2",
                    "text": f"How to Get Started with {topic}",
                    "keywords": ["how to", topic.lower()]
                },
                {
                    "type": "h2",
                    "text": f"Common Challenges and Solutions",
                    "keywords": ["challenges", "problems", topic.lower()]
                },
                {
                    "type": "h2",
                    "text": f"Best Practices for {topic}",
                    "keywords": ["best practices", topic.lower()]
                },
                {
                    "type": "h2",
                    "text": "Conclusion",
                    "guidelines": [
                        "Summarize key points",
                        "Call to action",
                        "Include primary keyword"
                    ]
                }
            ],
            "seo_checklist": [
                "Include target keyword in title, H1, H2s",
                "Keep title under 60 characters",
                "Meta description 150-160 characters",
                "Use numbered/bulleted lists",
                "Include internal links",
                "Add external authoritative links",
                "Use semantic keywords (LSI)",
                "Optimize images with alt text",
                "Aim for 1500-2500 words"
            ]
        }

        return outline

    def generate_aeo_snippets(self, topic: str, content_context: str = "") -> Dict:
        """Generate Answer Engine Optimization snippets.

        AEO optimizes for AI assistants, voice search, and featured snippets.

        Args:
            topic: Main topic
            content_context: Optional context from knowledge base

        Returns:
            Dict with AEO-optimized Q&A snippets
        """
        snippets = {
            "featured_snippet_qa": [
                {
                    "question": f"What is {topic}?",
                    "answer_format": "Short definition (40-60 words)",
                    "guidelines": [
                        "Start with direct answer",
                        "No filler words",
                        "Use simple language"
                    ]
                },
                {
                    "question": f"How does {topic} work?",
                    "answer_format": "Step-by-step list (3-5 steps)",
                    "guidelines": [
                        "Number each step",
                        "Action-oriented language",
                        "Keep each step concise"
                    ]
                },
                {
                    "question": f"What are the benefits of {topic}?",
                    "answer_format": "Bulleted list (3-5 benefits)",
                    "guidelines": [
                        "Start each with action verb",
                        "Quantify when possible",
                        "Focus on user value"
                    ]
                }
            ],
            "voice_search_qa": [
                {
                    "question": f"Why should I use {topic}?",
                    "answer_format": "Conversational 1-2 sentences"
                },
                {
                    "question": f"When is the best time to use {topic}?",
                    "answer_format": "Specific, actionable answer"
                }
            ],
            "semantic_keywords": self._generate_semantic_keywords(topic),
            "optimization_tips": [
                "Use natural language (how people speak)",
                "Answer questions directly in first paragraph",
                "Use schema markup (FAQ, HowTo)",
                "Include 'People Also Ask' questions",
                "Optimize for long-tail queries"
            ]
        }

        return snippets

    def _generate_semantic_keywords(self, topic: str) -> List[str]:
        """Generate LSI/semantic keywords related to topic."""
        # This is a simplified version - in production, use word2vec or BERT
        base_variations = [
            topic.lower(),
            f"{topic.lower()} guide",
            f"{topic.lower()} tutorial",
            f"{topic.lower()} tips",
            f"best {topic.lower()}",
            f"how to {topic.lower()}",
            f"{topic.lower()} for beginners"
        ]

        return base_variations

    def analyze_content_seo(self, content: str, target_keyword: str) -> Dict:
        """Analyze content for SEO quality.

        Args:
            content: Full content text
            target_keyword: Primary keyword to check

        Returns:
            Dict with SEO analysis and scores
        """
        content_lower = content.lower()
        keyword_lower = target_keyword.lower()

        # Count keyword occurrences
        keyword_count = content_lower.count(keyword_lower)
        word_count = len(content.split())

        # Calculate keyword density (ideal: 1-2%)
        keyword_density = (keyword_count / word_count * 100) if word_count > 0 else 0

        # Check H1/H2 presence
        h1_present = bool(re.search(r'^#\s', content, re.MULTILINE))
        h2_present = bool(re.search(r'^##\s', content, re.MULTILINE))

        # Check lists
        has_lists = bool(re.search(r'^\d+\.|\*|-', content, re.MULTILINE))

        analysis = {
            "word_count": word_count,
            "keyword_count": keyword_count,
            "keyword_density": round(keyword_density, 2),
            "scores": {
                "length": "PASS" if word_count >= 1500 else "IMPROVE",
                "keyword_density": "PASS" if 1 <= keyword_density <= 2 else "IMPROVE",
                "structure": "PASS" if (h1_present and h2_present) else "IMPROVE",
                "readability": "PASS" if has_lists else "IMPROVE"
            },
            "recommendations": []
        }

        # Add recommendations
        if word_count < 1500:
            analysis["recommendations"].append(f"Increase content to 1500+ words (current: {word_count})")

        if keyword_density < 1:
            analysis["recommendations"].append(f"Increase keyword usage (density: {keyword_density:.2f}%)")
        elif keyword_density > 2:
            analysis["recommendations"].append(f"Reduce keyword stuffing (density: {keyword_density:.2f}%)")

        if not h1_present or not h2_present:
            analysis["recommendations"].append("Add proper heading structure (H1, H2s)")

        if not has_lists:
            analysis["recommendations"].append("Add bulleted or numbered lists for better readability")

        return analysis
