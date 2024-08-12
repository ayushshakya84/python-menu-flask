FROM python:3.12.3-alpine
WORKDIR /app
COPY . .
RUN pip install gunicorn
RUN pip install -r requirements.txt
ENV PORT=80
CMD ["python" "main.py"]