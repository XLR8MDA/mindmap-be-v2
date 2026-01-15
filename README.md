### **Backend (`mindmap-backend/README.md`)**
```markdown
# Mindmap AI - Backend

This is the FastAPI-based backend for the Mindmap AI application. It processes user queries, generates structured mindmap data using the Groq API, and returns Markdown compatible with Markmap.js.

---

## Features

- **AI-Powered Mindmap Generation**: Leverages the Groq API to transform queries into Markdown-formatted mindmaps.
- **RESTful API**: Provides an endpoint for the frontend to request mindmap data.
- **Extensible Architecture**: Easy to modify or add new API endpoints.

---

## Project Structure

```plaintext
mindmap-backend/
│
├── main.py              # FastAPI app entry point
├── groq_client.py       # Handles Groq API interactions
├── schemas.py           # Data models for backend
├── requirements.txt     # Python dependencies
├── system_prompt.txt    # AI system prompt for generating mindmaps
├── pyproject.toml       # Backend configuration
├── test.ipynb           # Notebook for backend testing
├── .env                 # Environment variables (e.g., GROQ_API_KEY)
└── README.md            # Documentation
```

---

## Installation

### Prerequisites

- Python 3.9+
- `uv` package manager or `pip` (for dependency management)

### Setup

1. **Navigate to the Backend Folder**:
   ```bash
   cd mindmap-backend
   ```

2. **Set Up the Package Manager**:
   Ensure you have `uv` installed (or use pip if preferred).

3. **Install Dependencies**:
   Using `uv`:
   ```bash
   uv install
   ```
   Or using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the `mindmap-backend` folder with the following:
   ```plaintext
   GROQ_API_KEY=your_api_key_here
   ```

5. **Run the Development Server**:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be available at `http://localhost:8000`.

---

## API Details

### Endpoint: `/generate-mindmap`

- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "query": "How to prepare for a marathon"
  }
  ```
- **Response**:
  ```json
  {
    "markdown": "# Preparing for a Marathon\n\n## Introduction\n..."
  }
  ```
- **Description**:
  Transforms the query into a hierarchical Markdown string suitable for Markmap.js.

---

## Configuration

### Environment Variables

The backend requires a `.env` file to store sensitive information like the Groq API key. Example:
```plaintext
GROQ_API_KEY=your_api_key_here
```

Ensure this file is listed in `.gitignore` to prevent accidental exposure in version control.

---

## Deployment

1. **Choose a Hosting Platform**:
   Deploy the backend to a platform like:
   - [Render](https://render.com/)
   - [Railway](https://railway.app/)
   - [Fly.io](https://fly.io/)

2. **Start Command**:
   Configure the hosting service to use the following start command:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. **Environment Variables**:
   Add the `GROQ_API_KEY` to the hosting platform's environment variable settings.

---

## Technology Stack

- **Framework**: FastAPI
- **Language**: Python 3.9+
- **AI Integration**: Groq API
- **Hosting**: Render, Railway, or Fly.io

---

## Testing

Use the provided `test.ipynb` file to validate the backend:
- Test the `/generate-mindmap` endpoint.
- Ensure proper handling of edge cases and errors.

---

## Contributing

1. **Fork the Repository**:
   Click the "Fork" button on the repository page.

2. **Create a New Branch**:
   ```bash
   git checkout -b feature-name
   ```

3. **Commit Your Changes**:
   ```bash
   git commit -m "Add feature"
   ```

4. **Push and Create Pull Request**:
   ```bash
   git push origin feature-name
   ```

---

## License

This project is licensed under the MIT License. See the main repository's [LICENSE](../LICENSE) file for details.
```

---
