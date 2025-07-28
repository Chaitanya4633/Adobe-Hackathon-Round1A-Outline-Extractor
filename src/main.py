#!/usr/bin/env python3
import os
import json
import sys
import re
from pathlib import Path
from typing import Dict, List

import fitz 
import pdfplumber
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from utils import(
    detect_heading_level,
    extract_title_from_text,
    is_likely_heading,
    normalize_text,
    get_font_info
)

from config import(
    INPUT_DIR,
    OUTPUT_DIR,
    HEADING_PATTERNS,
    FONT_SIZE_THRESHOLDS,
    MAX_TITLE_LENGTH
)

class PDFOutlineExtractor:
    def __init__(self):
        self.doc=None
        self.language='en'
        self.font_sizes=[]
        self.avg_font_size=12

    def extract_outline(self,pdf_path: str)->Dict:
        try:
            self.doc=fitz.open(pdf_path)
            self._analyze_document_structure()
            title=self._extract_title()
            outline=self._extract_headings()
            return{
                "title":title,
                "outline":outline
            }
        except Exception as e:
            print(f"Error processing {pdf_path}:{str(e)}",file=sys.stderr)
            return {"title":"Unknown","outline":[]}
        finally:
            if self.doc:
                self.doc.close()

    def _analyze_document_structure(self):
        font_sizes=[]
        text_sample=""
        max_pages=min(5,len(self.doc))

        for page_num in range(max_pages):
            page=self.doc[page_num]
            blocks=page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            font_size=span["size"]
                            text=span["text"].strip()
                            if text and len(text)>2:
                                font_sizes.append(font_size)
                                text_sample+=text + " "

        if font_sizes:
            self.font_sizes=sorted(set(font_sizes),reverse=True)
            self.avg_font_size=sum(font_sizes)/len(font_sizes)

        try:
            if text_sample.strip():
                self.language=detect(text_sample[:1000])
        except LangDetectException:
            self.language='en'

    def _extract_title(self)->str:
        if not self.doc or len(self.doc)==0:
            return "Unknown"

        first_page=self.doc[0]
        blocks=first_page.get_text("dict")["blocks"]
        candidates=[]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    line_text=""
                    max_font_size=0
                    for span in line["spans"]:
                        text=span["text"].strip()
                        font_size=span["size"]
                        if text:
                            line_text+=text + " "
                            max_font_size=max(max_font_size,font_size)

                    line_text=line_text.strip()
                    if (line_text and len(line_text)<=MAX_TITLE_LENGTH and
                            len(line_text)>3 and max_font_size>self.avg_font_size*1.2):
                        candidates.append((line_text,max_font_size,len(line_text)))

        if candidates:
            candidates.sort(key=lambda x:(-x[1],x[2]))
            return normalize_text(candidates[0][0])

        return "Unknown"

    def _extract_headings(self)->List[Dict]:
        headings=[]

        for page_num in range(len(self.doc)):
            page=self.doc[page_num]
            blocks=page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        line_text=""
                        font_info=get_font_info(line)
                        for span in line["spans"]:
                            text=span["text"].strip()
                            if text:
                                line_text += text + " "
                        line_text=line_text.strip()

                        if line_text and is_likely_heading(line_text, font_info, self.avg_font_size, self.language):
                            level = detect_heading_level(line_text,font_info, self.font_sizes,self.language)
                            if level:
                                headings.append({
                                    "level":level,
                                    "text":normalize_text(line_text),
                                    "page":page_num + 1
                                })

        return headings


def process_pdf_file(input_path: str, output_path: str):
    extractor=PDFOutlineExtractor()
    result=extractor.extract_outline(input_path)

    with open(output_path,'w',encoding='utf-8') as f:
        json.dump(result,f,ensure_ascii=False,indent=2)

    print(f"Processed:{input_path}->{output_path}")


def main():
    input_dir=Path(INPUT_DIR)
    output_dir=Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)

    pdf_files=list(input_dir.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in input directory",file=sys.stderr)
        return

    for pdf_file in pdf_files:
        output_file=output_dir / f"{pdf_file.stem}.json"
        process_pdf_file(str(pdf_file),str(output_file))

    print(f"Processed{len(pdf_files)} PDF files")


if __name__ == "__main__":
    main()

import os
import json
import sys
import re
from pathlib import Path
from typing import Dict, List

import fitz  
import pdfplumber
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from utils import (
    detect_heading_level,
    extract_title_from_text,
    is_likely_heading,
    normalize_text,
    get_font_info
)
from config import(
    INPUT_DIR,
    OUTPUT_DIR,
    HEADING_PATTERNS,
    FONT_SIZE_THRESHOLDS,
    MAX_TITLE_LENGTH
)

class PDFOutlineExtractor:
    def __init__(self):
        self.doc = None
        self.language = 'en'
        self.font_sizes = []
        self.avg_font_size = 12

    def extract_outline(self, pdf_path: str) -> Dict:
        try:
            self.doc=fitz.open(pdf_path)
            self._analyze_document_structure()
            title=self._extract_title()
            outline=self._extract_headings()
            return {
                "title":title,
                "outline":outline
            }
        except Exception as e:
            print(f"Error processing {pdf_path}: {str(e)}",file=sys.stderr)
            return {"title": "Unknown", "outline":[]}
        finally:
            if self.doc:
                self.doc.close()

    def _analyze_document_structure(self):
        font_sizes=[]
        text_sample=""
        max_pages=min(5, len(self.doc))

        for page_num in range(max_pages):
            page=self.doc[page_num]
            blocks=page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            font_size=span["size"]
                            text=span["text"].strip()
                            if text and len(text) > 2:
                                font_sizes.append(font_size)
                                text_sample += text + " "

        if font_sizes:
            self.font_sizes=sorted(set(font_sizes),reverse=True)
            self.avg_font_size=sum(font_sizes) / len(font_sizes)

        try:
            if text_sample.strip():
                self.language=detect(text_sample[:1000])
        except LangDetectException:
            self.language='en'

    def _extract_title(self) -> str:
        if not self.doc or len(self.doc) == 0:
            return "Unknown"

        first_page=self.doc[0]
        blocks=first_page.get_text("dict")["blocks"]
        candidates=[]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    line_text=""
                    max_font_size=0
                    for span in line["spans"]:
                        text=span["text"].strip()
                        font_size=span["size"]
                        if text:
                            line_text += text + " "
                            max_font_size=max(max_font_size,font_size)

                    line_text = line_text.strip()
                    if (line_text and len(line_text)<=MAX_TITLE_LENGTH and
                            len(line_text)>3 and max_font_size>self.avg_font_size*1.2):
                        candidates.append((line_text, max_font_size,len(line_text)))

        if candidates:
            candidates.sort(key=lambda x:(-x[1], x[2]))
            return normalize_text(candidates[0][0])

        return "Unknown"

    def _extract_headings(self)->List[Dict]:
        headings=[]

        for page_num in range(len(self.doc)):
            page=self.doc[page_num]
            blocks=page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        line_text=""
                        font_info=get_font_info(line)
                        for span in line["spans"]:
                            text=span["text"].strip()
                            if text:
                                line_text += text + " "
                        line_text=line_text.strip()

                        if line_text and is_likely_heading(line_text, font_info, self.avg_font_size, self.language):
                            level=detect_heading_level(line_text, font_info, self.font_sizes, self.language)
                            if level:
                                headings.append({
                                    "level":level,
                                    "text":normalize_text(line_text),
                                    "page":page_num+1
                                })

        return headings


def process_pdf_file(input_path: str, output_path: str):
    extractor=PDFOutlineExtractor()
    result=extractor.extract_outline(input_path)

    with open(output_path,'w',encoding='utf-8') as f:
        json.dump(result,f,ensure_ascii=False,indent=2)

    print(f"Processed: {input_path}->{output_path}")


def main():
    input_dir=Path(INPUT_DIR)
    output_dir=Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)

    pdf_files=list(input_dir.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in input directory",file=sys.stderr)
        return

    for pdf_file in pdf_files:
        output_file=output_dir/f"{pdf_file.stem}.json"
        process_pdf_file(str(pdf_file),str(output_file))

    print(f"Processed {len(pdf_files)} PDF files")


if __name__ =="__main__":
    main()