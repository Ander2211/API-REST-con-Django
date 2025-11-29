# Inventario API (Django REST)

Proyecto mínimo para exponer la tabla `productos` mediante una API REST y conectar con la base de datos MySQL del dump `inventario_prueba.sql`.

Este README incluye instrucciones de instalación, importación del dump y ejemplos de cómo consumir los endpoints desde un front (fetch/axios), curl y notas útiles (CORS, autenticación básica).

## Setup rápido (PowerShell)

```powershell
# 1) Crear y activar virtualenv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Actualizar pip e instalar dependencias mínimas
python -m pip install --upgrade pip
pip install -r requirements.txt

# Si quieres instalar sólo REST framework y un driver PyMySQL rápido:
pip install djangorestframework PyMySQL

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

## Endpoints disponibles

- `GET /api/productos/?name=<texto>`
	- Búsqueda aproximada por nombre usando `icontains` (case-insensitive). Por ejemplo `?name=azucar` retornará cualquier producto que contenga la palabra "azucar" en su `nombre`.
- `GET /api/productos/?barcode=<codigo>`
	- Búsqueda por `codigo_barra` con igualdad exacta.

Ejemplo de respuesta (JSON):

```json
[
	{
		"id": 2,
		"nombre": "Libra de Azúcar Flecha Azul",
		"codigo_barra": "7591231391321",
		"precio": 0.5,
		"stock": 112
	}
]
```

> Nota: actualmente la vista devuelve todos los resultados que cumplen el filtro. Para tablas grandes se recomienda añadir paginación (DRF pagination) o límites.

## Ejemplos de consumo desde un Frontend

Los ejemplos usan la ruta base `http://localhost:8000/api/productos/`.

- Buscar por nombre (texto parcial)

curl (línea de comandos):

```bash
curl "http://localhost:8000/api/productos/?name=azucar"
```

JavaScript `fetch` (vanilla):

```javascript
const query = encodeURIComponent('azucar');
fetch(`http://localhost:8000/api/productos/?name=${query}`)
	.then(res => res.json())
	.then(data => console.log(data))
	.catch(err => console.error(err));
```

Axios (ejemplo en React):

```javascript
import axios from 'axios';

async function buscarPorNombre(texto) {
	const res = await axios.get('http://localhost:8000/api/productos/', {
		params: { name: texto }
	});
	return res.data; // array de productos
}

// uso
buscarPorNombre('azucar').then(items => console.log(items));
```

- Buscar por código de barras (igualdad exacta)

```bash
curl "http://localhost:8000/api/productos/?barcode=7501031311309"
```

Fetch:

```javascript
fetch('http://localhost:8000/api/productos/?barcode=7501031311309')
	.then(r => r.json())
	.then(data => console.log(data));
```

Axios:

```javascript
axios.get('http://localhost:8000/api/productos/', { params: { barcode: '7501031311309' } })
	.then(res => console.log(res.data));
```

### Ejemplo práctico en React (hook sencillo)

```javascript
import { useEffect, useState } from 'react';
import axios from 'axios';

function useProductosPorNombre(texto) {
	const [items, setItems] = useState([]);
	useEffect(() => {
		if (!texto) return;
		let mounted = true;
		axios.get('/api/productos/', { params: { name: texto } })
			.then(r => { if (mounted) setItems(r.data); })
			.catch(() => { if (mounted) setItems([]); });
		return () => { mounted = false; };
	}, [texto]);
	return items;
}

export default useProductosPorNombre;
```

> Si usas un `create-react-app` en desarrollo, puedes configurar el `proxy` en `package.json` para evitar problemas CORS:

```json
// package.json
{
	"proxy": "http://localhost:8000"
}
```

## Notas sobre CORS y despliegue

- Si tu frontend está en un dominio distinto al backend necesitarás permitir CORS. Una solución rápida en Django es instalar `django-cors-headers`:

```powershell
pip install django-cors-headers
```

Luego en `settings.py` añadir a `INSTALLED_APPS` y `MIDDLEWARE`, y configurar `CORS_ALLOW_ALL_ORIGINS = True` o `CORS_ALLOWED_ORIGINS = [...]`.

## Seguridad y siguientes mejoras

- Si vas a exponer la API públicamente, añade autenticación (Token, JWT o sesiones) y permisos en DRF.
- Añadir paginación, límites y validación de parámetros.
- Para búsquedas más "fuzzy" (errores tipográficos) considera usar extensiones de la base de datos (trigram, fuzzystrmatch) o integrar un motor de búsqueda (Elasticsearch / Meilisearch).

## Resumen rápido

- Ejecuta `python manage.py runserver` y prueba los endpoints en `http://localhost:8000/api/productos/`.
- Usa `?name=` para búsqueda parcial por nombre y `?barcode=` para búsqueda por código de barras exacta.

## Crear, actualizar y borrar (POST / PUT / PATCH / DELETE)

Además de las búsquedas y listados, la API soporta operaciones de escritura sobre los productos:

- `POST /api/productos/` — crear un producto.
- `GET /api/productos/<pk>/` — obtener un producto por su `id`.
- `PUT /api/productos/<pk>/` — reemplazar un producto (envía todos los campos).
- `PATCH /api/productos/<pk>/` — actualizar parcialmente un producto (envía solo los campos a cambiar).
- `DELETE /api/productos/<pk>/` — borrar un producto.

Ejemplos con `curl` (desde terminal):

# Crear (POST)
```bash
curl -X POST http://localhost:8000/api/productos/ \
	-H "Content-Type: application/json" \
	-d '{"nombre":"Snack Test","codigo_barra":"999888777666","precio":1.99,"stock":50}'
```

# Actualizar completamente (PUT)
```bash
curl -X PUT http://localhost:8000/api/productos/1/ \
	-H "Content-Type: application/json" \
	-d '{"nombre":"Snack Test Mod","codigo_barra":"999888777666","precio":2.49,"stock":40}'
```

# Actualizar parcialmente (PATCH)
```bash
curl -X PATCH http://localhost:8000/api/productos/1/ \
	-H "Content-Type: application/json" \
	-d '{"precio":2.99}'
```

# Borrar (DELETE)
```bash
curl -X DELETE http://localhost:8000/api/productos/1/
```

Respuestas y errores comunes

- 201 Created: respuesta esperada al crear con POST.
- 400 Bad Request: estructura JSON inválida o violación de restricciones (por ejemplo `codigo_barra` duplicado tiene una restricción UNIQUE en la tabla y producirá un error 400 con detalles).
- 404 Not Found: se intenta acceder a `/api/productos/<pk>/` con un `pk` que no existe.

Notas sobre CSRF y uso desde el navegador

- Si tu frontend hace peticiones con las credenciales de sesión (cookies), Django aplicará protección CSRF por defecto. Para peticiones `POST/PUT/PATCH/DELETE` desde el navegador con `fetch` o `axios`, necesitas enviar el encabezado `X-CSRFToken` (obtenido desde la cookie `csrftoken`) o usar un método de autenticación token (recomendado para APIs públicas/SPA).

Ejemplo con `fetch` (sin autenticación, útil cuando usas token Bearer):

```javascript
// Crear usando fetch + token Bearer
const token = 'TU_TOKEN_AQUI';
fetch('http://localhost:8000/api/productos/', {
	method: 'POST',
	headers: {
		'Content-Type': 'application/json',
		'Authorization': `Bearer ${token}`
	},
	body: JSON.stringify({ nombre: 'Snack Test', codigo_barra: '999888777666', precio: 1.99, stock: 50 })
})
	.then(r => r.json())
	.then(console.log)
	.catch(console.error);
```

Si usas sesiones (cookies) y CSRF, agrega el token a las cabeceras:

```javascript
// Obtener cookie csrftoken con una función auxiliar y usarla en headers
fetch('/api/productos/', {
	method: 'POST',
	credentials: 'include', // incluye cookies
	headers: {
		'Content-Type': 'application/json',
		'X-CSRFToken': getCookie('csrftoken')
	},
	body: JSON.stringify({ nombre: 'Snack Test', codigo_barra: '999888777660', precio: 1.5, stock: 20 })
});
```

Si prefieres evitar CSRF en desarrollo para probar desde un front local, puedes usar token authentication (por ejemplo JWT con `djangorestframework-simplejwt`) o temporalmente permitir `CORS_ALLOW_ALL_ORIGINS` y usar autorización por token en `Authorization` header.

Compatibilidad con la tabla existente

- El modelo `Product` mapea la tabla existente `productos` con `managed = False`, por lo que la API insertará/actualizará/borrará filas de esa tabla directamente. Asegúrate de que la tabla existe en la base de datos y que los campos requeridos (`nombre`, `codigo_barra`, `precio`) están presentes.


