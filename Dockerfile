FROM python:3.12-slim
WORKDIR /app

# primero se copian e instalan las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# después se incorpora el código de la aplicación
COPY src/ .

# usuario sin privilegios con permisos sobre el código
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
