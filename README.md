# 🧠 Adobe Hackathon Round 1A – Structured PDF Outline Extractor

## 📌 Problem Statement
In this challenge, we were tasked with extracting a **structured outline** from PDF files. This includes:
- Title of the document
- Headings organized by level: H1, H2, H3
- Page number information

The extracted content is output in a **clean, hierarchical JSON** format, to be used as a base for intelligent document navigation.

---

## 👨‍💻 Team Members
- **Chaitanya Pyla** *(Team Lead, Dev & Integration)*
- **Manohar**
- **Suhel**

We collaborated on this project by dividing tasks like text extraction, heading detection, logic for multilingual support, and Dockerization.

---

## 🧩 Features
- ✅ Title detection using font size and positioning
- ✅ Heading level detection: H1, H2, H3
- ✅ Page number tracking for each heading
- ✅ Works with multilingual PDFs (including Japanese)
- ✅ Offline-capable (no internet required)
- ✅ Fully Dockerized and platform-independent
- ✅ Compatible with CPU-only systems (no GPU dependencies)

---

## 🛠️ Technologies Used
- Python 3.9
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) (`fitz`)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [langdetect](https://pypi.org/project/langdetect/) (for multilingual handling)
- Docker

---

## 📁 Input / Output Format

### ✅ Input
PDF files placed in the `/app/input` directory.

### ✅ Output
One `.json` file per input PDF generated in the `/app/output` directory.

#### Example Output:
```json
{
  "title": "人工知能の概要",
  "outline": [
    { "level": "H1", "text": "第1章 はじめに", "page": 1 },
    { "level": "H2", "text": "1.1 人工知能とは？", "page": 1 },
    { "level": "H2", "text": "1.2 歴史的背景", "page": 1 }
  ]
}
