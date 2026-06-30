# Mock appointments MCP server — Care Pal Lab 5, Part A.
# No authentication: synthetic workshop tool deployed once by the admin.
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY server.py .

# Azure Container Apps injects PORT; default 8000 for local runs.
ENV PORT=8000
EXPOSE 8000
CMD ["python", "server.py"]
