from pydantic import BaseModel
from pydantic import Field
from typing import List

class MindMapNode(BaseModel):
    markdown: str = Field(...,min_length=1, description="Always return Markdown content in markmap.js friendly format. Make it multi layer")


class QueryModel(BaseModel):
    query: str

# Define the response model
class MindMapResponse(BaseModel):
    markdown: str