FROM python:3.12-slim

WORKDIR /app

# Build arg to optionally install heavy ML deps
ARG INSTALL_ML=false

COPY requirements.txt .
# Include the optional file so it is available at build time
COPY requirements-ml.txt requirements-ml.txt

# Install core requirements, and install optional ML packages only when INSTALL_ML=true
RUN pip install --no-cache-dir -r requirements.txt \
    && if [ "$INSTALL_ML" = "true" ]; then pip install --no-cache-dir -r requirements-ml.txt; fi

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
