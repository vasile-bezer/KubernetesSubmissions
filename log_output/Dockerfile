
FROM python:3.11-slim

# Keep Python output unbuffered so logs show up immediately
ENV PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTECODE=1 \
	APP_HOME=/app

WORKDIR $APP_HOME

COPY . $APP_HOME

RUN pip install --no-cache-dir -r requirements.txt

#-u ensures unbuffered output
CMD ["python", "-u", "__main__.py"]

