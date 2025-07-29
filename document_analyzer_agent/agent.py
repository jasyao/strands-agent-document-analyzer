import logging
import os
import argparse
from strands import Agent
from strands.multiagent import GraphBuilder
from strands.types.content import ContentBlock
from strands_tools import file_write, image_reader, shell
from tools import pdf_to_png


# Enables Strands debug log level
logging.getLogger("strands").setLevel(logging.DEBUG)

# Sets the logging format and streams logs to stderr
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

# Create agents for image processing workflow
image_analyzer = Agent(
    system_prompt=
        f'''
            You are an image analysis expert. Analyze all images in the folder {os.getcwd()}/document_analyzer_agent/documents.
            
            YOU MUST analyze PDF files by first converting them to PNG images using the pdf_to_png tool.
            
            When you encounter a PDF file:
            1. Use the pdf_to_png tool to convert it to PNG images
            2. Use the image_reader tool to read the generated PNG images
            3. Analyze the images as you would with any other image

            ONLY ANALYZE the image(s) and provide the following information in a well structured format that is easy to consume and process:
                1. Summary of image analysis
                2. Insights on any trends or themes that you have observed

            DO NOT CREATE the Markdown report as there is a separate agent that owns this responsibility. You are only providing information to that agent.
        ''',
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[image_reader, shell, pdf_to_png]
)
report_generator = Agent(
    system_prompt=
        f'''
            You are an Markdown report generation expert. Generate a report based on the provided analysis of the image(s) and save the report in the directory {os.getcwd()}/document_analyzer_agent/output.
            
            You will be provided the following information:
                1. Summary of analysis
                2. Insights on any trends or themes
        ''',
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[file_write]
)        

# Build the graph
builder = GraphBuilder()
builder.add_node(image_analyzer, "image_analyzer")
builder.add_node(report_generator, "report_generator")
builder.add_edge("image_analyzer", "report_generator")
builder.set_entry_point("image_analyzer")

graph = builder.build()

# Parse command line arguments
parser = argparse.ArgumentParser(description='Document analyzer agent')
parser.add_argument('--context', type=str, help='Additional context for image analysis', default=None)
args = parser.parse_args()

# Create content blocks with text and image
documents_folder_path = f"{os.getcwd()}/document_analyzer_agent/documents"
file_names = os.listdir(documents_folder_path)

# Create initial content block with instructions and optional context
instruction_text = f"Analyze the provided images or PDF files in the documents directory and create a Markdown report that provides high level insights and metrics. Please output the path to the generated report."
if args.context:
    instruction_text += f"\n\nAdditional context for analysis: {args.context}"

content_blocks = [
    ContentBlock(text=instruction_text)
]

# Execute the graph with multi-modal input
result = graph(content_blocks)
