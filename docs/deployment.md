# Despliegue de EcoBite

## 1. Infraestructura declarativa

La configuración del servicio de Render se mantiene en:

```
render.yaml
```

El archivo declara el servicio Docker, la rama `main`, el Dockerfile, el contexto de construcción, las variables de entorno requeridas y el health check.

Configuración relevante:

```yaml
type: web
runtime: docker
branch: main
dockerfilePath: ./Dockerfile
dockerContext: .
healthCheckPath: /health/
```

## 2. Construcción del contenedor

El proyecto utiliza un `Dockerfile` basado en:

```
python:3.13-slim
```

El contenedor instala las dependencias de Python y las librerías necesarias para Django, GeoDjango y PostgreSQL/PostGIS.

Gunicorn inicia la aplicación mediante:

```
gunicorn EcoBite.wsgi:application --bind 0.0.0.0:8000
```

## 3. Preparación al inicio

El Dockerfile utiliza `build.sh` como entrypoint.

El script:

1. Detecta la configuración de PostgreSQL cuando existe `DATABASE_URL`.
2. Espera la disponibilidad de PostgreSQL cuando corresponde.
3. Ejecuta las migraciones:

```
python manage.py migrate --noinput
```

4. Recolecta los archivos estáticos:

```
python manage.py collectstatic --noinput
```

5. Ejecuta el proceso recibido por el contenedor.

Esto permite que el contenedor realice la preparación necesaria antes de iniciar la aplicación.

## 4. Variables de entorno y secretos

Las variables sensibles no se almacenan como valores en el repositorio.

Entre las variables utilizadas se encuentran:

```
SECRET_KEY
DATABASE_URL
DEBUG
```

`render.yaml` declara las variables necesarias, mientras que los valores sensibles se proporcionan desde la configuración del servicio.

## 5. Health check

La aplicación incorpora:

```
/health/
```

La respuesta de la versión desplegada es:

```json
{
  "status": "ok",
  "service": "EcoBite",
  "version": "1.1.0"
}
```

Este endpoint permite comprobar disponibilidad y versión.

## 6. Proceso de despliegue

El flujo operativo es:

```
GitHub
   ↓
Tag SemVer
   ↓
GitHub Actions CD
   ↓
GHCR
   ↓
Imagen Docker
   ↓
Render
   ↓
EcoBite
   ↓
/health/
```

## 7. Verificación

Una vez desplegado el servicio se debe comprobar:

- Estado del servicio en Render.
- Logs de construcción e inicio.
- Disponibilidad de `/health/`.
- Versión reportada por el endpoint.
