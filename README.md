# Inventario API (Django REST)

Proyecto mínimo para exponer la tabla `productos` mediante una API REST y conectar con la base de datos MySQL del dump `inventario_prueba.sql`.

Setup rápido (PowerShell):

```powershell
# 1) Crear y activar virtualenv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Instalar dependencias
pip install --upgrade pip
python -m pip install djangorestframework
pip install -r requirements.txt

# 3) Crear DB e importar el dump (si aún no lo has hecho)
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS inventario_prueba;"
mysql -u root -p inventario_prueba < inventario_prueba.sql

# 4) Variables de entorno necesarias (ejemplo)
$env:DB_NAME='inventario_prueba';
$env:DB_USER='root';
$env:DB_PASSWORD='tu_password';
$env:DB_HOST='127.0.0.1';
$env:DB_PORT='3306';
$env:SECRET_KEY='cambiar_esto';
$env:DEBUG='1';

# 5) Ejecutar servidor
python manage.py runserver
```

Endpoints:

- `GET /api/productos/?name=<texto>` - busca por nombre usando coincidencia parcial (case-insensitive).
- `GET /api/productos/?barcode=<codigo>` - busca por código de barras (igualdad exacta).

Notas:

- El modelo `Product` mapea la tabla existente `productos` con `managed = False`, por lo que no creará ni modificará la tabla con migraciones.
- Si deseas usar migraciones gestionadas por Django, cambia `managed = True` y crea las migraciones apropiadas.
