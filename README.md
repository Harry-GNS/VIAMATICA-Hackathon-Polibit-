# 🏥 VIAMATICA HACKATHON — Reto 3
## Estimador Agéntico de Copago y Cobertura para el Paciente

Sistema conversacional impulsado por IA que ayuda a los pacientes a comprender su cobertura médica antes de atenderse.

El agente interpreta síntomas ingresados por el usuario, sugiere la especialidad médica adecuada y calcula el copago estimado según el plan de seguro del paciente. Además, recomienda el hospital de la red más conveniente económicamente.

---

# ✨ Objetivo

Reducir la incertidumbre de los pacientes al momento de utilizar su seguro médico mediante un asistente inteligente capaz de:

- Interpretar síntomas mediante IA
- Recomendar especialidades médicas
- Consultar cobertura del seguro
- Calcular copagos estimados
- Recomendar hospitales de la red
- Explicar de forma clara cómo se calcula el beneficio

---

# 🧠 Flujo del Sistema

1. El paciente ingresa un síntoma o consulta
2. La IA analiza el mensaje
3. El sistema identifica la especialidad médica sugerida
4. Se consulta la cobertura del plan
5. Se calcula el copago estimado
6. Se recomiendan hospitales disponibles
7. El agente responde de forma conversacional

---

# 🏗️ Arquitectura del Proyecto

```bash
VIAMATICA-HACKATHON/
│
├── assets/        # Recursos visuales e imágenes
├── backend/       # API y lógica principal
├── data/          # Datos mock de seguros, hospitales y coberturas
├── frontend/      # Interfaz del usuario
├── models/        # Modelos y esquemas
├── public/        # Archivos públicos
├── utils/         # Funciones auxiliares
│
├── .env.example   # Variables de entorno de ejemplo
├── .gitignore
├── README.md
└── requirements.txt

## 🚀 Características Principales

- ✅ Agente conversacional con IA
- ✅ Integración con Notion (planes de seguro)
- ✅ Cálculo automático de copagos
- ✅ Recomendación de especialidades
- ✅ Comparación de hospitales por costo

## 📋 Requisitos

- Python 3.10+
- API Key de Anthropic
- API Key de Notion
- Variables de entorno configuradas

## 🔧 Instalación

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env basado en .env.example
copy .env.example .env
# Luego llenar con tus API keys
```

## 🎮 Uso

```bash
python main.py
```
## 👨‍💻 Autor

Polibit 

## 📝 Licencia

Viamatica Hackathon 2026