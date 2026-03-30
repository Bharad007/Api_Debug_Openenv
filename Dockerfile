FROM python:3.10-slim

WORKDIR /app

COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 🔴 THIS IS THE CRITICAL LINE 🔴
# Install the project so [project.scripts] is registered
RUN pip install --no-cache-dir .

EXPOSE 7860

CMD ["uvicorn", "api_debug_openenv.server.app:app", "--host", "0.0.0.0", "--port", "7860"]