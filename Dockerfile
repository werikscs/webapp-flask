FROM python:3.12-slim-bullseye
WORKDIR /app
COPY . .
RUN apt-get update
RUN pip install -r requirements.txt
RUN apt-get install -y libgl1-mesa-glx
CMD ["python", "main.py"]