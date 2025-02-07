FROM python:3.11-slim

WORKDIR /frontend

RUN mkdir -p /frontend/app/

COPY ./app /frontend/app

COPY requirements.txt /frontend

COPY config.json /frontend

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "app/main.py", "--server.address=0.0.0.0", "--server.port=8501"]
