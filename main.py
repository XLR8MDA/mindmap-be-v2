from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from schemas import  QueryModel
from groq_client import generate_mindmap
import os
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup: FastAPI server is initializing.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown: FastAPI server is shutting down.")


@app.get("/health")
def check_health():
    return 'OK'
    

@app.post("/generate-mindmap", response_model=dict)
def generate_mindmap_endpoint(query: QueryModel):
    """
    Endpoint to generate a mind map in Markdown format and save it as a file.
    """
    try:
        logger.info(f"Received request to generate mind map for query: {query.query}")
        # Generate mind map using the provided query
        response = generate_mindmap(query.query)
        logger.info("Mind map generation successful.")
        return {"markdown": response.markdown} 
    except Exception as e:
        logger.error(f"Error generating mind map: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate mind map.")



if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
