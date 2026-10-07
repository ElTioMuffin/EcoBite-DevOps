# EcoBite DevOps

Repositorio DevOps de EcoBite, aplicación web Django orientada a reducir el desperdicio de alimentos mediante packs sorpresa de comercios locales.

## Arquitectura

- Django 5.2.8
- GeoDjango/PostGIS
- Gunicorn
- Docker
- GitHub Actions
- GitHub Container Registry (GHCR)
- Render Blueprint

## Flujo

`feature/*` → Pull Request → CI → `main` → tag SemVer → CD → GHCR → despliegue.

## Contenedores

La imagen usa `python:3.13-slim`, instala las dependencias geoespaciales necesarias y ejecuta Gunicorn. El entrypoint ejecuta migraciones y `collectstatic` antes de iniciar la aplicación.

## CI

El workflow `.github/workflows/ci.yml` instala las dependencias, ejecuta `manage.py check`, migraciones y pruebas sobre PostgreSQL/PostGIS.

## CD

El workflow `.github/workflows/cd.yml` se activa con tags `vMAJOR.MINOR.PATCH` y publica la imagen en GHCR.

## Infraestructura

`render.yaml` define el servicio Docker, variables requeridas, health check y ejecución de migraciones antes del despliegue.

## Variables

Nunca subir secretos reales. Crear las variables `SECRET_KEY` y `DATABASE_URL` en el entorno de despliegue.

## Desarrollo

```bash
python -m venv .venv
pip install -r requirements.txt
python manage.py check
python manage.py test
python manage.py runserver
```

## Versionado

Se utiliza Semantic Versioning:

- `v1.0.0`: primera versión estable.
- `v1.1.0`: nueva funcionalidad compatible.
- `v1.1.1`: corrección compatible.

## Evidencia

Consultar `docs/evidence.md` para la lista de evidencias recomendadas para la evaluación DevOps.
