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
- `document_analyzer_agent/credentials_loader.py`: Module for loading Langfuse credentials
- `document_analyzer_agent/credentials.properties.template`: Template for Langfuse credentials
- `document_analyzer_agent/tools/pdf_to_png.py`: Custom tool for PDF to PNG conversion
- `document_analyzer_agent/documents/`: Directory for input images and PDFs
- `document_analyzer_agent/output/`: Directory for generated Markdown reports

## Usage

Place your image or PDF files in the `documents` directory (or a custom directory specified with `--documents_path`) and run the agent. The system will:

1. Process supported image formats (JPG, PNG, GIF, WebP) directly
2. Convert PDF files to PNG images before processing
3. Generate a Markdown report in the `output` directory (or a custom directory specified with `--output_path`)

### Command Line Options

The agent supports the following command line options:

- `--context`: Optional. Provides additional context for image analysis. This can be used to guide the analysis with specific information or requirements.
- `--documents_path`: Optional. Specifies a custom path to the folder containing documents to analyze. If not provided, defaults to `document_analyzer_agent/documents`.
- `--output_path`: Optional. Specifies a custom path to the folder where output reports will be saved. If not provided, defaults to `document_analyzer_agent/output`.

Example usage:

```bash
# Run with default settings
python document_analyzer_agent/agent.py

# Run with additional context
python document_analyzer_agent/agent.py --context "These are energy bill statements from June 2025. Look for patterns in energy consumption and costs."

# Run with custom documents path
python document_analyzer_agent/agent.py --documents_path "/path/to/your/documents"

# Run with custom output path
python document_analyzer_agent/agent.py --output_path "/path/to/save/reports"

# Run with both custom paths and context
python document_analyzer_agent/agent.py --documents_path "/path/to/your/documents" --output_path "/path/to/save/reports" --context "Analyze these medical images for abnormalities."
```

## Dependencies

In addition to the Strands SDK, this project requires:

- `strands-agents[otel]`: Strands SDK with OpenTelemetry support
- `strands-agents-tools`: Tools for Strands agents
- `langfuse`: For observability and tracing
- `pdf2image`: For converting PDF files to PNG images
- `Pillow`: For image processing
- `poppler`: Backend for pdf2image (must be installed separately)

## Langfuse Configuration

The agent uses Langfuse for observability and tracing. To configure Langfuse:

1. Copy the template file to create your credentials file:
   ```bash
   cp document_analyzer_agent/credentials.properties.template document_analyzer_agent/credentials.properties
   ```

2. Edit the `document_analyzer_agent/credentials.properties` file with your Langfuse API keys:
   ```ini
   [langfuse]
   langfuse_public_key = your_public_key_here
   langfuse_secret_key = your_secret_key_here
   langfuse_host = https://us.cloud.langfuse.com  # or https://cloud.langfuse.com for EU region
   ```

3. Get your API keys from the [Langfuse dashboard](https://cloud.langfuse.com) after creating an account.

The agent will automatically load these credentials when it runs. If the credentials file is not found or doesn't contain the required keys, the agent will continue to run without Langfuse integration.

### Installing Poppler

Poppler is required for PDF processing. Install it using:

- **macOS**: `brew install poppler`
- **Ubuntu/Debian**: `apt-get install poppler-utils`
- **Windows**: Download from [poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)

## Todo

1. ✅ Support PDF file types by building a custom tool for agent.
2. ✅ Support custom document and output paths.
3. ✅ Integrate with Langfuse for improved observability.
