# Evidencia de evaluación DevOps

## Objetivo

Este documento define las evidencias que deben conservarse para demostrar la implementación del flujo DevOps de EcoBite.

Las capturas deben mostrar, cuando sea posible, el nombre del repositorio, rama, commit, tag, fecha y resultado de la operación.

## 1. Repositorio y estructura

**Captura:** página principal de GitHub.

Debe permitir identificar:

- Repositorio `ElTioMuffin/EcoBite-DevOps`.
- Estructura del proyecto.
- `Dockerfile`.
- `render.yaml`.
- `.github/workflows/`.
- Documentación.

**Criterios demostrados:** uso de Git, estructura y documentación.

## 2. Estrategia de ramas y protección

**Captura:** configuración de protección de `main`.

Debe evidenciar las restricciones configuradas para evitar cambios directos no controlados.

**Criterios demostrados:** estrategia de ramas y protección del código.

## 3. Pull Requests

**Captura:** listado de Pull Requests.

Debe mostrar los cambios integrados mediante Pull Requests y, cuando corresponda, el resultado de los checks.

**Criterios demostrados:** revisión/integración y trazabilidad.

## 4. Integración Continua

**Captura:** ejecución exitosa de `CI`.

Debe evidenciar:

- Django check.
- PostgreSQL/PostGIS.
- Migraciones.
- Tests.
- Docker build.

**Criterios demostrados:** pipeline como código, validaciones automatizadas y build.

## 5. Entrega Continua

**Captura:** ejecución exitosa de `CD` asociada a un tag SemVer.

Para la versión actual se recomienda utilizar `v1.1.0`.

**Criterios demostrados:** entrega automatizada y versionamiento.

## 6. Releases

**Captura:** página de Releases.

Debe mostrar las versiones:

```
v1.0.0
v1.1.0
```

**Criterios demostrados:** versionamiento y trazabilidad.

## 7. GitHub Container Registry

**Captura:** GitHub Packages.

Debe mostrar la imagen Docker de EcoBite y las etiquetas publicadas, incluyendo `latest` y las etiquetas SemVer disponibles.

**Criterios demostrados:** registro de artefactos y publicación de imágenes.

## 8. Infraestructura como código

**Captura:** `render.yaml` en el repositorio.

Debe permitir identificar la definición declarativa del servicio, Dockerfile, rama, health check y variables de entorno.

**Criterios demostrados:** infraestructura como código.

## 9. Render

**Captura:** servicio desplegado en Render.

Debe mostrar que el servicio está desplegado y operativo.

**Criterios demostrados:** despliegue cloud y ejecución del contenedor.

## 10. Health check

**Captura:** endpoint:

```
/health/
```

La respuesta esperada para la versión actual es:

```json
{
  "status": "ok",
  "service": "EcoBite",
  "version": "1.1.0"
}
```

**Criterios demostrados:** disponibilidad del servicio y verificación de la versión desplegada.

## 11. Pruebas automatizadas

**Captura:** resultado de los tests dentro de GitHub Actions.

Debe evidenciar que las pruebas se ejecutan como parte del pipeline y no únicamente de manera manual.

**Criterios demostrados:** automatización de pruebas.

## 12. Orden recomendado para el informe

Se recomienda incorporar las evidencias en este orden:

1. Repositorio.
2. Protección de `main`.
3. Pull Requests.
4. CI.
5. CD.
6. Releases.
7. GHCR.
8. `render.yaml`.
9. Render.
10. `/health/`.

## 13. Regla de trazabilidad

Cada captura debe acompañarse de una breve explicación que indique qué demuestra y, cuando resulte visible, la relación entre:

```
Cambio
 ↓
Pull Request
 ↓
Commit
 ↓
Tag
 ↓
Pipeline
 ↓
Imagen
 ↓
Despliegue
```

Esto permite relacionar el código fuente con el artefacto y el servicio desplegado.
