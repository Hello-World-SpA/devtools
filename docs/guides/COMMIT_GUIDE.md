# 📝 Guía de Mensajes de Commit - DevTools

**Fecha:** 17 Oct 2025
**Nivel:** Básico/Intermedio

---

## 🎯 Estructura del Mensaje

```
<tipo>(<alcance>): <descripción corta>

<descripción larga explicando POR QUÉ>

<footer con referencias>
```

### Ejemplo Real

```bash
docs(guides): agregar guía completa de traductor po_translator.py

Se creó documentación detallada del script po_translator.py para
facilitar el onboarding y el uso correcto de la herramienta por parte
del equipo. Incluye ejemplos, troubleshooting y mejores prácticas.

- Agregado PO_TRANSLATOR_GUIDE.md con instrucciones completas
- Actualizado README.md con enlaces a la nueva guía
- Incluidos ejemplos de uso y casos comunes

Refs: #12
```

---

## 📚 Tipos de Commit

### `feat` - Nueva funcionalidad

Cuando agregas una nueva característica, herramienta, script o guía al repositorio.

```bash
feat(scripts): agregar script para sincronización de bases de datos

Se agregó sync_database.py para sincronizar datos entre ambientes de
desarrollo y staging, permitiendo al equipo trabajar con datos reales
sin afectar producción.

- Script con validaciones de seguridad
- Soporte para PostgreSQL y MySQL
- Modo dry-run para pruebas
- Documentación en README

Refs: #45
```

### `fix` - Corrección de bugs

Cuando corriges un error en un script, comando o documentación.

```bash
fix(translator): corregir manejo de caracteres especiales en HTML

El traductor fallaba al procesar entidades HTML como &nbsp; y &copy;
causando que las traducciones quedaran incorrectas. Se agregó
decodificación HTML antes de enviar a la API.

- Uso de html.unescape() antes de traducir
- Tests agregados para caracteres especiales
- Actualizada documentación con este caso

Fixes: #78
```

### `docs` - Documentación

Cuando creas o actualizas documentación, guías o README.

```bash
docs(git): crear guía completa de mensajes de commit

Se documentaron las convenciones de commits del equipo con ejemplos
prácticos para mejorar la consistencia y calidad del historial de Git.

- Creado COMMIT_GUIDE.md con estructura y tipos
- Ejemplos buenos y malos
- Checklist y comandos útiles
- Actualizado README con enlace a la guía
```

### `refactor` - Refactorización

Cuando mejoras código existente sin cambiar su funcionalidad.

```bash
refactor(translator): separar lógica de traducción en funciones

Se refactorizó translate_po_file() en funciones más pequeñas para
mejorar legibilidad y facilitar testing unitario.

- Creadas funciones extract_entries(), translate_batch()
- Reducido cyclomatic complexity de 15 a 5
- Mantenida compatibilidad total con API existente
```

### `chore` - Tareas de mantenimiento

Actualizaciones de dependencias, configuración, estructura del repo, etc.

```bash
chore(deps): actualizar dependencias del translator a versiones LTS

Actualización de dependencias para mantener compatibilidad y seguridad.
Se priorizaron versiones LTS con soporte extendido.

- openai>=1.51.0 (soporte mejorado para streaming)
- polib>=1.2.0 (bugfixes críticos)
- beautifulsoup4>=4.12.3 (vulnerabilidades corregidas)

Refs: #90
```

### `perf` - Mejoras de rendimiento

Cuando optimizas velocidad, uso de memoria o recursos.

```bash
perf(translator): implementar caché de traducciones

Se agregó sistema de caché local con shelve para evitar retraducciones
de strings idénticos, reduciendo llamadas a API en ~60% y acelerando
traducciones de archivos .po con strings repetidos.

- Caché persistente en .cache/translations.db
- Invalidación automática por cambio de idioma
- Reducción de costos de API estimada: $50/mes
```

### `security` - Seguridad

Correcciones de vulnerabilidades o mejoras de seguridad.

```bash
security(scripts): remover API keys hardcodeadas en ejemplos

Se detectaron API keys de prueba expuestas en comentarios de código.
Se removieron y se actualizó documentación para usar solo variables
de entorno.

- Removidas todas las keys de ejemplo
- Actualizado .gitignore para archivos .env
- Agregada validación de API key en runtime
```

### `test` - Tests

Cuando agregas o corriges tests.

```bash
test(translator): agregar tests unitarios para parsing HTML

Se agregaron tests para verificar que el traductor maneja
correctamente HTML complejo sin romper estructura.

- 15 tests nuevos con fixtures de HTML real
- Coverage aumentado de 45% a 78%
- Agregado pytest-html para reportes visuales
```

### `ci` - CI/CD

Cambios en workflows, GitHub Actions, scripts de deployment.

```bash
ci(actions): agregar workflow para validar guías markdown

Se agregó GitHub Action para validar que todas las guías markdown
tengan formato correcto y enlaces válidos antes de merge.

- Workflow runs en PRs a main
- Validación de sintaxis markdown
- Verificación de enlaces rotos
- Generación de reporte en comentarios
```

### `style` - Estilo de código

Formateo, linting, ordenamiento de imports (sin cambio de lógica).

```bash
style(scripts): aplicar black y isort a todos los scripts Python

Se formateó todo el código Python siguiendo PEP 8 para mantener
consistencia y facilitar code review.

- Aplicado black con line-length=100
- Ordenados imports con isort
- Agregado pre-commit hook para mantener formato
```

---

## ❌ Ejemplos de MALOS commits

```bash
# ❌ Muy vago
"fix bug"
"update files"
"changes"

# ❌ Sin contexto
"actualizar script"
"agregar documentación"
"modificar readme"

# ❌ Múltiples cambios sin relación
"actualizar translator, agregar guía de docker, fix readme, cambiar deps"

# ❌ Solo describe el QUÉ, no el POR QUÉ
"agregar beautifulsoup4 a requirements.txt"
"cambiar nombre de función translate()"

# ❌ Sin tipo ni alcance
"mejoras en el proyecto"
"actualización general"
```

---

## ✅ Ejemplos de BUENOS commits

```bash
# ✅ Clara y completa
feat(scripts): agregar script para backup automático de bases de datos

Se creó backup_db.py para automatizar backups diarios de PostgreSQL
con compresión y rotación de archivos antiguos, mejorando nuestra
estrategia de disaster recovery.

- Soporte para PostgreSQL 13+
- Compresión gzip automática
- Rotación: mantiene últimos 30 días
- Logs detallados en /var/log/backups

Refs: #156

# ✅ Fix bien explicado
fix(translator): corregir timeout en archivos .po grandes

Los archivos con +1000 strings causaban timeout de 60s en la API.
Se implementó procesamiento en chunks de 50 strings con reintentos
automáticos en caso de fallo.

- Procesamiento en batches de 50 strings
- Retry con backoff exponencial (3 intentos)
- Progress bar para visualizar avance
- Timeout aumentado a 120s por batch

Fixes: #201

# ✅ Docs útiles
docs(guides): agregar troubleshooting común de Django a FAQ

Se documentaron los 10 problemas más frecuentes reportados en Slack
durante el último mes para reducir preguntas repetitivas.

- Agregado DJANGO_FAQ.md con soluciones
- Links a documentación oficial
- Ejemplos de código funcional
- Actualizado README con enlace
```

---

## 🎯 Alcances (scope) Comunes

| Alcance | Uso |
|---------|-----|
| `scripts` | Scripts de utilidad (po_translator, backups, etc.) |
| `guides` | Documentación y guías técnicas |
| `git` | Configuración Git, hooks, etc. |
| `deps` | Dependencias y requirements |
| `docker` | Dockerfiles, docker-compose |
| `ci` | GitHub Actions, workflows |
| `config` | Configuraciones generales |
| `translator` | Específico del po_translator |

---

## ✅ Checklist antes de hacer commit

- [ ] ¿El tipo de commit es correcto? (feat, fix, docs, etc.)
- [ ] ¿La descripción corta tiene menos de 50 caracteres?
- [ ] ¿Expliqué **POR QUÉ** hice el cambio, no solo QUÉ cambié?
- [ ] ¿Incluí referencias a issues o tickets si aplica?
- [ ] ¿El mensaje ayudará a entender el cambio en 6 meses?
- [ ] ¿Usé verbos en imperativo? (agregar, no agregado)
- [ ] ¿El commit contiene un solo cambio lógico?

---

## 🚀 Comandos Útiles

### Ver historial de commits

```bash
# Últimos 10 commits con formato bonito
git log --oneline --graph --decorate -10

# Ver commits por autor
git log --author="Tu Nombre" --oneline

# Ver commits de un archivo específico
git log --oneline -- scripts/po_translator.py

# Ver cambios en un commit específico
git show <commit-hash>
```

### Mejorar commits

```bash
# Cambiar el último mensaje de commit (antes de push)
git commit --amend

# Agregar cambios al último commit (antes de push)
git add .
git commit --amend --no-edit

# Reescribir últimos N commits (avanzado)
git rebase -i HEAD~3
```

### Buscar en el historial

```bash
# Buscar commit que introdujo un cambio
git log -S "función_especifica" --oneline

# Buscar en mensajes de commit
git log --grep="translator" --oneline

# Ver quién cambió cada línea
git blame scripts/po_translator.py
```

---

## 🔧 Configuración Recomendada

### Configurar editor para commits

```bash
# VS Code (recomendado)
git config --global core.editor "code --wait"

# Vim
git config --global core.editor vim

# Nano
git config --global core.editor nano
```

### Plantilla de commit (opcional)

Puedes crear una plantilla para recordar la estructura:

**1. Crear archivo `.gitmessage` en tu HOME:**

```bash
# ~/.gitmessage
# <tipo>(<alcance>): <descripción corta máx 50 chars>

# Por qué hice este cambio (el contexto es clave):
# -
# -

# Refs: #issue
```

**2. Configurar Git para usarla:**

```bash
git config --global commit.template ~/.gitmessage
```

**3. Al hacer commit se abrirá con la plantilla:**

```bash
git commit  # Se abre editor con plantilla
```

---

## 📊 Beneficios de Buenos Mensajes

### 1. **Historial útil como documentación**
```bash
$ git log --oneline
ee8615d docs: agregar documentación completa de po_translator.py
eb8dbc7 feat: configuración inicial del repositorio devtools
```

### 2. **Debugging más fácil**
```bash
# Encontrar cuándo se introdujo un bug
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
```

### 3. **Code reviews mejores**
Los reviewers entienden el **contexto** y pueden dar feedback más útil.

### 4. **Onboarding rápido**
Nuevos desarrolladores pueden entender **por qué** se tomaron decisiones.

### 5. **Generación automática de CHANGELOG**
```bash
# Generar changelog desde commits
git log --oneline --grep="^feat" > CHANGELOG.md
```

---

## 🎓 Recursos Adicionales

- **Conventional Commits:** https://www.conventionalcommits.org/
- **Semantic Versioning:** https://semver.org/
- **Git Best Practices:** https://git-scm.com/book/en/v2

---

## 💡 Tips Finales

1. **Commits pequeños y atómicos:** Un cambio = un commit
2. **Commit frecuentemente:** No esperes a tener 50 archivos modificados
3. **El mensaje es para el futuro tú:** Sé amable contigo mismo
4. **Lee tus commits antes de push:** `git log -3` para revisar
5. **Si usas "y" en la descripción:** Probablemente deberían ser 2 commits

---

**¿Dudas o sugerencias?** Abre un [Issue](https://github.com/Hello-World-SpA/devtools/issues)

---

**Última actualización:** 17 Oct 2025