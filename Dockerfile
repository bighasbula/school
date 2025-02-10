FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
    

ENV BOT_TOKEN='7638889053:AAEImpNVav_UvU7xfPg1JrLkli5LYJcN2f0'
ENV YOUR_CHAT_ID=1249376888
CMD ["python", "bot.py"]