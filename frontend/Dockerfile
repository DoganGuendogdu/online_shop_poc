FROM python:3.11-slim

WORKDIR /frontend

RUN mkdir -p /frontend/app/src

COPY ./app/src /frontend/app/src

COPY requirements.txt /frontend

COPY config.json /frontend

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "app/src/main.py", "--server.address=0.0.0.0", "--server.port=8501"]
