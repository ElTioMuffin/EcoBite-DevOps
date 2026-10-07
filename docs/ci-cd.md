# CI/CD

CI se ejecuta en Pull Requests y ramas de desarrollo. Comprueba Django, instala dependencias, aplica migraciones y ejecuta tests con PostgreSQL/PostGIS.

CD se activa mediante tags SemVer y publica la imagen Docker en GHCR. El despliegue de Render se define declarativamente mediante `render.yaml`.
