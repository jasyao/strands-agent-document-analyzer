# strands-agent-document-analyzer

## Overview

This package contains an agent implementation using the Strands SDK to analyze documents in image format. It processes images and generates a Markdown report with analysis and insights.

## Features

- Analyzes images using Claude 3 Sonnet model
- Generates structured Markdown reports with analysis results
- Supports multiple image formats: JPG, PNG, GIF, and WebP
- Supports PDF files by converting them to PNG images
- Uses a multi-agent workflow for specialized processing

## How It Works

The package implements a two-agent workflow:

1. **Image Analyzer Agent**: Processes images and extracts information, insights, and trends
2. **Report Generator Agent**: Takes the analysis and creates a formatted Markdown report

The workflow is orchestrated using Strands' GraphBuilder, which manages the flow of information between agents.

## Supported File Formats

- JPEG/JPG
- PNG
- GIF
- WebP
- PDF (converted to PNG for processing)

## Directory Structure

- `document_analyzer_agent/agent.py`: Main agent implementation
- `document_analyzer_agent/tools/pdf_to_png.py`: Custom tool for PDF to PNG conversion
- `document_analyzer_agent/documents/`: Directory for input images and PDFs
- `document_analyzer_agent/output/`: Directory for generated Markdown reports

## Usage

Place your image or PDF files in the `documents` directory and run the agent. The system will:

1. Process supported image formats (JPG, PNG, GIF, WebP) directly
2. Convert PDF files to PNG images before processing
3. Generate a Markdown report in the `output` directory

### Command Line Options

The agent supports the following command line options:

- `--context`: Optional. Provides additional context for image analysis. This can be used to guide the analysis with specific information or requirements.

Example usage:

```bash
# Run with default settings
python document_analyzer_agent/agent.py

# Run with additional context
python document_analyzer_agent/agent.py --context "These are energy bill statements from June 2025. Look for patterns in energy consumption and costs."
```

## Dependencies

In addition to the Strands SDK, this project requires:

- `pdf2image`: For converting PDF files to PNG images
- `Pillow`: For image processing
- `poppler`: Backend for pdf2image (must be installed separately)

### Installing Poppler

Poppler is required for PDF processing. Install it using:

- **macOS**: `brew install poppler`
- **Ubuntu/Debian**: `apt-get install poppler-utils`
- **Windows**: Download from [poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)

## Todo

1. ✅ Support PDF file types by building a custom tool for agent.
2. Integrate with Langfuse for improved observability.
