FROM python:3.8

WORKDIR /app

# Skopiuj pliki wymagane dla projektu Django
COPY . /app

# Zainstaluj biblioteki z pliku requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]