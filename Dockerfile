FROM python:3.9.19-alpine3.19

LABEL authors="pradyumna,arun,abhimanyu,swarangi"

WORKDIR /src

COPY requirements.txt .
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY righttoknow/ righttoknow/

EXPOSE 8000
ENV FLAVOUR=production
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-n", "righttoknow", "righttoknow.__init__:create_app()"]
