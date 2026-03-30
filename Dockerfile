FROM python:3.10-slim

WORKDIR /app

COPY . .

# Install the project and dependencies from pyproject.toml
# The -e flag ensures [project.scripts] entry points are registered
RUN pip install --no-cache-dir -e .

EXPOSE 7860

CMD ["uvicorn", "api_debug_openenv.server.app:app", "--host", "0.0.0.0", "--port", "7860"]