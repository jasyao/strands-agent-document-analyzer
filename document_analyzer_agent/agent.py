import logging
import os
import argparse
from strands import Agent
from strands.multiagent import GraphBuilder
from strands.types.content import ContentBlock
from strands_tools import file_write


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
        '''
            You are an image analysis expert. Only analyze the image(s) and provide the following information:
                1. Summary of image analysis
                2. Insights on any trends or themes that you have observed

            The information will be shared to an HTML report generation agent. Please present the information in a well structured format that is easy to consume and process.
        ''',
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0"
)
report_generator = Agent(
    system_prompt=
        '''
            You are an HTML report generation expert. Generate a report based on the provided analysis of the image(s). You will be provided the following information:
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
instruction_text = f"Analyze the provided images and create an HTML report that provides high level insights and metrics in the directory {os.getcwd()}/document_analyzer_agent/output."
if args.context:
    instruction_text += f"\n\nAdditional context for analysis: {args.context}"

content_blocks = [
    ContentBlock(text=instruction_text)
]

for file_name in file_names:
    # Check if the file is a supported image format (jpg, png, gif, webp)
    if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
        with open(f"{documents_folder_path}/{file_name}", "rb") as fp:
            image_bytes = fp.read()
            # Determine the format based on file extension
            if file_name.lower().endswith('.png'):
                image_format = "png"
            elif file_name.lower().endswith(('.jpg', '.jpeg')):
                image_format = "jpeg"
            elif file_name.lower().endswith('.gif'):
                image_format = "gif"
            elif file_name.lower().endswith('.webp'):
                image_format = "webp"
            content_blocks.append(ContentBlock(image={"format": image_format, "source": {"bytes": image_bytes}}))
    else:
        logging.warning(f"Skipping file {file_name}: not a supported image format (jpg/jpeg/png/gif/webp)")

# Execute the graph with multi-modal input
result = graph(content_blocks)
