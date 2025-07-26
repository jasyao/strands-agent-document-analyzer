# strands-agent-document-analyzer

## Overview

This package contains an agent implementation using the Strands SDK to analyze documents in image format. It processes images and generates an HTML report with analysis and insights.

## Features

- Analyzes images using Claude 3 Sonnet model
- Generates structured HTML reports with analysis results
- Supports multiple image formats: JPG, PNG, GIF, and WebP
- Uses a multi-agent workflow for specialized processing

## How It Works

The package implements a two-agent workflow:

1. **Image Analyzer Agent**: Processes images and extracts information, insights, and trends
2. **Report Generator Agent**: Takes the analysis and creates a formatted HTML report

The workflow is orchestrated using Strands' GraphBuilder, which manages the flow of information between agents.

## Supported Image Formats

- JPEG/JPG
- PNG
- GIF
- WebP

## Directory Structure

- `document_analyzer_agent/agent.py`: Main agent implementation
- `document_analyzer_agent/documents/`: Directory for input images
- `document_analyzer_agent/output/`: Directory for generated HTML reports

## Usage

Place your image files in the `documents` directory and run the agent. The system will:

1. Process only supported image formats (JPG, PNG, GIF, WebP)
2. Skip any unsupported file types with a warning
3. Generate an HTML report in the `output` directory

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
