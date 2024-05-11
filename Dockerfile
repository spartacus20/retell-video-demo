FROM python:3.11

WORKDIR /voice

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD python main.py
