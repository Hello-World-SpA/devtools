# 🔍 Guía de Verificación de Sincronización: Modelos Django vs Base de Datos

**Fecha:** 17 Oct 2025
**Nivel:** Intermedio

---

## 🎯 Objetivo

Esta guía explica cómo usar el script `check_model_db_sync.py` para detectar automáticamente desincronización entre los modelos de Django y el estado real de la base de datos PostgreSQL.

---

## 📋 Prerequisitos

- Django 3.2+
- PostgreSQL 12+
- Python 3.8+
- Acceso a la base de datos del proyecto

---

## ❓ ¿Qué hace este script?

El script `check_model_db_sync.py` compara cada modelo de Django con su tabla correspondiente en PostgreSQL y detecta:

- ❌ **Campos faltantes en la BD**: Campos definidos en el modelo pero que no existen en la tabla
- ⚠️ **Campos sobrantes en la BD**: Columnas en la tabla que no están en el modelo
- 🔴 **Tablas faltantes**: Modelos sin tabla correspondiente en la base de datos
- ✅ **Sincronización correcta**: Modelos y tablas que coinciden perfectamente

---

## 🚀 Inicio Rápido

### 1. Copiar el script a tu proyecto

```bash
# Copiar desde devtools a tu proyecto Django
cp /path/to/devtools/scripts/check_model_db_sync.py /path/to/tu_proyecto/
```

### 2. Configurar el script para tu proyecto

Edita el archivo `check_model_db_sync.py`:

```python
# ⚠️ Línea 13: Cambiar 'pymemadweb.settings' por tu proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')

# ⚠️ Líneas 146-160: Actualizar con tus apps
PROJECT_APPS = [
    'accounts',
    'products',
    'orders',
    # ... tus apps aquí
]
```

### 3. Ejecutar el script

```bash
# Desde el directorio raíz de tu proyecto Django
python check_model_db_sync.py
```

---

## 📊 Interpretando la Salida

### Ejemplo de salida:

```
================================================================================
🔍 VERIFICACIÓN DE SINCRONIZACIÓN: MODELOS DJANGO vs BASE DE DATOS
================================================================================

📦 App: accounts
--------------------------------------------------------------------------------
   ✅ User                            → accounts_user
   ⚠️  Profile                        → accounts_profile
      🔴 Faltantes en DB: avatar, bio, phone
      🟡 Sobrantes en DB: old_field_name

📦 App: products
--------------------------------------------------------------------------------
   ✅ Product                         → products_product
   ✅ Category                        → products_category
   ❌ Manufacturer                    → Tabla 'products_manufacturer' NO EXISTE

================================================================================
📊 RESUMEN
================================================================================
Modelos verificados: 5
Problemas encontrados: 4

❌ HAY DESINCRONIZACIÓN. Revisa los problemas arriba.

💡 Soluciones:
   1. Crear migraciones: python manage.py makemigrations
   2. Aplicar migraciones: python manage.py migrate
   3. Si hay desincronización compleja, usar SeparateDatabaseAndState
      Ver: docs/guides/DJANGO_MIGRATIONS_GUIDE.md
```

### Leyenda de símbolos:

| Símbolo | Significado | Acción requerida |
|---------|-------------|------------------|
| ✅ | Todo sincronizado | Ninguna |
| ⚠️ | Diferencias encontradas | Revisar y crear migraciones |
| 🔴 | Campos faltantes en BD | Crear migraciones para agregar campos |
| 🟡 | Campos sobrantes en BD | Evaluar si remover o agregar al modelo |
| ❌ | Tabla no existe | Crear migraciones iniciales |

---

## 🔧 Configuración Detallada

### Configurar DJANGO_SETTINGS_MODULE

**Línea 13 del script:**

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')
```

**Opciones comunes:**

```python
# Producción
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# Desarrollo
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

# Testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.test')
```

### Configurar PROJECT_APPS

**Líneas 146-160 del script:**

```python
PROJECT_APPS = [
    'accounts',
    'products',
    'orders',
    # ... lista todas tus apps aquí
]
```

**Tip**: Para obtener todas las apps instaladas automáticamente:

```python
# Alternativa: detectar apps automáticamente
from django.conf import settings
PROJECT_APPS = [app.split('.')[0] for app in settings.INSTALLED_APPS
                if not app.startswith('django.')]
```

---

## 💡 Casos de Uso

### Caso 1: Antes de hacer deploy

```bash
# Verificar que no haya desincronización antes de subir a producción
python check_model_db_sync.py

# Si todo OK, proceder con deploy
git push origin main
```

### Caso 2: Después de pull de cambios

```bash
# Actualizar código
git pull origin main

# Verificar sincronización
python check_model_db_sync.py

# Si hay problemas, aplicar migraciones
python manage.py migrate
```

### Caso 3: Debugging de errores

```bash
# Error: column 'avatar' does not exist
ProgrammingError: column accounts_user.avatar does not exist

# Verificar sincronización
python check_model_db_sync.py

# Resultado: Campo 'avatar' falta en la BD
# Solución: Aplicar migraciones pendientes
```

### Caso 4: Auditoría de proyecto heredado

```bash
# Proyecto heredado con estado incierto
python check_model_db_sync.py > sync_report.txt

# Revisar el reporte
cat sync_report.txt
```

---

## 🛠️ Soluciones a Problemas Comunes

### Problema 1: Campos faltantes en BD

**Síntoma:**
```
🔴 Faltantes en DB: avatar, bio, phone
```

**Solución A - Migraciones normales:**
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

**Solución B - Desincronización compleja:**
```bash
# Usar SeparateDatabaseAndState
# Ver guía completa: DJANGO_MIGRATIONS_GUIDE.md
python manage.py makemigrations app_name --empty --name fix_sync
```

### Problema 2: Tabla no existe

**Síntoma:**
```
❌ Manufacturer → Tabla 'products_manufacturer' NO EXISTE
```

**Solución:**
```bash
# Crear migraciones iniciales
python manage.py makemigrations products

# Aplicar migraciones
python manage.py migrate products
```

### Problema 3: Campos sobrantes en BD

**Síntoma:**
```
🟡 Sobrantes en DB: old_field_name, deprecated_column
```

**Opciones:**

**A) Agregar al modelo si se necesitan:**
```python
# models.py
class Profile(models.Model):
    # ... otros campos
    old_field_name = models.CharField(max_length=100, blank=True)
```

**B) Remover de BD si no se necesitan:**
```bash
# Crear migración para remover
python manage.py makemigrations --empty app_name --name remove_old_fields

# Editar migración y agregar:
operations = [
    migrations.RunSQL(
        sql="ALTER TABLE table_name DROP COLUMN IF EXISTS old_field_name;",
        reverse_sql="-- No reversible"
    ),
]
```

### Problema 4: App no encontrada

**Síntoma:**
```
⚠️  App 'old_app' no encontrada
```

**Solución:**
```python
# Remover de PROJECT_APPS en el script
PROJECT_APPS = [
    'accounts',
    'products',
    # 'old_app',  # ← Comentar o eliminar
]
```

---

## 🔄 Integración con CI/CD

### GitHub Actions

```yaml
# .github/workflows/check_db_sync.yml
name: Check DB Sync

on: [pull_request]

jobs:
  check-sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Check model-database sync
        run: |
          python check_model_db_sync.py
        env:
          DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "🔍 Verificando sincronización modelo-BD..."
python check_model_db_sync.py

if [ $? -ne 0 ]; then
    echo "❌ Hay desincronización. Ejecuta las migraciones antes de commit."
    exit 1
fi

echo "✅ Sincronización OK"
```

---

## 📝 Mejores Prácticas

### ✅ Hacer:

1. **Ejecutar antes de cada deploy** para asegurar sincronización
2. **Incluir en CI/CD** para prevenir desincronización
3. **Ejecutar después de pull** para detectar cambios de otros devs
4. **Mantener PROJECT_APPS actualizado** con las apps del proyecto
5. **Documentar campos sobrantes** antes de eliminarlos

### ❌ Evitar:

1. **No ignorar warnings** de campos sobrantes sin investigar
2. **No ejecutar en producción** sin antes probar en desarrollo
3. **No modificar el script** sin entender el código
4. **No eliminar columnas** sin verificar que no se usan
5. **No ejecutar con usuarios sin permisos** de información_schema

---

## 🔍 Cómo Funciona (Técnico)

### 1. Obtener columnas de PostgreSQL

```python
SELECT column_name, data_type, is_nullable, character_maximum_length, column_default
FROM information_schema.columns
WHERE table_name = 'accounts_user'
ORDER BY ordinal_position;
```

### 2. Obtener campos del modelo Django

```python
model._meta.get_fields()
# Filtra: relaciones inversas, GenericFK, M2M
```

### 3. Comparar conjuntos

```python
missing_in_db = set(model_fields) - set(db_columns)
missing_in_model = set(db_columns) - set(model_fields)
```

### 4. Reportar diferencias

```python
if missing_in_db:
    print("🔴 Faltantes en DB:", missing_in_db)
if missing_in_model:
    print("🟡 Sobrantes en DB:", missing_in_model)
```

---

## 🧪 Testing del Script

### Crear ambiente de prueba

```bash
# Crear BD de test
createdb test_sync_db

# Configurar settings de test
export DJANGO_SETTINGS_MODULE=config.settings.test

# Ejecutar script
python check_model_db_sync.py
```

### Casos de prueba

```python
# Test 1: Todo sincronizado
# Esperado: ✅ para todos los modelos

# Test 2: Campo faltante en BD
# 1. Agregar campo al modelo
# 2. NO ejecutar makemigrations
# 3. Ejecutar script
# Esperado: 🔴 Campo faltante

# Test 3: Tabla no existe
# 1. Eliminar tabla manualmente
# 2. Ejecutar script
# Esperado: ❌ Tabla no existe
```

---

## 📚 Recursos Relacionados

- **[DJANGO_MIGRATIONS_GUIDE.md](DJANGO_MIGRATIONS_GUIDE.md)** - Guía completa de migraciones con SeparateDatabaseAndState
- **[COMMIT_GUIDE.md](COMMIT_GUIDE.md)** - Convenciones de commits para documentar cambios
- [Django Migrations Docs](https://docs.djangoproject.com/en/4.2/topics/migrations/)
- [PostgreSQL information_schema](https://www.postgresql.org/docs/current/information-schema.html)

---

## 💻 Código Fuente

El script completo está disponible en:

👉 **[scripts/check_model_db_sync.py](../../scripts/check_model_db_sync.py)**

---

## 🤝 Contribuir

¿Encontraste un bug o tienes una mejora?

1. Abre un [Issue](https://github.com/Hello-World-SpA/devtools/issues)
2. Describe el problema o mejora propuesta
3. Si es posible, incluye un ejemplo de uso

---

## 📊 Ejemplo Completo

### Escenario: Proyecto con desincronización

```bash
# 1. Ejecutar verificación
$ python check_model_db_sync.py

================================================================================
🔍 VERIFICACIÓN DE SINCRONIZACIÓN: MODELOS DJANGO vs BASE DE DATOS
================================================================================

📦 App: accounts
--------------------------------------------------------------------------------
   ✅ User                            → accounts_user
   ⚠️  Profile                        → accounts_profile
      🔴 Faltantes en DB: avatar, bio
   ✅ Role                            → accounts_role

📦 App: products
--------------------------------------------------------------------------------
   ✅ Product                         → products_product
   ⚠️  Category                       → products_category
      🟡 Sobrantes en DB: old_slug

================================================================================
📊 RESUMEN
================================================================================
Modelos verificados: 5
Problemas encontrados: 3

❌ HAY DESINCRONIZACIÓN. Revisa los problemas arriba.

# 2. Solucionar problemas
$ python manage.py makemigrations
Migrations for 'accounts':
  accounts/migrations/0003_profile_avatar_profile_bio.py
    - Add field avatar to profile
    - Add field bio to profile

$ python manage.py migrate
Running migrations:
  Applying accounts.0003_profile_avatar_profile_bio... OK

# 3. Verificar nuevamente
$ python check_model_db_sync.py
✅ ¡TODO SINCRONIZADO! Los modelos coinciden con la base de datos.
```

---

**¿Dudas o sugerencias?** Abre un [Issue](https://github.com/Hello-World-SpA/devtools/issues)

---

**Última actualización:** 17 Oct 2025