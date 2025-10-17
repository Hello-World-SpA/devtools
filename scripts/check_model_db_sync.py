#!/usr/bin/env python
"""
Script para comparar los modelos de Django con el estado actual de la base de datos.
Detecta campos faltantes, sobrantes, y diferencias de tipo.

IMPORTANTE: Este script debe ser adaptado a tu proyecto Django:
    1. Cambiar 'pymemadweb.settings' (línea 13) por el nombre de tu proyecto
    2. Actualizar PROJECT_APPS (líneas 146-160) con las apps de tu proyecto
    3. Ejecutar desde el directorio raíz del proyecto Django

Uso:
    python check_model_db_sync.py

Documentación completa:
    docs/guides/MODEL_DB_SYNC_GUIDE.md
"""
import os
import sys
import django
from django.db import connection
from django.apps import apps

# ⚠️ CONFIGURAR: Cambiar por el nombre de tu proyecto Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pymemadweb.settings')
django.setup()

def get_table_columns(table_name):
    """Obtiene las columnas de una tabla desde PostgreSQL"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, character_maximum_length, column_default
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position;
        """, [table_name])
        columns = {}
        for row in cursor.fetchall():
            col_name, data_type, is_nullable, max_length, default = row
            columns[col_name] = {
                'type': data_type,
                'nullable': is_nullable == 'YES',
                'max_length': max_length,
                'default': default
            }
        return columns

def get_model_fields(model):
    """Obtiene los campos del modelo Django"""
    from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

    fields = {}
    for field in model._meta.get_fields():
        # Ignorar relaciones inversas
        if field.auto_created and not field.concrete:
            continue

        # Ignorar GenericForeignKey y GenericRelation (no tienen columnas en DB)
        if isinstance(field, (GenericForeignKey, GenericRelation)):
            continue

        # Ignorar ManyToManyField (tienen tabla intermedia)
        if field.many_to_many:
            continue

        # Obtener nombre de columna
        if hasattr(field, 'column'):
            col_name = field.column
        else:
            col_name = field.name

        # Obtener tipo de campo (algunos campos no tienen get_internal_type)
        try:
            field_type = field.get_internal_type()
        except AttributeError:
            field_type = field.__class__.__name__

        fields[col_name] = {
            'field_type': field_type,
            'null': field.null if hasattr(field, 'null') else True,
            'blank': field.blank if hasattr(field, 'blank') else True,
            'default': field.default if hasattr(field, 'default') else None,
        }
    return fields

def compare_model_with_db(model):
    """Compara un modelo con su tabla en la base de datos"""
    table_name = model._meta.db_table

    # Verificar si la tabla existe
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = %s
            );
        """, [table_name])
        table_exists = cursor.fetchone()[0]

    if not table_exists:
        return {
            'status': 'missing_table',
            'table_name': table_name,
            'model': model.__name__,
        }

    # Obtener columnas de DB y modelo
    db_columns = get_table_columns(table_name)
    model_fields = get_model_fields(model)

    # Comparar
    missing_in_db = set(model_fields.keys()) - set(db_columns.keys())
    missing_in_model = set(db_columns.keys()) - set(model_fields.keys())
    common_fields = set(model_fields.keys()) & set(db_columns.keys())

    issues = []

    # Campos faltantes en DB
    for field_name in missing_in_db:
        issues.append({
            'type': 'missing_in_db',
            'field': field_name,
            'field_info': model_fields[field_name]
        })

    # Campos sobrantes en DB
    for field_name in missing_in_model:
        issues.append({
            'type': 'extra_in_db',
            'field': field_name,
            'db_info': db_columns[field_name]
        })

    if issues or missing_in_db or missing_in_model:
        return {
            'status': 'mismatch',
            'table_name': table_name,
            'model': model.__name__,
            'issues': issues,
            'missing_in_db': list(missing_in_db),
            'missing_in_model': list(missing_in_model),
        }

    return {
        'status': 'ok',
        'table_name': table_name,
        'model': model.__name__,
    }

def main():
    """Función principal"""
    print("=" * 80)
    print("🔍 VERIFICACIÓN DE SINCRONIZACIÓN: MODELOS DJANGO vs BASE DE DATOS")
    print("=" * 80)
    print()

    # ⚠️ CONFIGURAR: Actualizar con las apps de tu proyecto Django
    PROJECT_APPS = [
        'accounts',
        'billing',
        'communications',
        'core',
        'documents',
        'governance',
        'landing',
        'members',
        'news',
        'panel',
        'permissions',
        'scrapers',
        'strategy',
    ]

    all_ok = True
    total_issues = 0
    models_checked = 0

    for app_label in PROJECT_APPS:
        try:
            app_config = apps.get_app_config(app_label)
        except LookupError:
            print(f"⚠️  App '{app_label}' no encontrada")
            continue

        print(f"\n📦 App: {app_label}")
        print("-" * 80)

        models = app_config.get_models()
        if not models:
            print("   (sin modelos)")
            continue

        for model in models:
            models_checked += 1
            result = compare_model_with_db(model)

            if result['status'] == 'ok':
                print(f"   ✅ {result['model']:30} → {result['table_name']}")

            elif result['status'] == 'missing_table':
                print(f"   ❌ {result['model']:30} → Tabla '{result['table_name']}' NO EXISTE")
                all_ok = False
                total_issues += 1

            elif result['status'] == 'mismatch':
                print(f"   ⚠️  {result['model']:30} → {result['table_name']}")

                if result['missing_in_db']:
                    print(f"      🔴 Faltantes en DB: {', '.join(result['missing_in_db'])}")
                    all_ok = False
                    total_issues += len(result['missing_in_db'])

                if result['missing_in_model']:
                    print(f"      🟡 Sobrantes en DB: {', '.join(result['missing_in_model'])}")

    print("\n" + "=" * 80)
    print("📊 RESUMEN")
    print("=" * 80)
    print(f"Modelos verificados: {models_checked}")
    print(f"Problemas encontrados: {total_issues}")

    if all_ok and total_issues == 0:
        print("\n✅ ¡TODO SINCRONIZADO! Los modelos coinciden con la base de datos.")
        return 0
    else:
        print("\n❌ HAY DESINCRONIZACIÓN. Revisa los problemas arriba.")
        print("\n💡 Soluciones:")
        print("   1. Crear migraciones: python manage.py makemigrations")
        print("   2. Aplicar migraciones: python manage.py migrate")
        print("   3. Si hay desincronización compleja, usar SeparateDatabaseAndState")
        print("      Ver: docs/guides/DJANGO_MIGRATIONS_GUIDE.md")
        return 1

if __name__ == '__main__':
    sys.exit(main())