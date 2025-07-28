#!/usr/bin/env python3
"""
Configuration settings for PDF outline extraction.
"""
import os

INPUT_DIR="/app/input"
OUTPUT_DIR="/app/output"

if not os.path.exists(INPUT_DIR):
    INPUT_DIR="../input"
if not os.path.exists(OUTPUT_DIR):
    OUTPUT_DIR="../output"

MAX_TITLE_LENGTH=150

FONT_SIZE_THRESHOLDS={
    'H1':1.5,
    'H2':1.3,
    'H3':1.1,
}

HEADING_PATTERNS={
    'numbered':[
        r'^\d+\.?\s+',
        r'^\d+\.\d+\.?\s+',
        r'^\d+\.\d+\.\d+\.?\s+',
        r'^[IVXLCDM]+\.?\s+',
        r'^[A-Z]\.\s+',
        r'^\([a-z]\)\s+',
    ],
    'japanese':[
        r'^第[一二三四五六七八九十百千万]+章\s*',
        r'^第[0-9]+章\s*',
        r'^[一二三四五六七八九十百千万]+[、．]\s*',
    ],
    'keywords':{
        'en':['chapter','section','introduction','conclusion','abstract', 'summary','overview','background'],
        'ja':['章','節','項','序論','結論','概要','背景','まとめ'],
        'zh':['章','节','部分','引言','结论','摘要','概述','背景'],
        'es':['capítulo','sección','introducción','conclusión','resumen'],
        'fr':['chapitre','section','introduction','conclusion','résumé'],
        'de':['kapitel','abschnitt','einleitung','schluss','zusammenfassung'],
        'ko':['장','절','항','서론','결론','요약','개요','배경'],
        'ar':['فصل','قسم','مقدمة','خاتمة','ملخص','نظرة عامة'],
        'ru':['глава','раздел','введение','заключение','резюме','обзор'],
    }
}

MAX_PAGES_TO_ANALYZE=50
MAX_PROCESSING_TIME=10  
MIN_HEADING_LENGTH=2
MAX_HEADING_LENGTH=200
MIN_TITLE_LENGTH=3
LANGUAGE_DETECTION_SAMPLE_SIZE=1000

SUPPORTED_LANGUAGES=[
    'en','ja','zh','ko','es','fr','de','ar','ru','it','pt','nl','sv','da','no'
]

MIN_FONT_SIZE_DIFFERENCE=0.5
BOLD_FONT_FLAG=16  
JSON_INDENT=2
JSON_ENSURE_ASCII=False