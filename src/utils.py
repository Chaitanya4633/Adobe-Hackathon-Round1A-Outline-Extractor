#!/usr/bin/env python3
"""
Utility functions for PDF outline extraction with multilingual support.
"""

import re
from typing import Dict, List, Optional, Tuple
from langdetect import detect, LangDetectException

def normalize_text(text: str) -> str:
    """Normalize text by removing extra whitespace and cleaning up formatting."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove common PDF artifacts
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    return text


def get_font_info(line: Dict) -> Dict:
    """Extract font information from a text line."""
    font_info = {
        'size': 0,
        'weight': 'normal',
        'flags': 0,
        'font_name': ''
    }
    
    if 'spans' in line:
        for span in line['spans']:
            if span.get('size', 0) > font_info['size']:
                font_info['size'] = span.get('size', 0)
                font_info['flags'] = span.get('flags', 0)
                font_info['font_name'] = span.get('font', '')
                
                # Detect bold text (flag 16 = bold)
                if span.get('flags', 0) & 16:
                    font_info['weight'] = 'bold'
    
    return font_info


def is_likely_heading(text: str, font_info: Dict, avg_font_size: float, language: str = 'en') -> bool:
    """Determine if text is likely a heading based on various criteria."""
    if not text or len(text.strip()) < 2:
        return False
    
    text = text.strip()
    
    # Skip very long lines (likely paragraphs)
    if len(text) > 200:
        return False
    
    # Skip lines that end with periods (likely sentences)
    if text.endswith('.'):
        return False
    
    # Font size criterion
    font_size = font_info.get('size', 0)
    if font_size <= avg_font_size * 1.1:
        return False
    
    # Check for numbered headings (multilingual)
    numbered_patterns = [
        r'^\d+\.?\s+',  # "1. " or "1 "
        r'^\d+\.\d+\.?\s+',  # "1.1. " or "1.1 "
        r'^\d+\.\d+\.\d+\.?\s+',  # "1.1.1. " or "1.1.1 "
        r'^[IVXLCDM]+\.?\s+',  # Roman numerals
        r'^[A-Z]\.\s+',  # "A. "
        r'^\([a-z]\)\s+',  # "(a) "
    ]
    
    # Japanese/Chinese specific patterns
    if language in ['ja', 'zh', 'ko']:
        numbered_patterns.extend([
            r'^第[一二三四五六七八九十百千万]+章\s*',  # Japanese chapter
            r'^第[0-9]+章\s*',  # Numbered chapter
            r'^[一二三四五六七八九十百千万]+[、．]\s*',  # Chinese numerals
        ])
    
    for pattern in numbered_patterns:
        if re.match(pattern, text):
            return True
    
    # Check for common heading keywords (multilingual)
    heading_keywords = {
        'en': ['chapter', 'section', 'introduction', 'conclusion', 'abstract', 'summary', 'overview', 'background'],
        'ja': ['章', '節', '項', '序論', '結論', '概要', '背景', 'まとめ'],
        'zh': ['章', '节', '部分', '引言', '结论', '摘要', '概述', '背景'],
        'es': ['capítulo', 'sección', 'introducción', 'conclusión', 'resumen'],
        'fr': ['chapitre', 'section', 'introduction', 'conclusion', 'résumé'],
        'de': ['kapitel', 'abschnitt', 'einleitung', 'schluss', 'zusammenfassung'],
    }
    
    keywords = heading_keywords.get(language, heading_keywords['en'])
    text_lower = text.lower()
    
    for keyword in keywords:
        if keyword in text_lower:
            return True
    
    # Bold text is more likely to be a heading
    if font_info.get('weight') == 'bold':
        return True
    
    # Check if text is all caps (common for headings)
    if text.isupper() and len(text) > 3:
        return True
    
    # Check capitalization pattern (Title Case)
    words = text.split()
    if len(words) >= 2:
        capitalized_words = sum(1 for word in words if word and word[0].isupper())
        if capitalized_words / len(words) >= 0.7:  # 70% of words capitalized
            return True
    
    return False


def detect_heading_level(text: str, font_info: Dict, font_sizes: List[float], language: str = 'en') -> Optional[str]:
    """Detect the heading level (H1, H2, H3) based on font size and content."""
    if not font_sizes:
        return "H1"  # Default if no font size information
    
    font_size = font_info.get('size', 0)
    
    # Sort font sizes in descending order
    sorted_sizes = sorted(set(font_sizes), reverse=True)
    
    # Determine level based on font size ranking
    if len(sorted_sizes) >= 3:
        if font_size >= sorted_sizes[0]:
            level = "H1"
        elif font_size >= sorted_sizes[1]:
            level = "H2"
        else:
            level = "H3"
    elif len(sorted_sizes) == 2:
        if font_size >= sorted_sizes[0]:
            level = "H1"
        else:
            level = "H2"
    else:
        level = "H1"
    
    # Adjust level based on content patterns
    text_clean = text.strip()
    
    # Check for explicit numbering patterns that indicate level
    if re.match(r'^\d+\.\s+', text_clean):  # "1. "
        level = "H1"
    elif re.match(r'^\d+\.\d+\.\s+', text_clean):  # "1.1. "
        level = "H2"
    elif re.match(r'^\d+\.\d+\.\d+\.\s+', text_clean):  # "1.1.1. "
        level = "H3"
    
    # Japanese/Chinese specific level detection
    if language in ['ja', 'zh', 'ko']:
        if re.match(r'^第[一二三四五六七八九十百千万]+章', text_clean):
            level = "H1"
        elif re.match(r'^第[一二三四五六七八九十百千万]+節', text_clean):
            level = "H2"
        elif re.match(r'^第[一二三四五六七八九十百千万]+項', text_clean):
            level = "H3"
    
    return level


def extract_title_from_text(text: str, max_length: int = 100) -> str:
    """Extract a clean title from text."""
    if not text:
        return "Unknown"
    
    # Clean up the text
    title = normalize_text(text)
    
    # Remove common title prefixes
    prefixes_to_remove = [
        r'^title:?\s*',
        r'^subject:?\s*',
        r'^document:?\s*',
    ]
    
    for prefix in prefixes_to_remove:
        title = re.sub(prefix, '', title, flags=re.IGNORECASE)
    
    # Truncate if too long
    if len(title) > max_length:
        title = title[:max_length].rsplit(' ', 1)[0] + '...'
    
    return title.strip() or "Unknown"


def is_multilingual_text(text: str) -> Tuple[bool, str]:
    """Detect if text contains multilingual content."""
    try:
        language = detect(text)
        
        # Check for mixed scripts
        has_latin = bool(re.search(r'[a-zA-Z]', text))
        has_cjk = bool(re.search(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]', text))
        has_arabic = bool(re.search(r'[\u0600-\u06ff]', text))
        has_cyrillic = bool(re.search(r'[\u0400-\u04ff]', text))
        
        script_count = sum([has_latin, has_cjk, has_arabic, has_cyrillic])
        
        return script_count > 1, language
    
    except LangDetectException:
        return False, 'en'


def clean_heading_text(text: str, language: str = 'en') -> str:
    """Clean heading text by removing numbering and formatting artifacts."""
    if not text:
        return ""
    
    cleaned = normalize_text(text)
    
    # Remove common numbering patterns
    patterns_to_remove = [
        r'^\d+\.?\s*',  # "1. " or "1 "
        r'^\d+\.\d+\.?\s*',  # "1.1. " or "1.1 "
        r'^\d+\.\d+\.\d+\.?\s*',  # "1.1.1. " or "1.1.1 "
        r'^[IVXLCDM]+\.?\s*',  # Roman numerals
        r'^[A-Z]\.\s*',  # "A. "
        r'^\([a-z]\)\s*',  # "(a) "
    ]
    
    # Language-specific patterns
    if language in ['ja', 'zh', 'ko']:
        patterns_to_remove.extend([
            r'^第[一二三四五六七八九十百千万]+章\s*',
            r'^第[0-9]+章\s*',
            r'^[一二三四五六七八九十百千万]+[、．]\s*',
        ])
    
    for pattern in patterns_to_remove:
        cleaned = re.sub(pattern, '', cleaned)
    
    return cleaned.strip()