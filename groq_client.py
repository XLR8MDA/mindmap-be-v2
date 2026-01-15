import os
import json
import logging
import traceback
from fastapi import HTTPException
from fastapi.responses import FileResponse
from groq import Groq
import instructor
from schemas import MindMapNode

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize Groq client
try:
    logger.info("Initializing Groq client.")
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    client = instructor.patch(client)
    logger.info("Groq client initialized and patched successfully.")
except Exception as e:
    logger.error("Error initializing Groq client.", exc_info=True)
    raise e

# Load the prompt
try:
    logger.info("Loading system prompt from file.")
    prompt = open("system_prompt.txt", "r").read()
    logger.info("System prompt loaded successfully.")
except FileNotFoundError as e:
    logger.error("System prompt file not found.", exc_info=True)
    raise e
except Exception as e:
    logger.error("Error loading system prompt.", exc_info=True)
    raise e



def generate_mindmap(query: str) -> str:
    """
    Generates a mind map based on a user query using Groq API.

    Args:
        query (str): The user input query.

    Returns:
        str: The path to the saved Markdown file.
    """
    try:
        logger.info(f"Received query to generate mind map: {query}")
        
        # Fetch the response from Groq
        logger.info("Sending request to Groq API.")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": query}],
            response_model=MindMapNode,
        )
        logger.info("Response received from Groq API.")
        return response
    except Exception as e:
        error_trace = traceback.format_exc()
        logger.error("Error occurred during mind map generation:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error generating mind map: {e}\nTraceback has been logged."
        )

