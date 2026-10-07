# Integración Continua y Entrega Continua (CI/CD)

## 1. Integración Continua

La integración continua se implementa mediante:

```
.github/workflows/ci.yml
```

El workflow se ejecuta en Pull Requests y en las ramas configuradas para desarrollo.

### Etapas principales

1. Configuración del entorno Python 3.13.
2. Instalación de las dependencias del proyecto.
3. Instalación de dependencias del sistema necesarias para GeoDjango.
4. Disponibilidad de PostgreSQL/PostGIS mediante un servicio de GitHub Actions.
5. Ejecución de:

```
python manage.py check
```

6. Aplicación de migraciones:

```
python manage.py migrate --noinput
```

7. Ejecución de las pruebas:

```
python manage.py test
```

8. Construcción de la imagen:

```
docker build -t ecobite:ci .
```

El objetivo es detectar problemas antes de integrar los cambios en `main`.

## 2. Entrega Continua

La entrega continua se implementa mediante:

```
.github/workflows/cd.yml
```

El workflow se activa mediante tags que siguen Semantic Versioning:

```
vMAJOR.MINOR.PATCH
```

Ejemplos utilizados:

```
v1.0.0
v1.1.0
```

El pipeline utiliza Docker y GitHub Container Registry para construir y publicar la imagen correspondiente a la versión.

## 3. Flujo completo

```
feature/*
   ↓
Pull Request
   ↓
CI
   ├── Django check
   ├── PostgreSQL/PostGIS
   ├── Migraciones
   ├── Tests
   └── Docker build
   ↓
main
   ↓
Tag vX.Y.Z
   ↓
CD
   ↓
GHCR
   ↓
Imagen Docker
   ↓
Render
```

## 4. Versionamiento del artefacto

Las versiones del proyecto se mantienen mediante tags Git y archivos de documentación como `VERSION` y `CHANGELOG.md`.

La versión `1.1.0` incorpora además la versión en la respuesta del endpoint `/health/`, permitiendo verificar qué versión está ejecutándose.

## 5. Evidencias recomendadas

Para demostrar CI/CD se recomienda conservar:

- Ejecución exitosa de CI.
- Ejecución exitosa de CD.
- Pull Request asociado al cambio.
- Release/tag SemVer.
- Imagen publicada en GHCR.
- Servicio desplegado en Render.
