# Adobe Hackathon Round 1A: PDF Outline Extractor

A high-performance, multilingual PDF outline extraction tool that extracts structured document outlines (title, headings H1/H2/H3, and page numbers) from PDF files.

## Features

- **Multilingual Support**: Handles documents in English, Japanese, Chinese, Korean, Spanish, French, German, Arabic, Russian, and more
- **Smart Heading Detection**: Uses font analysis, text patterns, and linguistic cues to identify headings
- **Performance Optimized**: Processes 50-page PDFs in under 10 seconds
- **Docker Ready**: Containerized solution with no internet dependency
- **Robust Text Processing**: Handles various PDF formats and encoding issues

## Architecture

```
📁 adobe-hackathon-round1A/
├── 📁 input/          # PDF input files
├── 📁 output/         # JSON output files
├── 📁 src/
│   ├── main.py        # Main PDF processing logic
│   ├── utils.py       # Text processing utilities
│   ├── requirements.txt # Python dependencies
│   ├── Dockerfile     # Container configuration
│   └── run.sh         # Execution script
├── config.py          # Configuration settings
└── README.md          # This file
```

## Quick Start

### Docker Usage (Recommended)

1. **Build the Docker image:**
   ```bash
   docker build -t pdf-outline-extractor .
   ```

2. **Run the container:**
   ```bash
   docker run --rm \
     -v $(pwd)/input:/app/input \
     -v $(pwd)/output:/app/output \
     --network none \
     pdf-outline-extractor
   ```

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r src/requirements.txt
   ```

2. **Run the extractor:**
   ```bash
   cd src
   python main.py
   ```

## Input/Output Format

### Input
- PDF files placed in the `input/` directory
- Maximum 50 pages per PDF
- Supports multilingual documents

### Output
- JSON files in the `output/` directory
- One JSON file per input PDF

**Example Output:**
```json
{
  "title": "Understanding Artificial Intelligence",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 },
    { "level": "H2", "text": "Machine Learning Basics", "page": 5 },
    { "level": "H1", "text": "Conclusion", "page": 10 }
  ]
}
```

## Multilingual Support

The extractor supports documents in multiple languages with specific optimizations:

- **English**: Standard heading patterns, keywords
- **Japanese**: 第一章, 第二節, etc.
- **Chinese**: 章, 节, 部分, etc.
- **Korean**: 장, 절, 항, etc.
- **Arabic**: فصل, قسم, مقدمة, etc.
- **European Languages**: Spanish, French, German, Russian, etc.

## Technical Details

### Heading Detection Algorithm

1. **Font Analysis**: Identifies headings based on font size relative to document average
2. **Pattern Matching**: Recognizes numbered headings (1., 1.1., etc.) and language-specific patterns
3. **Keyword Detection**: Uses multilingual keyword dictionaries
4. **Formatting Cues**: Considers bold text, capitalization, and positioning

### Performance Optimizations

- **Efficient PDF Parsing**: Uses PyMuPDF for fast font and text extraction
- **Smart Sampling**: Analyzes document structure from first few pages
- **Minimal Dependencies**: Lightweight container with essential libraries only
- **Memory Management**: Processes documents page-by-page to minimize memory usage

### Dependencies

- **PyMuPDF**: Fast PDF text and font extraction
- **pdfplumber**: Additional PDF processing capabilities
- **langdetect**: Automatic language detection
- **regex**: Advanced pattern matching for multilingual text

## Configuration

Key settings in `config.py`:

- `MAX_TITLE_LENGTH`: Maximum title length (150 chars)
- `FONT_SIZE_THRESHOLDS`: Font size multipliers for heading levels
- `SUPPORTED_LANGUAGES`: List of supported languages
- `MAX_PROCESSING_TIME`: Maximum processing time (10 seconds)

## Error Handling

- Graceful handling of corrupted or unsupported PDFs
- Fallback mechanisms for font analysis failures
- Comprehensive logging for debugging
- Safe defaults when language detection fails

## Constraints Compliance

✅ **Execution Time**: ≤ 10 seconds for 50-page PDF  
✅ **Model Size**: ≤ 200MB (no ML models used)  
✅ **Internet**: No internet access required  
✅ **Runtime**: CPU only, optimized for x86_64  
✅ **Platform**: linux/amd64 compatible  

## Testing

To test with sample PDFs:

1. Place PDF files in the `input/` directory
2. Run the Docker container or local script
3. Check the `output/` directory for JSON results
4. Verify heading detection accuracy and performance

## Troubleshooting

**Common Issues:**

- **No headings detected**: Check if PDF has proper font formatting
- **Wrong language detection**: Ensure sufficient text sample for detection
- **Performance issues**: Verify PDF complexity and page count
- **Docker build fails**: Check system dependencies and Docker version

## License

This project is created for the Adobe Hackathon Round 1A competition.

---

**Author**: PDF Outline Extractor Team  
**Version**: 1.0.0  
**Last Updated**: 2025-07-26