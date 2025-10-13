# 🧰 DevTools - Hello World SpA

Repositorio central de guías, comandos y scripts de utilidad para el equipo de desarrollo.

---

## 📂 Estructura del Repositorio

```
devtools/
├── scripts/              # Scripts de utilidad y automatización
│   └── po_translator.py  # Traductor automático de archivos .po con IA
├── docs/
│   └── guides/          # Guías técnicas y tutoriales
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

**Uso básico:**

```bash
# Instalar dependencias
pip install polib beautifulsoup4 openai python-dotenv

# Configurar API key en .env
echo "DEEPSEEK_API_KEY=sk-xxxxx" >> .env

# Modo simulación (recomendado primero)
python scripts/po_translator.py --locale-path locale --dry-run

# Traducir todos los archivos .po
python scripts/po_translator.py --locale-path locale --batch-size 10

# Traducir un archivo específico
python scripts/po_translator.py --file locale/en/LC_MESSAGES/django.po
```

**Ver documentación completa:** [scripts/po_translator.py](scripts/po_translator.py)

---

## 📚 Guías Disponibles

_Próximamente: Guías técnicas sobre Django, Docker, Git, CI/CD y más..._

---

## 🤝 Contribuir

1. Crea una rama para tu guía o script:
   ```bash
   git checkout -b feature/nueva-guia
   ```

2. Agrega tu contenido en la carpeta apropiada:
   - Scripts → `scripts/`
   - Guías → `docs/guides/`

3. Haz commit y push:
   ```bash
   git add .
   git commit -m "docs: agregar guía de [tema]"
   git push origin feature/nueva-guia
   ```

4. Crea un Pull Request

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

## 📚 Referencias

- Enlace 1
- Enlace 2
```

---

## 🔗 Enlaces Útiles

- **Organización GitHub:** [Hello-World-SpA](https://github.com/Hello-World-SpA)
- **Team Developers:** Acceso con permisos de escritura

---

## 📞 Contacto

¿Tienes dudas o sugerencias? Abre un [Issue](https://github.com/Hello-World-SpA/devtools/issues) en este repositorio.

---

**Última actualización:** 13 Oct 2025