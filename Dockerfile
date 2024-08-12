FROM python:3.12.3-alpine3.20
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn
COPY . .
ENV PORT=80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "main:app"]
