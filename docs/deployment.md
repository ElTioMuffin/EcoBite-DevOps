# Despliegue

Render usa `render.yaml` para definir el servicio Docker. El servicio ejecuta migraciones como paso previo y utiliza el health check `/`.

Las variables `SECRET_KEY` y `DATABASE_URL` se configuran fuera del repositorio.
