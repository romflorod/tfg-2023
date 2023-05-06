# Definir imagen base de Python
FROM python:3.9-slim-buster

# Copiar archivos de la aplicación al contenedor
WORKDIR /app
COPY . .

# Instalar dependencias
RUN pip install -r requirements.txt

# Configurar variable de entorno DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE=valorant.settings

# Ejecutar migraciones de Django
RUN python manage.py makemigrations
RUN python manage.py migrate

# Exponer puerto de la aplicación
EXPOSE 8000

# Comando de inicio
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
