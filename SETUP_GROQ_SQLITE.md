# 🚀 GUÍA RÁPIDA DE SETUP - GROQ + SQLite

## ✨ Cambios Realizados

✅ **Reemplazado:**
- Anthropic Claude → **Groq API** (gratuito, muy rápido)
- Notion → **SQLite** (base de datos local, gratis)

✅ **Beneficios:**
- 🆓 100% gratuito
- ⚡ Super rápido (Groq es 2x más rápido que otros LLMs)
- 💾 Base de datos local (sin dependencias externas)
- 🔒 Tus datos en tu máquina

---

## 📋 Requisitos

- Python 3.10+
- pip

---

## 🔧 Instalación (5 minutos)

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Obtener API Key de Groq (GRATIS)

1. Ve a https://console.groq.com
2. Crea cuenta (gratis)
3. Copia tu API Key

### 3. Configurar `.env`

```bash
# Copiar archivo de ejemplo
copy .env.example .env
```

Edita `.env` y reemplaza:
```
GROQ_API_KEY=tu_api_key_aqui
```

### 4. Inicializar base de datos (OPCIONAL)
```bash
python init_database.py
```
*Nota: Se inicializa automáticamente al ejecutar `main.py` si está vacía*

### 5. ¡Listo! Ejecuta el servidor
```bash
python main.py
```

Verás:
```
🚀 Iniciando servidor en http://localhost:5000
✅ Agente inicializado correctamente con Groq + SQLite
```

---

## 🧪 Verificar Setup

```bash
python test_setup.py
```

Esto verifica:
- ✅ API Key configurado
- ✅ Dependencias instaladas
- ✅ Base de datos OK
- ✅ Agente funcionando

---

## 🎮 Usar la API

### Chat Endpoint
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tengo dolor de pecho"}'
```

### Health Check
```bash
curl http://localhost:5000/health
```

### Reset Conversación
```bash
curl -X POST http://localhost:5000/api/reset
```

---

## 📂 Estructura de Archivos (Nueva)

```
backend/
├── database/
│   ├── __init__.py
│   └── db_manager.py          ← NUEVO: SQLite Manager
├── agent/
│   └── copago_agent.py        ← Actualizado (Groq)
├── api/
│   └── app.py
└── integrations/
    └── hospital_data.py

data/
└── viamatica.db              ← Base de datos (se crea automáticamente)

init_database.py              ← NUEVO: Script de inicialización
test_setup.py                 ← NUEVO: Script de verificación
```

---

## 🔑 Variables de Entorno

```env
# API
GROQ_API_KEY=xxx              # Requerido (obtén en https://console.groq.com)

# Servidor
PORT=5000                     # Puerto (default 5000)
DEBUG=True                    # Modo debug (default True)

# Base de Datos
DATABASE_PATH=data/viamatica.db  # Ruta SQLite (default)
```

---

## ⚡ Modelos Disponibles en Groq

Groq ofrece estos modelos gratis con alta velocidad:
- `mixtral-8x7b-32768` ⭐ (recomendado - rápido, buen balance)
- `llama2-70b-4096`
- `gemma-7b-it`

*Actualmente usamos `mixtral-8x7b-32768`*

---

## 🐛 Troubleshooting

### "GROQ_API_KEY no configurado"
```
✅ Solución:
1. Ve a https://console.groq.com
2. Copia tu API key
3. Edita .env y agrega: GROQ_API_KEY=tu_key
```

### "ModuleNotFoundError: No module named 'groq'"
```
✅ Solución:
pip install -r requirements.txt
```

### "Base de datos no inicializa"
```
✅ Solución:
python init_database.py
```

---

## 📊 Base de Datos

### Tablas
- **hospitales**: Info de hospitales
- **especialidades**: Especialidades médicas
- **planes_seguro**: Planes de seguro
- **cobertura_especialidad**: Cobertura por plan/especialidad

### Datos de Ejemplo
Se cargan automáticamente con:
- 4 hospitales
- 5 especialidades
- 3 planes de seguro

### Agregar Datos Personalizados
```python
from backend.database.db_manager import DatabaseManager

db = DatabaseManager()
db.add_hospital(
    id="hosp_nuevo",
    nombre="Mi Hospital",
    red="Mi Red",
    copago_base=30
)
```

---

## 📞 Soporte Groq

- Docs: https://console.groq.com/docs
- Community: https://discord.gg/groq
- Free tier: Sin límite de solicitudes (con límite de rate)

---

## ✅ Checklist Final

- [ ] `pip install -r requirements.txt`
- [ ] `GROQ_API_KEY` configurado en `.env`
- [ ] `python test_setup.py` pasa todos los checks
- [ ] `python main.py` inicia correctamente
- [ ] Pruebas con curl o Postman

---

¡Listo! 🚀
