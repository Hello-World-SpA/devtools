# 🧰 DevTools - Hello World SpA

Repositorio central de guías, comandos y scripts de utilidad para el equipo de desarrollo.

---

## 📂 Estructura del Repositorio

```
devtools/
├── scripts/                        # Scripts de utilidad y automatización
│   ├── po_translator.py            # Traductor automático de archivos .po con IA
│   └── requirements-translator.txt # Dependencias para po_translator.py
├── docs/
│   └── guides/                     # Guías técnicas y tutoriales
│       └── PO_TRANSLATOR_GUIDE.md  # Guía completa del traductor
└── README.md
```

---

## 🛠️ Scripts Disponibles

### 📝 `po_translator.py` - Traductor de archivos .po con IA

Script para traducir automáticamente archivos `.po` de Django usando DeepSeek API.

**Características:**
- ✅ Traduce texto simple y HTML preservando etiquetas
- ✅ Procesa archivos `.po` completos en lotes
- ✅ Crea backups automáticos antes de modificar
- ✅ Detecta y traduce solo entradas vacías o fuzzy
- ✅ Preserva nombres propios, marcas y términos técnicos
- ✅ Modo `--dry-run` para simular sin hacer cambios
- ✅ Soporta inglés (EN) y portugués (PT)

#### 🚀 Inicio Rápido

**1. Instalar dependencias:**

```bash
pip install -r scripts/requirements-translator.txt
```

**Dependencias instaladas:**
- `openai>=1.0.0` - Cliente OpenAI para DeepSeek API
- `polib>=1.2.0` - Manejo de archivos .po
- `beautifulsoup4>=4.12.0` - Parsing de HTML
- `lxml>=4.9.0` - Parser HTML adicional
- `python-dotenv>=1.0.0` - Variables de entorno desde .env

**2. Configurar API key:**

```bash
# Opción A: Variable de entorno
export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Opción B: Archivo .env en tu proyecto Django
echo "DEEPSEEK_API_KEY=sk-xxxxx" >> .env
```

**3. Traducir archivos .po:**

```bash
# Modo simulación (recomendado primero)
python scripts/po_translator.py --locale-path locale --dry-run

# Traducir todos los archivos .po
python scripts/po_translator.py --locale-path locale --batch-size 10

# Traducir un archivo específico
python scripts/po_translator.py --file locale/en/LC_MESSAGES/django.po
```

#### 📖 Documentación Completa

**Ver la guía completa con ejemplos, troubleshooting y flujo paso a paso:**

👉 **[Guía Completa del Traductor](docs/guides/PO_TRANSLATOR_GUIDE.md)**

---

## 📚 Guías Disponibles

- **[PO_TRANSLATOR_GUIDE.md](docs/guides/PO_TRANSLATOR_GUIDE.md)** - Guía completa del traductor de archivos .po

_Próximamente: Más guías técnicas sobre Django, Docker, Git, CI/CD y más..._

---

## 🤝 Contribuir

**Importante:** Este repositorio tiene permisos de **solo lectura** para el team developers.

Si deseas contribuir:

1. **Haz un fork del repositorio:**
   ```bash
   # Desde GitHub, click en "Fork"
   ```

2. **Clona tu fork:**
   ```bash
   git clone https://github.com/TU-USUARIO/devtools.git
   cd devtools
   ```

3. **Crea una rama para tu contribución:**
   ```bash
   git checkout -b feature/nueva-guia
   ```

4. **Agrega tu contenido:**
   - Scripts → `scripts/`
   - Guías → `docs/guides/`

5. **Haz commit y push a tu fork:**
   ```bash
   git add .
   git commit -m "docs: agregar guía de [tema]"
   git push origin feature/nueva-guia
   ```

6. **Crea un Pull Request:**
   - Ve a tu fork en GitHub
   - Click en "Pull Request"
   - Selecciona `Hello-World-SpA/devtools` como base

---

## 📋 Template para Nuevas Guías

```markdown
# 📘 Título de la Guía

**Fecha:** YYYY-MM-DD
**Autor:** Tu Nombre
**Nivel:** Básico/Intermedio/Avanzado

## 🎯 Objetivo

Descripción breve del objetivo de la guía.

## 📋 Prerequisitos

- Requisito 1
- Requisito 2

## 📝 Paso a Paso

### Paso 1: Título del Paso

Descripción y comandos...

### Paso 2: Título del Paso

Descripción y comandos...

## ✅ Verificación

Cómo verificar que funcionó correctamente.

## 🔍 Troubleshooting

Problemas comunes y soluciones.

## 📚 Referencias

- Enlace 1
- Enlace 2
```

---

## 🔗 Enlaces Útiles

- **Organización GitHub:** [Hello-World-SpA](https://github.com/Hello-World-SpA)
- **Team Developers:** Acceso de solo lectura
- **Issues:** [Reportar problemas](https://github.com/Hello-World-SpA/devtools/issues)

---

## 📞 Contacto

¿Tienes dudas o sugerencias? Abre un [Issue](https://github.com/Hello-World-SpA/devtools/issues) en este repositorio.

---

**Última actualización:** 13 Oct 2025