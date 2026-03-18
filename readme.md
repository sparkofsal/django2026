# Videos ASM — Entrega Final (Avances 1–4)

## Descripción del proyecto
En este proyecto desarrollé un sistema llamado **Videos ASM** (Armando Salazar Martinez) para capturar información de usuarios, registrar  videos, administrarlos y guardar toda la información. La solución se construyó en 4 avances, siguiendo los requisitos del proyecto.

---

## Estructura del proyecto
Dentro de mi carpeta principal tengo esta estructura:

Videos ASM/
Avance 1/
Primera etapa.py
salida.txt
evidencias/
Avance 2/
Segunda etapa.py
salida.txt
evidencias/
Avance 3/
evidencias/
Mis videos/ <- Proyecto Django (aqui esta la app de videos)
manage.py
mis_videos/
settings.py
urls.py
videos_app/
models.py
views.py
forms.py
urls.py
templates/
videos_app/
index.html
static/
videos_app/
css/
styles.css
js/
validaciones.js
templatetags/
init.py
post_extras.py


Nota: En Avance 3 y 4 la base de datos es PostgreSQL y se llama **Pro_Gol** de acuerdo al requisito del PDF.

---

## Requisitos del proyecto por avance

### Avance 1 — Consola (Python)
- Capturar nómina (alfanumérico), nombre (solo letras), cantidad de videos (numérico).
- Confirmación Sí/No.
- Si Sí: capturar por video: título, nombre, extensión (alfanumérico) y tamaño (numérico, máximo 3MB).
- Guardar TODO en `salida.txt` en una sola línea separada por ` | `.
- Uso de validaciones, ciclos, funciones y excepciones.

### Avance 2 — POO (Python)
- Clases: `Persona` (nombre, nómina) y `Videos` (nombre, extensión, tamaño) con métodos de capturar e imprimir.
- Mantener la misma funcionalidad del Avance 1 y el mismo formato de `salida.txt`.

### Avance 3 — Django + PostgreSQL
- Proyecto Django: **Mis videos**
- Base de datos PostgreSQL: **Pro_Gol**
- Tablas: Usuario, Videos y relación Usuario–Video.
- Guardar toda la información en la base de datos.

### Avance 4 — Frontend HTML/CSS + Validaciones + Guardar a BD
- Pantallas HTML para capturar usuario y N videos.
- Mensaje de confirmación.
- Validaciones al salir del campo (evento blur).
- Botón Guardar que persiste en PostgreSQL.
- Utilizar CSS

---

## Cómo ejecutar cada avance (desde VS Code)

Trabaje todo desde la terminal integrada de VS Code y Windows; uso `py` (para Python launcher).

### Avance 1
**Ruta:** `Videos ASM/Avance 1/`

**Ejecutar:**
cd -- "C:\Users\salaz\Django2026\Videos ASM\Avance 1"
py "Primera etapa.py"

### Avance 2
**Ruta:** `Videos ASM/Avance 2/`
cd -- "C:\Users\salaz\Django2026\Videos ASM\Avance 2"
py "Segunda etapa.py"

### Avance 3
**Ruta:** `Videos ASM/Avance 3/Mis videos/`
cd -- "C:\Users\salaz\Django2026\Videos ASM\Avance 3"
.\.venv\Scripts\Activate.ps1
cd "Mis videos"

**Despues ejecuto el servidor**
py manage.py runserver

y se abre en http://127.0.0.1:8000/

### Avance 4
Configuración de Base de Datos (PostgreSQL)
Base de datos: Pro_Gol
Usuario: postgres
Puerto: 5432
Host: localhost
La conexión está configurada en mis_videos/settings.py usando el engine django.db.backends.postgresql.


**Para comprobar que se guardo en PostreSQL**
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -h localhost -d "Pro_Gol"

y dentro de psql
\dt
SELECT id, nomina, nombre FROM videos_app_usuario ORDER BY id DESC LIMIT 5;
SELECT id, usuario_id, titulo, nombre, extension, tamano_mb FROM videos_app_video ORDER BY id DESC LIMIT 10;
\q