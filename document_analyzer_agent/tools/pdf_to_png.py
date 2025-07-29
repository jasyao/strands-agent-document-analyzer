"""
PDF to PNG conversion tool for Strands Agent.

This module provides functionality to convert PDF files to PNG images for use with
the Strands Agent. It converts each page of a PDF file to a separate PNG image and
returns the paths to the generated images.

Key Features:
1. PDF Processing:
   • Convert PDF files to PNG images
   • Process individual pages or entire documents
   • Configurable DPI for image quality

2. File Path Handling:
   • Support for absolute paths
   • User directory expansion (~/path/to/file.pdf)
   • Automatic output directory creation
   • Path validation and error reporting

3. Response Format:
   • List of paths to generated PNG images
   • Status reporting for success/failure
   • Detailed error messages

Usage with Strands Agent:
```python
from strands import Agent
from document_analyzer_agent.tools.pdf_to_png import pdf_to_png

agent = Agent(tools=[pdf_to_png])

# Basic usage - convert a PDF file to PNG images
result = agent.tool.pdf_to_png(pdf_path="/path/to/document.pdf")

# With custom output directory and DPI
result = agent.tool.pdf_to_png(
    pdf_path="/path/to/document.pdf",
    output_dir="/path/to/output",
    dpi=300
)
```

Dependencies:
- pdf2image: For PDF to image conversion
- poppler: Backend for pdf2image (must be installed separately)

See the pdf_to_png function docstring for more details on parameters and return format.
"""

import os
from os.path import expanduser, basename, splitext, join, exists
from typing import Any, List, Optional

from pdf2image import convert_from_path
from strands.types.tools import ToolResult, ToolUse

TOOL_SPEC = {
    "name": "pdf_to_png",
    "description": "Converts a PDF file to PNG images, one image per page",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "pdf_path": {
                    "type": "string",
                    "description": "The path to the PDF file to convert",
                },
                "output_dir": {
                    "type": "string",
                    "description": "The directory where PNG images will be saved. If not provided, images will be saved in the same directory as the PDF file.",
                },
                "dpi": {
                    "type": "integer",
                    "description": "The DPI (dots per inch) for the output images. Higher values result in larger, higher quality images.",
                    "default": 200
                },
                "first_page": {
                    "type": "integer",
                    "description": "The first page to convert (1-based index)",
                    "default": 1
                },
                "last_page": {
                    "type": "integer",
                    "description": "The last page to convert (1-based index). If not provided, all pages from first_page to the end will be converted.",
                }
            },
            "required": ["pdf_path"],
        }
    },
}


def pdf_to_png(tool: ToolUse, **kwargs: Any) -> ToolResult:
    """
    Convert a PDF file to PNG images, one image per page.

    This function takes a PDF file path, converts each page to a PNG image,
    and saves the images to the specified output directory. It returns the
    paths to the generated PNG images.

    How It Works:
    ------------
    1. The function expands the provided PDF path (handling ~/ notation)
    2. It checks if the file exists at the specified path
    3. It creates the output directory if it doesn't exist
    4. It converts each page of the PDF to a PNG image using pdf2image
    5. It saves the images to the output directory with sequential naming
    6. It returns the paths to the generated PNG images

    Common Usage Scenarios:
    ---------------------
    - Document processing: Converting PDF documents for image-based analysis
    - OCR preprocessing: Converting PDF files to images for text extraction
    - Visual analysis: Preparing PDF content for AI-based image analysis
    - Document archiving: Converting PDF files to image format for storage

    Args:
        tool: ToolUse object containing the tool usage information and parameters
              The tool input should include:
              - pdf_path (str): Path to the PDF file to convert. Can be absolute
                or user-relative (with ~/).
              - output_dir (str, optional): Directory where PNG images will be saved.
                If not provided, images will be saved in the same directory as the PDF.
              - dpi (int, optional): DPI for the output images. Default is 200.
              - first_page (int, optional): First page to convert (1-based index). Default is 1.
              - last_page (int, optional): Last page to convert (1-based index).
                If not provided, all pages from first_page to the end will be converted.
        **kwargs: Additional keyword arguments (not used in this function)

    Returns:
        ToolResult: A dictionary containing the status and content:
        - On success: Returns paths to the generated PNG images
          {
              "toolUseId": "<tool_use_id>",
              "status": "success",
              "content": [{"text": "Successfully converted PDF to PNG images: [list of paths]"}]
          }
        - On failure: Returns an error message
          {
              "toolUseId": "<tool_use_id>",
              "status": "error",
              "content": [{"text": "Error message"}]
          }

    Notes:
        - This function requires the pdf2image library and poppler to be installed
        - The output images are named based on the PDF filename with page numbers
        - The function validates file existence before attempting to convert
        - User paths with tilde (~) are automatically expanded
    """
    try:
        tool_use_id = tool["toolUseId"]
        tool_input = tool["input"]

        if "pdf_path" not in tool_input:
            return {
                "toolUseId": tool_use_id,
                "status": "error",
                "content": [{"text": "PDF path is required"}],
            }

        # Expand user path and validate PDF file
        pdf_path = expanduser(tool_input.get("pdf_path"))
        if not exists(pdf_path):
            return {
                "toolUseId": tool_use_id,
                "status": "error",
                "content": [{"text": f"PDF file not found at path: {pdf_path}"}],
            }

        # Get output directory or use PDF directory as default
        output_dir = expanduser(tool_input.get("output_dir", ""))
        if not output_dir:
            output_dir = os.path.dirname(pdf_path)
        
        # Create output directory if it doesn't exist
        if not exists(output_dir):
            os.makedirs(output_dir)

        # Get conversion parameters
        dpi = int(tool_input.get("dpi", 200))
        first_page = int(tool_input.get("first_page", 1))
        last_page = int(tool_input.get("last_page", 0)) if "last_page" in tool_input else None

        # Generate base filename from PDF name
        pdf_filename = basename(pdf_path)
        base_filename = splitext(pdf_filename)[0]
        
        # Convert PDF to images
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            first_page=first_page,
            last_page=last_page
        )
        
        # Save images and collect paths
        image_paths = []
        for i, image in enumerate(images):
            page_num = first_page + i
            image_path = join(output_dir, f"{base_filename}_page_{page_num}.png")
            image.save(image_path, "PNG")
            image_paths.append(image_path)
        
        return {
            "toolUseId": tool_use_id,
            "status": "success",
            "content": [{"text": f"Successfully converted PDF to {len(image_paths)} PNG images: {image_paths}"}],
        }
    except Exception as e:
        return {
            "toolUseId": tool_use_id,
            "status": "error",
            "content": [{"text": f"Error converting PDF to PNG: {str(e)}"}],
        }
