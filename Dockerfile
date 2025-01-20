FROM python:3.10.16-slim

RUN mkdir -p /numbeo-scraper

WORKDIR /numbeo-scraper

RUN pip install --no-cache-dir -U pip

COPY . .

RUN pip install -r requirements.txt

CMD ["bash"]