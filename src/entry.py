from js import Response, Headers, fetch, Request
import json

# Embedded system prompt to ensure reliability in Worker environment
SYSTEM_PROMPT = """
**Prompt for LLM:**

You are an assistant that generates structured responses in Markdown format compatible with `mindmap.js`. Always format your responses using nested headings (`#`, `##`, `###`, etc.) to represent hierarchical information. Do not use bullet points, dashes, or any other list symbols. Instead, structure all content strictly as nested headings.

### Guidelines:

1. **Structure:**  
   - Use `#` for the main topic, `##` for subtopics, `###` for further details, and so on.
   - Each sub-node must use a progressively deeper heading level.

2. **Consistency:**  
   - Ensure that the hierarchy is clear and logically organized.
   - Avoid redundant or irrelevant information.

3. **Content Style:**  
   - Write concise and actionable content for each node.
   - Use clear, straightforward language.

4. **Compatibility:**  
   - Ensure that the response is fully compatible with `mindmap.js` by strictly adhering to the nested heading structure.

### Example:

```markdown
# Main Topic

## Subtopic 1
### Detail 1
#### Key Point 1
##### Explanation or Example
#### Key Point 2
##### Explanation or Example

### Detail 2
#### Key Point 1
##### Explanation or Example
#### Key Point 2
##### Explanation or Example

## Subtopic 2
### Detail 1
#### Instruction 1
##### Further Explanation
#### Instruction 2
##### Further Explanation
```

Now, apply this structure to any topic or query requested.
"""

def create_cors_headers():
    h = Headers.new()
    h.set("Access-Control-Allow-Origin", "*")
    h.set("Access-Control-Allow-Methods", "POST, OPTIONS")
    h.set("Access-Control-Allow-Headers", "Content-Type")
    return h

async def on_fetch(request, env):
    # Handle CORS (Options request)
    if request.method == "OPTIONS":
        return Response.new("", headers=create_cors_headers())

    if request.url.endswith("/generate-mindmap") and request.method == "POST":
        try:
            # 1. Get Secret Key
            try:
                api_key = env.GROQ_API_KEY
            except:
                api_key = env["GROQ_API_KEY"]
            
            if not api_key:
                return Response.new(json.dumps({"error": "GROQ_API_KEY not found in environment"}), status=500, headers=create_cors_headers())

            # 2. Parse Body
            body_json = await request.json()
            # body_json might be a JS Object, convert safely
            try:
                query = str(body_json.query)
            except:
                query = str(body_json["query"])
            
            if not query:
                return Response.new(json.dumps({"error": "Missing query"}), status=400, headers=create_cors_headers())

            # 3. Prepare Groq Request
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": query}
                ]
            }
            
            groq_headers = Headers.new()
            groq_headers.set("Authorization", f"Bearer {api_key}")
            groq_headers.set("Content-Type", "application/json")
            
            # 4. Fetch from Groq
            groq_request = Request.new(
                "https://api.groq.com/openai/v1/chat/completions",
                method="POST",
                headers=groq_headers,
                body=json.dumps(payload)
            )
            
            response = await fetch(groq_request)
            
            if not response.ok:
                error_text = await response.text()
                return Response.new(
                    json.dumps({"error": f"Groq API error: {error_text}"}),
                    status=response.status,
                    headers=create_cors_headers()
                )

            data = await response.json()
            
            # Extract content safely from poly-type response
            try:
                # Try JS object-style access
                content = data.choices[0].message.content
            except:
                # Try dict-style access
                content = data["choices"][0]["message"]["content"]
            
            # 5. Return success
            res_headers = create_cors_headers()
            res_headers.set("Content-Type", "application/json")
            return Response.new(
                json.dumps({"markdown": content}),
                headers=res_headers
            )

        except Exception as e:
            # Final fallback for any error
            err_headers = create_cors_headers()
            err_headers.set("Content-Type", "application/json")
            return Response.new(
                json.dumps({"error": f"Internal Error: {str(e)}"}),
                status=500,
                headers=err_headers
            )

    return Response.new("Not Found", status=404)
