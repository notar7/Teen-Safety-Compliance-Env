FROM public.ecr.aws/docker/library/python:3.11.13-slim-bookworm

# Set working directory
WORKDIR /app

# Install dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir --retries 5 --timeout 120 -r requirements.txt

# Copy project files
COPY . .

# HuggingFace Spaces requires port 7860
EXPOSE 7860

# Start FastAPI server
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
