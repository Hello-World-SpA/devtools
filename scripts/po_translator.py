#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script optimizado para traducir archivos .po usando DeepSeek API
Reutiliza las funciones eficientes del script de traducción de Moodle
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
import shutil
import polib
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


class POTranslator:
    """
    Traductor eficiente de archivos .po usando DeepSeek API
    """

    def __init__(self, api_key=None):
        """
        Inicializa el traductor con la API de DeepSeek

        Args:
            api_key: Clave API de DeepSeek (opcional, usa variable de entorno si no se proporciona)
        """
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("Se requiere DEEPSEEK_API_KEY. Proporciona la clave o configura la variable de entorno.")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=os.environ.get("DEEPSEEK_API_URL", "https://api.deepseek.com/v1")
        )

    def segment_html_with_placeholders(self, html):
        """
        Segmenta el HTML extrayendo texto para traducir y reemplazándolo con placeholders.
        Reutilizada del script de Moodle.

        Args:
            html (str): HTML a segmentar

        Returns:
            tuple: (html_con_placeholders, diccionario_placeholders)
        """
        soup = BeautifulSoup(html, 'html.parser')
        placeholders = {}
        count = 1

        for text_node in soup.find_all(string=True):
            text = text_node.strip()
            if text and not text.isspace():
                placeholder = f"{{{{TEXT_{count}}}}}"
                placeholders[placeholder] = text
                text_node.replace_with(placeholder)
                count += 1

        return str(soup), placeholders

    def reintegrate_translations(self, html_with_placeholders, translated_placeholders):
        """
        Reintegra las traducciones en el HTML con placeholders.
        Reutilizada del script de Moodle.

        Args:
            html_with_placeholders (str): HTML con placeholders
            translated_placeholders (dict): Diccionario con placeholders traducidos

        Returns:
            str: HTML con traducciones integradas
        """
        result = html_with_placeholders
        for placeholder, translated_text in translated_placeholders.items():
            result = result.replace(placeholder, translated_text)
        return result

    def translate_placeholders_with_deepseek(self, placeholders, target_lang, source_lang='es'):
        """
        Traduce un diccionario de placeholders usando DeepSeek.
        Adaptada del script de Moodle para un solo idioma a la vez.

        Args:
            placeholders (dict): Diccionario con placeholders y textos
            target_lang (str): Código de idioma destino ('en' o 'pt')
            source_lang (str): Código de idioma origen (default: 'es')

        Returns:
            dict: Diccionario con placeholders traducidos
        """
        if not placeholders:
            return {}

        # Preparar textos para traducir - solo los valores, no los placeholders
        texts_list = list(placeholders.values())
        placeholder_keys = list(placeholders.keys())

        # Crear un mapeo numerado para simplificar
        numbered_texts = []
        for i, text in enumerate(texts_list, 1):
            numbered_texts.append(f"{i}. {text}")

        lang_names = {
            'en': 'English',
            'pt': 'Portuguese (Brazil)',
            'pt_br': 'Portuguese (Brazil)'
        }

        target_lang_name = lang_names.get(target_lang, target_lang)

        system_prompt = """Eres un traductor profesional especializado en contenido web empresarial.
Traduce con precisión manteniendo el contexto y significado original.
Preserva nombres propios, marcas, nombres de lugares, términos técnicos y acrónimos."""

        user_prompt = f"""
Traduce estos textos del español a {target_lang_name}:

{chr(10).join(numbered_texts)}

Reglas:
- Mantén el formato de numeración exacto (1. 2. 3. etc.)
- Preserva TODAS las etiquetas HTML sin modificar
- NO traduzcas nombres propios de personas, lugares, empresas o marcas
- NO traduzcas acrónimos, códigos o términos técnicos
- Devuelve SOLO las traducciones numeradas, sin explicaciones

Formato:
1. [traducción]
2. [traducción]
"""

        try:
            message = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=4000,
                timeout=90
            )

            content = message.choices[0].message.content

            # Parsear las respuestas numeradas
            translations = {}
            lines = content.strip().split('\n')

            for line in lines:
                line = line.strip()
                if line and line[0].isdigit():
                    # Extraer número y traducción
                    parts = line.split('.', 1)
                    if len(parts) == 2:
                        try:
                            num = int(parts[0].strip())
                            translation = parts[1].strip()
                            # Mapear de vuelta al placeholder original
                            if 1 <= num <= len(placeholder_keys):
                                placeholder_key = placeholder_keys[num - 1]
                                translations[placeholder_key] = translation
                        except:
                            continue

            return translations

        except Exception as e:
            print(f"❌ Error al traducir placeholders: {e}")
            return {}

    def translate_simple_text(self, text, target_lang, source_lang='es'):
        """
        Traduce texto simple (sin HTML) usando DeepSeek.

        Args:
            text (str): Texto a traducir
            target_lang (str): Código de idioma destino
            source_lang (str): Código de idioma origen

        Returns:
            str: Texto traducido o None si falla
        """
        lang_names = {
            'en': 'English',
            'pt': 'Portuguese (Brazil)'
        }

        target_lang_name = lang_names.get(target_lang, target_lang)

        system_prompt = f"""You are a professional translator. Translate from Spanish to {target_lang_name}.
Rules:
- Return ONLY the translation, nothing else
- Do NOT include instructions, explanations, or notes
- Do NOT translate proper names, brands, or technical terms
- Preserve formatting and punctuation"""

        user_prompt = f"""Translate to {target_lang_name}:

{text}"""

        try:
            message = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=2000,
                timeout=60
            )

            translation = message.choices[0].message.content.strip()

            # Remover comillas si la respuesta viene entre comillas
            if translation.startswith('"') and translation.endswith('"'):
                translation = translation[1:-1]
            if translation.startswith("'") and translation.endswith("'"):
                translation = translation[1:-1]

            # Validar que la respuesta no contenga las instrucciones
            if self._is_valid_translation(translation, text):
                return translation
            else:
                print(f"⚠️  Respuesta inválida del API (contiene instrucciones o es muy larga)")
                return None

        except Exception as e:
            print(f"❌ Error al traducir texto simple: {e}")
            return None

    def translate_text_smart(self, text, target_lang, source_lang='es'):
        """
        Traduce texto de forma inteligente: detecta si tiene HTML y usa el método apropiado.

        Args:
            text (str): Texto a traducir (puede contener HTML)
            target_lang (str): Código de idioma destino
            source_lang (str): Código de idioma origen

        Returns:
            str: Texto traducido o None si falla
        """
        # Detectar si el texto contiene HTML
        if '<' in text and '>' in text:
            # Es HTML, usar segmentación con placeholders
            html_with_placeholders, placeholders = self.segment_html_with_placeholders(text)

            if not placeholders:
                # No hay texto para traducir
                return text

            # Traducir los placeholders
            translated_placeholders = self.translate_placeholders_with_deepseek(
                placeholders,
                target_lang,
                source_lang
            )

            if not translated_placeholders:
                print(f"⚠️  No se pudieron traducir los placeholders")
                return None

            # Reintegrar las traducciones
            translated_html = self.reintegrate_translations(html_with_placeholders, translated_placeholders)
            return translated_html
        else:
            # Es texto simple
            return self.translate_simple_text(text, target_lang, source_lang)

    def _is_valid_translation(self, translation, original_text):
        """
        Valida que la traducción sea válida y no contenga instrucciones del prompt.

        Args:
            translation (str): Texto traducido
            original_text (str): Texto original

        Returns:
            bool: True si es válida, False en caso contrario
        """
        if not translation or not translation.strip():
            return False

        # Detectar si contiene patrones específicos de las instrucciones del prompt
        # Usamos patrones más específicos para evitar falsos positivos
        invalid_patterns = [
            r'\brules:\s*\n',           # "rules:" seguido de salto de línea
            r'\breglas:\s*\n',          # "reglas:" seguido de salto de línea
            r'translate from .+ to',     # "translate from Spanish to..."
            r'traduce del .+ a',        # "traduce del español a..."
            r'do not translate\b',      # "do not translate" como frase
            r'no traduzcas\b',          # "no traduzcas" como frase
            r'\bpreserve formatting',   # "preserve formatting"
            r'return only',             # "return only"
            r'devuelve solo',           # "devuelve solo"
            r'format:\s*\n',            # "format:" seguido de salto de línea
            r'formato:\s*\n',           # "formato:" seguido de salto de línea
        ]

        translation_lower = translation.lower()
        for pattern in invalid_patterns:
            if re.search(pattern, translation_lower):
                return False

        # La traducción no debe ser mucho más larga que el original
        # (indica que probablemente incluye instrucciones)
        max_length_ratio = 3.0  # Permitir hasta 3x el tamaño original
        if len(translation) > len(original_text) * max_length_ratio:
            return False

        return True

    def should_translate(self, text):
        """
        Determina si un texto debe ser traducido.

        Args:
            text (str): Texto a evaluar

        Returns:
            bool: True si debe traducirse, False en caso contrario
        """
        if not text or not text.strip():
            return False

        # No traducir textos muy cortos (menos de 2 caracteres)
        if len(text.strip()) < 2:
            return False

        # No traducir si es solo variables/placeholders de Django/Python
        if re.match(r'^(%\(.*?\)[sd]|{\w+}|\$\w+)+$', text.strip()):
            return False

        # No traducir si es solo una URL o email
        if re.match(r'^(https?://|www\.|[\w\.-]+@[\w\.-]+).*$', text.strip()) and not ' ' in text:
            return False

        return True

    def create_backup(self, file_path):
        """
        Crea un backup del archivo .po

        Args:
            file_path (Path): Ruta del archivo

        Returns:
            Path: Ruta del backup creado
        """
        backup_dir = file_path.parent / "backups"
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_backup_{timestamp}.po"
        backup_path = backup_dir / backup_name

        shutil.copy2(str(file_path), str(backup_path))
        print(f"✅ Backup creado: {backup_path}")
        return backup_path

    def translate_po_file(self, po_file_path, batch_size=10, dry_run=False):
        """
        Traduce un archivo .po completo.

        Args:
            po_file_path (str|Path): Ruta al archivo .po
            batch_size (int): Número de entradas a procesar por lote
            dry_run (bool): Si es True, solo muestra qué se traduciría sin hacer cambios

        Returns:
            bool: True si se procesó correctamente, False en caso contrario
        """
        po_file_path = Path(po_file_path)

        if not po_file_path.exists():
            print(f"❌ Archivo no encontrado: {po_file_path}")
            return False

        # Determinar el idioma destino por la ruta del archivo
        if '/en/' in str(po_file_path):
            target_lang = 'en'
        elif '/pt/' in str(po_file_path):
            target_lang = 'pt'
        else:
            print(f"❌ No se pudo determinar el idioma destino del archivo: {po_file_path}")
            return False

        print(f"\n{'='*80}")
        print(f"📁 Procesando: {po_file_path}")
        print(f"🌐 Idioma destino: {target_lang}")
        print(f"🔧 Modo: {'DRY-RUN (simulación)' if dry_run else 'PRODUCCIÓN'}")
        print(f"{'='*80}\n")

        # Crear backup si no es dry-run
        if not dry_run:
            self.create_backup(po_file_path)

        try:
            # Cargar el archivo .po
            po = polib.pofile(str(po_file_path))

            # Filtrar entradas que necesitan traducción
            entries_to_translate = []
            for entry in po:
                if entry.obsolete:
                    continue

                # Traducir si:
                # 1. No tiene traducción (msgstr vacío)
                # 2. Es fuzzy
                # 3. La traducción es igual al original (probablemente incorrecta)
                needs_translation = (
                    not entry.msgstr or
                    entry.fuzzy or
                    entry.msgstr == entry.msgid
                )

                if needs_translation and self.should_translate(entry.msgid):
                    entries_to_translate.append(entry)

            total_entries = len(entries_to_translate)

            if total_entries == 0:
                print("✅ No hay entradas que necesiten traducción")
                return True

            print(f"📊 Entradas a traducir: {total_entries}")
            print(f"📦 Procesando en lotes de {batch_size}\n")

            translated_count = 0
            error_count = 0

            # Procesar en lotes
            for i in range(0, total_entries, batch_size):
                batch = entries_to_translate[i:i+batch_size]
                batch_num = (i // batch_size) + 1
                total_batches = (total_entries + batch_size - 1) // batch_size

                print(f"\n🔄 Lote {batch_num}/{total_batches} ({len(batch)} entradas)")
                print("-" * 80)

                for entry in batch:
                    try:
                        original_text = entry.msgid

                        if dry_run:
                            print(f"  🔍 [{translated_count + 1}/{total_entries}] Original: {original_text[:80]}...")
                        else:
                            print(f"  🔄 [{translated_count + 1}/{total_entries}] Traduciendo: {original_text[:80]}...")

                            # Traducir usando el método inteligente
                            translation = self.translate_text_smart(original_text, target_lang)

                            if translation:
                                entry.msgstr = translation
                                entry.fuzzy = False  # Quitar el flag fuzzy
                                translated_count += 1
                                print(f"  ✅ Traducido: {translation[:80]}...")
                            else:
                                error_count += 1
                                print(f"  ⚠️  No se pudo traducir")

                    except Exception as e:
                        error_count += 1
                        print(f"  ❌ Error: {e}")

            # Guardar el archivo si no es dry-run
            if not dry_run and translated_count > 0:
                po.save(str(po_file_path))
                print(f"\n💾 Archivo guardado: {po_file_path}")

            print(f"\n{'='*80}")
            print(f"✅ Proceso completado")
            print(f"📊 Estadísticas:")
            print(f"   - Total procesadas: {total_entries}")
            print(f"   - Traducidas exitosamente: {translated_count}")
            print(f"   - Errores: {error_count}")
            print(f"{'='*80}\n")

            return True

        except Exception as e:
            print(f"❌ Error procesando archivo: {e}")
            import traceback
            traceback.print_exc()
            return False

    def translate_locale_folder(self, locale_path='locale', batch_size=10, dry_run=False):
        """
        Traduce todos los archivos .po en la carpeta locale.

        Args:
            locale_path (str): Ruta a la carpeta locale
            batch_size (int): Número de entradas a procesar por lote
            dry_run (bool): Si es True, solo muestra qué se traduciría

        Returns:
            bool: True si todos los archivos se procesaron correctamente
        """
        locale_path = Path(locale_path)

        if not locale_path.exists():
            print(f"❌ La carpeta locale no existe: {locale_path}")
            return False

        # Buscar archivos .po
        po_files = list(locale_path.glob('**/django.po'))

        if not po_files:
            print(f"❌ No se encontraron archivos django.po en: {locale_path}")
            return False

        print(f"\n{'='*80}")
        print(f"🌍 TRADUCTOR DE ARCHIVOS .PO CON DEEPSEEK")
        print(f"{'='*80}")
        print(f"📁 Carpeta locale: {locale_path}")
        print(f"📄 Archivos encontrados: {len(po_files)}")
        for pf in po_files:
            print(f"   - {pf}")
        print(f"{'='*80}\n")

        success = True
        for po_file in po_files:
            result = self.translate_po_file(po_file, batch_size=batch_size, dry_run=dry_run)
            if not result:
                success = False

        return success


def main():
    """Función principal del script"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Traductor eficiente de archivos .po usando DeepSeek API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Modo dry-run (simulación) - RECOMENDADO primero
  python po_translator.py --dry-run

  # Traducir todos los archivos .po
  python po_translator.py

  # Traducir un archivo específico
  python po_translator.py --file locale/en/LC_MESSAGES/django.po

  # Usar lotes más grandes para mayor velocidad (default: 10)
  python po_translator.py --batch-size 20

  # Especificar API key directamente
  python po_translator.py --api-key sk-xxxxx
        """
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Modo simulación: muestra qué se traduciría sin hacer cambios'
    )

    parser.add_argument(
        '--file',
        type=str,
        help='Traducir un archivo .po específico en lugar de todos'
    )

    parser.add_argument(
        '--locale-path',
        type=str,
        default='locale',
        help='Ruta a la carpeta locale (default: locale)'
    )

    parser.add_argument(
        '--batch-size',
        type=int,
        default=10,
        help='Número de entradas a procesar por lote (default: 10)'
    )

    parser.add_argument(
        '--api-key',
        type=str,
        help='Clave API de DeepSeek (también se puede usar DEEPSEEK_API_KEY env var)'
    )

    parser.add_argument(
        '--retry-failed',
        action='store_true',
        help='Reintentar traducir solo las entradas que fallaron previamente'
    )

    args = parser.parse_args()

    try:
        # Inicializar el traductor
        translator = POTranslator(api_key=args.api_key)

        # Procesar archivo(s)
        if args.file:
            success = translator.translate_po_file(
                args.file,
                batch_size=args.batch_size,
                dry_run=args.dry_run
            )
        else:
            success = translator.translate_locale_folder(
                locale_path=args.locale_path,
                batch_size=args.batch_size,
                dry_run=args.dry_run
            )

        sys.exit(0 if success else 1)

    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
        print("\n💡 Tip: Configura la variable de entorno DEEPSEEK_API_KEY o usa --api-key")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()