# 🌍 Guía Completa: Traductor de Archivos .po con DeepSeek API

**Fecha:** 13 Oct 2025
**Autor:** Hello World SpA
**Nivel:** Intermedio

---

## 🎯 Objetivo

Traducir automáticamente archivos `.po` de Django usando la API de DeepSeek, aprovechando inteligencia artificial para obtener traducciones de alta calidad que preservan el contexto y respetan nombres propios, marcas y términos técnicos.

---

## 🚀 Características

- ✅ **Traducción inteligente**: Detecta automáticamente si el texto contiene HTML y usa el método apropiado
- ✅ **Segmentación con placeholders**: Maneja correctamente estructuras HTML complejas
- ✅ **Procesamiento por lotes**: Traduce múltiples entradas de forma eficiente
- ✅ **Backups automáticos**: Crea copias de seguridad antes de modificar archivos
- ✅ **Términos protegidos**: No traduce nombres propios, marcas, términos técnicos
- ✅ **Modo dry-run**: Simula la traducción sin hacer cambios
- ✅ **Soporte multi-idioma**: Inglés (EN) y Portugués (PT)

---

## 📋 Prerequisitos

### 1. Tener Python 3.8 o superior

```bash
python --version
# Python 3.8.0 o superior
```

### 2. API Key de DeepSeek

Solicitar la API key al líder del equipo o crear una en: https://platform.deepseek.com/

---

## 🔧 Instalación

### Paso 1: Clonar el repositorio devtools

```bash
cd /ruta/de/tu/proyecto
git clone https://github.com/Hello-World-SpA/devtools.git
```

### Paso 2: Instalar dependencias

```bash
cd devtools/scripts
pip install -r requirements-translator.txt
```

**Dependencias que se instalarán:**
- `openai>=1.0.0` - Cliente OpenAI para DeepSeek API
- `polib>=1.2.0` - Manejo de archivos .po
- `beautifulsoup4>=4.12.0` - Parsing de HTML
- `lxml>=4.9.0` - Parser HTML adicional (recomendado)
- `python-dotenv>=1.0.0` - Cargar variables de entorno desde .env

### Paso 3: Configurar API Key de DeepSeek

**Opción A - Variable de entorno (recomendado):**

```bash
export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Opción B - Archivo .env:**

```bash
# Crear archivo .env en la raíz de tu proyecto Django
echo "DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" > .env
echo "DEEPSEEK_API_URL=https://api.deepseek.com/v1" >> .env
```

**Opción C - Parámetro en línea de comandos:**

```bash
python po_translator.py --api-key "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

## 📖 Uso Básico

### 1. Modo dry-run (simulación) - RECOMENDADO primero

**Siempre ejecuta esto primero para ver qué se traducirá:**

```bash
# Desde el directorio raíz de tu proyecto Django
python /ruta/a/devtools/scripts/po_translator.py --dry-run
```

**Salida esperada:**

```
================================================================================
🌍 TRADUCTOR DE ARCHIVOS .PO CON DEEPSEEK
================================================================================
📁 Carpeta locale: locale
📄 Archivos encontrados: 2
   - locale/en/LC_MESSAGES/django.po
   - locale/pt/LC_MESSAGES/django.po
================================================================================

📁 Procesando: locale/en/LC_MESSAGES/django.po
🌐 Idioma destino: en
🔧 Modo: DRY-RUN (simulación)

📊 Entradas a traducir: 156
📦 Procesando en lotes de 10

🔄 Lote 1/16 (10 entradas)
  🔍 [1/156] Original: Bienvenido a nuestra plataforma...
  🔍 [2/156] Original: Por favor ingresa tu usuario...
```

### 2. Traducir todos los archivos .po

**Una vez verificado el dry-run:**

```bash
python /ruta/a/devtools/scripts/po_translator.py
```

### 3. Traducir un archivo específico

```bash
python /ruta/a/devtools/scripts/po_translator.py --file locale/en/LC_MESSAGES/django.po
```

### 4. Ajustar el tamaño del lote

```bash
# Procesa más entradas por lote (más rápido, pero usa más tokens)
python po_translator.py --batch-size 20
```

### 5. Especificar carpeta locale personalizada

```bash
python po_translator.py --locale-path /ruta/a/tu/locale
```

---

## 🔍 Cómo Funciona

### 1. Detección de contenido

El script detecta automáticamente si el texto contiene HTML:

- **Texto simple**: Usa traducción directa con DeepSeek
- **HTML complejo**: Segmenta el HTML usando placeholders, traduce solo el texto, y reintegra

### 2. Segmentación con placeholders (para HTML)

```html
<!-- Original -->
<p>Bienvenido a <strong>PymeMad</strong></p>

<!-- Segmentado -->
<p>{{TEXT_1}}<strong>{{TEXT_2}}</strong></p>

<!-- Placeholders -->
{{TEXT_1}} = "Bienvenido a "
{{TEXT_2}} = "PymeMad"

<!-- Traducción -->
{{TEXT_1}} = "Welcome to "
{{TEXT_2}} = "PymeMad"  (protegido, no se traduce)

<!-- Resultado -->
<p>Welcome to <strong>PymeMad</strong></p>
```

### 3. Términos protegidos

**No se traducen:**
- Nombres propios: Sebastián, Víctor, María
- Marcas y acrónimos: PymeMad, CMPC, PEFC, FSC, ISO
- Términos técnicos: Django, Python, HTML, CSS, JavaScript
- Variables y placeholders: `%(variable)s`, `{placeholder}`
- URLs y emails

### 4. Criterios de traducción

**Se traduce una entrada si:**
- No tiene traducción (`msgstr` vacío)
- Está marcada como `fuzzy`
- La traducción es igual al original (probablemente incorrecta)

---

## 📊 Ejemplo de Salida Completa

```
================================================================================
📁 Procesando: locale/en/LC_MESSAGES/django.po
🌐 Idioma destino: en
🔧 Modo: PRODUCCIÓN
================================================================================

✅ Backup creado: locale/en/LC_MESSAGES/backups/django_backup_20251013_143022.po

📊 Entradas a traducir: 156
📦 Procesando en lotes de 10

🔄 Lote 1/16 (10 entradas)
--------------------------------------------------------------------------------
  🔄 [1/156] Traduciendo: Bienvenido a PymeMad...
  ✅ Traducido: Welcome to PymeMad...
  🔄 [2/156] Traduciendo: La Asociación Gremial de Pequeñas y Medianas...
  ✅ Traducido: The Guild Association of Small and Medium...
  🔄 [3/156] Traduciendo: Por favor ingresa tu usuario y contraseña...
  ✅ Traducido: Please enter your username and password...
  ...

🔄 Lote 2/16 (10 entradas)
--------------------------------------------------------------------------------
  ...

💾 Archivo guardado: locale/en/LC_MESSAGES/django.po

================================================================================
✅ Proceso completado
📊 Estadísticas:
   - Total procesadas: 156
   - Traducidas exitosamente: 154
   - Errores: 2
================================================================================
```

---

## 🎓 Flujo Completo de Traducción

### Paso 1: Preparar archivos .po

```bash
# En tu proyecto Django
python manage.py makemessages -l en --no-obsolete
python manage.py makemessages -l pt --no-obsolete
```

### Paso 2: Simular traducción

```bash
python /ruta/a/devtools/scripts/po_translator.py --dry-run
```

### Paso 3: Traducir

```bash
python /ruta/a/devtools/scripts/po_translator.py
```

### Paso 4: Compilar traducciones

```bash
python manage.py compilemessages
```

### Paso 5: Reiniciar servidor

```bash
# Detener servidor (Ctrl+C)
python manage.py runserver
```

### Paso 6: Probar en el navegador

```
http://localhost:8000/en/  # Inglés
http://localhost:8000/pt/  # Portugués
```

---

## ⚙️ Opciones Avanzadas

### Ver ayuda completa

```bash
python po_translator.py --help
```

### Configurar URL de API personalizada

```bash
export DEEPSEEK_API_URL="https://tu-endpoint-personalizado.com/v1"
```

### Reintentar entradas que fallaron

```bash
python po_translator.py --retry-failed
```

---

## 🔍 Troubleshooting

### Error: "Se requiere DEEPSEEK_API_KEY"

**Solución:**

```bash
export DEEPSEEK_API_KEY="tu-api-key"
# o
python po_translator.py --api-key "tu-api-key"
```

### No se encuentran archivos .po

**Verificar:**

1. Estás en el directorio correcto del proyecto Django
2. La carpeta `locale/` existe
3. Los archivos se llaman `django.po`

```bash
ls -la locale/en/LC_MESSAGES/
ls -la locale/pt/LC_MESSAGES/
```

### Errores de traducción

**Posibles causas y soluciones:**

1. **Sin conexión a internet**: Verifica tu conectividad
2. **API key inválida**: Verifica que la key sea correcta
3. **Rate limit excedido**: Reduce `--batch-size` o espera unos minutos
4. **Timeout**: Reduce `--batch-size` a 5 o menos

```bash
# Usar lotes más pequeños
python po_translator.py --batch-size 5
```

### Las traducciones no se actualizan en el navegador

**Solución:**

```bash
# 1. Recompilar traducciones
python manage.py compilemessages

# 2. Limpiar cache de Python
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -delete

# 3. Reiniciar servidor
# Ctrl+C para detener
python manage.py runserver

# 4. Limpiar cache del navegador
# Ctrl+Shift+R (forzar recarga)
```

---

## 📝 Notas Importantes

1. **Siempre usa `--dry-run` primero** para ver qué se va a traducir
2. Los backups se guardan automáticamente en `locale/*/LC_MESSAGES/backups/`
3. El script NO modifica:
   - Entradas obsoletas
   - Términos en la lista de exclusión
   - Variables y placeholders
4. Después de traducir, **siempre ejecuta** `python manage.py compilemessages`
5. Las traducciones con IA son de alta calidad pero **no perfectas** - revisa casos críticos

---

## 🆚 Ventajas sobre otros métodos

| Característica | Traducción Manual | Google Translate | po_translator.py |
|----------------|-------------------|------------------|------------------|
| Calidad | Excelente | Regular | Excelente |
| Velocidad | Muy lento | Rápido | Muy rápido |
| Contexto HTML | ✅ | ❌ | ✅ |
| Términos protegidos | ✅ | ❌ | ✅ |
| Consistencia | Variable | Regular | Alta |
| Costo tiempo | Alto | Bajo | Muy bajo |
| Procesamiento por lotes | ❌ | ❌ | ✅ |

---

## 🤝 Contribuir

Para mejorar el script:

1. Reporta términos que no deberían traducirse
2. Sugiere mejoras en los prompts
3. Reporta bugs o comportamientos inesperados

Abrir issue en: https://github.com/Hello-World-SpA/devtools/issues

---

## 📚 Referencias

- **Django i18n**: https://docs.djangoproject.com/en/4.2/topics/i18n/
- **DeepSeek API**: https://platform.deepseek.com/
- **polib**: https://pypi.org/project/polib/
- **GNU gettext**: https://www.gnu.org/software/gettext/manual/

---

## 📞 Soporte

¿Necesitas ayuda? Contacta al equipo técnico o abre un issue en el repositorio.

---

**Última actualización:** 13 Oct 2025