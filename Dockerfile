FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port required by Hugging Face Spaces
EXPOSE 7860

# Start the FastAPI app using the packaged module
CMD ["uvicorn", "api_debug_openenv.server.app:app", "--host", "0.0.0.0", "--port", "7860"]
