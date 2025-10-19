# 🔧 Guía de GitHub Actions - Diagnóstico y Monitoreo con gh CLI

**Fecha:** 18 Oct 2025
**Nivel:** Intermedio

---

## 🎯 Objetivo

Esta guía te ayudará a revisar, monitorear y diagnosticar problemas en los workflows de GitHub Actions usando `gh` CLI (GitHub Command Line Interface).

---

## 📋 Prerequisitos

- GitHub CLI instalado (`gh`)
- Autenticación con GitHub (`gh auth login`)
- Acceso a un repositorio con GitHub Actions

---

## 📋 Tabla de Contenidos

- [Comandos Básicos](#comandos-básicos)
  - [Ver últimos workflows ejecutados](#ver-últimos-workflows-ejecutados)
  - [Ver resumen de un workflow específico](#1-ver-resumen-de-un-workflow-específico)
  - [Monitorear workflow en tiempo real](#2-monitorear-workflow-en-tiempo-real)
  - [Re-ejecutar workflows](#3-re-ejecutar-workflows)
- [Diagnosticar Fallos](#diagnosticar-fallos)
- [Logs Detallados](#logs-detallados)
- [Ejemplos Prácticos](#ejemplos-prácticos)
- [Tips y Trucos](#tips-y-trucos)
- [Flujo de Trabajo Recomendado](#flujo-de-trabajo-recomendado)

---

## Comandos Básicos

### Ver últimos workflows ejecutados

```bash
# Ver los últimos 5 workflows
gh run list --limit 5

# Ver workflows de una rama específica
gh run list --branch main --limit 10

# Ver solo workflows en ejecución
gh run list --status in_progress

# Ver solo workflows fallidos
gh run list --status failure --limit 10

# Ver workflows exitosos
gh run list --status success --limit 10
```

**Salida esperada:**
```
STATUS      TITLE                                      WORKFLOW                         BRANCH  EVENT  ID           ELAPSED  AGE
✓ Success   fix: add missing dependency                Build, Push and Deploy to K8s    main    push   18604907574  3m2s     5m
✗ Failure   feat: configure Sentry monitoring          Build, Push and Deploy to K8s    main    push   18604764965  1m14s    10m
```

---

## Ver Estado de Workflows

### 1. Ver resumen de un workflow específico

```bash
# Usando el ID del run
gh run view 18604907574

# Ver el último workflow ejecutado
gh run view
```

**Salida esperada:**
```
✗ main Build, Push and Deploy to Kubernetes · 18604907574
Triggered via push about 5 minutes ago

JOBS
✓ test_django / test_django (3.9) in 1m8s (ID 53051590838)
✗ deploy in 2m6s (ID 53052151415)
  ✓ Set up job
  ✓ Notificar inicio de deploy en Slack
  ✓ Checkout
  ✓ Set up Docker Buildx
  ✓ Login to Docker Hub
  ✗ Build and push Docker image    <-- AQUÍ FALLÓ
  - Notificar fallo de Docker Build
  ✓ Complete job
```

### 2. Monitorear workflow en tiempo real

```bash
# Ver un workflow en progreso (watch mode)
gh run watch 18604907574

# Watch del último workflow
gh run watch
```

### 3. Re-ejecutar workflows

```bash
# Re-ejecutar un workflow completo usando su ID
gh run rerun 18616559309

# Re-ejecutar solo los jobs que fallaron
gh run rerun 18616559309 --failed

# Re-ejecutar el último workflow fallido
gh run list --status failure --limit 1 --json databaseId --jq '.[0].databaseId' | xargs gh run rerun
```

**Casos de uso comunes:**

```bash
# 1. El error fue temporal (timeout de red, recurso no disponible)
gh run rerun 18616559309

# 2. Ya corregiste el código y quieres verificar que el workflow pasa
git add .
git commit -m "fix: corregir error"
git push
# El push disparará automáticamente un nuevo workflow

# 3. Quieres re-ejecutar sin hacer push (útil para errores de infraestructura)
gh run rerun 18616559309 --failed

# 4. Monitorear el nuevo run después de re-ejecutar
gh run rerun 18616559309 && gh run watch
```

---

## Diagnosticar Fallos

### 1. Ver logs del paso que falló

```bash
# Ver SOLO los logs de los pasos que fallaron
gh run view 18604907574 --log-failed

# Ver TODOS los logs (exitosos y fallidos)
gh run view 18604907574 --log
```

### 2. Ver logs de un job específico

```bash
# Listar todos los jobs del workflow
gh run view 18604907574 --json jobs --jq '.jobs[] | {name: .name, id: .databaseId, status: .conclusion}'

# Ver logs de un job específico por nombre
gh run view 18604907574 --job=deploy --log

# Ver solo errores del job
gh run view 18604907574 --job=deploy --log | grep -i "error\|failed\|traceback"
```

### 3. Buscar errores específicos en logs

```bash
# Buscar errores de Docker
gh run view 18604907574 --log-failed | grep -i "docker\|build"

# Buscar errores de dependencias (Python)
gh run view 18604907574 --log-failed | grep -i "modulenotfound\|no module"

# Buscar errores de dependencias (Node.js)
gh run view 18604907574 --log-failed | grep -i "cannot find module\|npm err"

# Buscar errores de conexión
gh run view 18604907574 --log-failed | grep -i "connection\|refused\|timeout"

# Buscar códigos de error HTTP
gh run view 18604907574 --log-failed | grep -E "(401|403|404|500|502|503)"
```

### 4. Extraer solo las líneas de error

```bash
# Ver líneas que contienen "Error" o "error"
gh run view 18604907574 --log-failed | grep -i "error"

# Ver traceback de Python
gh run view 18604907574 --log-failed | grep -A 10 "Traceback"

# Ver stack trace de Node.js
gh run view 18604907574 --log-failed | grep -A 15 "Error:"

# Ver mensajes de fallo de Docker
gh run view 18604907574 --log-failed | grep -E "ERROR|failed to|ERROR:"
```

---

## Logs Detallados

### Ver logs con contexto

```bash
# Ver 5 líneas antes y después de cada error
gh run view 18604907574 --log-failed | grep -B 5 -A 5 -i "error"

# Ver 10 líneas después de "Build and push"
gh run view 18604907574 --log | grep -A 10 "Build and push"

# Ver todo el paso específico
gh run view 18604907574 --log | awk '/Build and push/,/Complete job/'
```

### Filtrar por paso específico

```bash
# Ver solo el paso de build
gh run view 18604907574 --log | grep "docker build" -A 50

# Ver solo el paso de tests
gh run view 18604907574 --log | grep "Run Tests" -A 30

# Ver configuración de secrets/env
gh run view 18604907574 --log | grep -i "secret\|environment"
```

---

## Ejemplos Prácticos

### Ejemplo 1: Diagnosticar fallo en Docker Build

**Problema:** El step "Build and push Docker image" falló

```bash
# 1. Ver resumen del workflow
gh run view 18604907574

# 2. Ver SOLO los logs del paso que falló
gh run view 18604907574 --log-failed | grep -A 20 "Build and push"

# 3. Buscar errores específicos de Docker
gh run view 18604907574 --log-failed | grep -i "dockerfile\|docker build\|error"

# 4. Ver si hay problemas con dependencias
gh run view 18604907574 --log-failed | grep -i "no such file\|not found"
```

**Comandos útiles para este caso:**
```bash
# Ver todo el log del job de deploy
gh run view 18604907574 --job=deploy --log

# Guardar logs en un archivo para análisis
gh run view 18604907574 --log-failed > error_logs.txt

# Buscar líneas específicas de Dockerfile
gh run view 18604907574 --log-failed | grep -E "(Step [0-9]+|RUN|COPY|ERROR)"
```

### Ejemplo 2: Diagnosticar fallo en Tests

**Problema:** Los tests de Django/Node.js fallaron

```bash
# 1. Ver qué test falló
gh run view <RUN_ID> --log-failed | grep -i "test\|failed\|error"

# 2. Ver traceback completo (Python)
gh run view <RUN_ID> --log-failed | grep -A 30 "Traceback"

# 3. Ver qué módulos faltan
gh run view <RUN_ID> --log-failed | grep "ModuleNotFoundError"

# 4. Ver errores de base de datos
gh run view <RUN_ID> --log-failed | grep -i "database\|postgres\|connection"

# 5. Ver tests específicos que fallaron
gh run view <RUN_ID> --log-failed | grep "FAILED\|AssertionError"
```

### Ejemplo 3: Diagnosticar fallo en CI/CD Pipeline

**Problema:** El deployment a Kubernetes/Cloud falló

```bash
# 1. Ver logs del job de deployment
gh run view <RUN_ID> --job=deploy --log

# 2. Buscar errores de kubectl
gh run view <RUN_ID> --log-failed | grep -i "kubectl\|kubernetes\|error"

# 3. Ver problemas de conexión con cluster
gh run view <RUN_ID> --log-failed | grep -i "connection refused\|timeout\|unauthorized"

# 4. Ver configuración de secrets
gh run view <RUN_ID> --log | grep -i "secret\|kubeconfig"
```

### Ejemplo 4: Diagnosticar fallo en Health Check de Kubernetes

**Problema:** El paso "Final health check" falló con "No resources found in namespace"

**Síntomas:**
- El deployment se marcó como exitoso ✓
- El "Rolling Update" completó sin errores ✓
- Pero el health check reporta: "No resources found in hector-academy namespace"

**Comandos para diagnosticar:**

```bash
# 1. Ver resumen del workflow
gh run view 53081889997

# 2. Ver SOLO los logs del paso que falló
gh run view 53081889997 --log-failed

# 3. Ver contexto antes del health check
gh run view 53081889997 --log | grep -B 10 -A 10 "Final health check"

# 4. Ver qué pasó en el Rolling Update (que se marcó exitoso)
gh run view 53081889997 --log | grep -A 50 "Rolling Update with Resource Management"

# 5. Ver si hubo warnings durante el deployment
gh run view 53081889997 --log | grep -i "warning\|warn"

# 6. Ver el paso "Wait for all deployments to stabilize"
gh run view 53081889997 --log | grep -A 30 "Wait for all deployments to stabilize"

# 7. Buscar errores de kubectl relacionados con pods
gh run view 53081889997 --log | grep -i "kubectl.*pods\|no resources\|not found"

# 8. Ver si hubo problemas con ImagePull
gh run view 53081889997 --log | grep -i "imagepull\|errimagepull"

# 9. Ver eventos del cluster
gh run view 53081889997 --log | grep "kubectl get events"

# 10. Guardar logs completos para análisis detallado
gh run view 53081889997 --job=deploy --log > deploy_full.log
```

**Posibles causas:**

1. **Pods no se crearon**: El deployment existe pero no genera pods
   ```bash
   gh run view <RUN_ID> --log | grep "kubectl get deployments"
   gh run view <RUN_ID> --log | grep "kubectl get pods"
   ```

2. **Pods crashearon inmediatamente**: Se crearon pero fallaron
   ```bash
   gh run view <RUN_ID> --log | grep -i "crashloopbackoff\|error\|backoff"
   ```

3. **Health check corre demasiado rápido**: Pods aún no están listos
   ```bash
   # Ver timestamps del deploy vs health check
   gh run view <RUN_ID> --log | grep -E "Rolling Update|Wait for|Final health"
   ```

4. **Problema con la imagen Docker**: No puede pull la imagen
   ```bash
   gh run view <RUN_ID> --log | grep -i "image.*not found\|unauthorized"
   ```

5. **Bug en el script de health check**: Lógica incorrecta
   ```bash
   # Ver el script completo del health check
   gh run view <RUN_ID> --log | awk '/Final health check/,/Error: Process completed/'
   ```

**Análisis del log guardado:**

```bash
# Una vez guardado el log, analizar localmente
cat deploy_full.log | grep -B 20 -A 20 "Final health check"

# Ver toda la secuencia del deployment
cat deploy_full.log | grep -E "kubectl (apply|get|rollout|describe)"

# Ver si hay recursos en el namespace
cat deploy_full.log | grep "kubectl get all"
```

**Re-ejecutar el workflow después de corregir:**

```bash
# Una vez identificado y corregido el problema, re-ejecutar el workflow completo
gh run rerun 53081889997

# O re-ejecutar solo el job que falló (deploy)
gh run rerun 53081889997 --failed

# Monitorear el nuevo run en tiempo real
gh run watch

# Ver el estado del nuevo run
gh run list --limit 1
```

**Tip:** Después de hacer cambios en tu código para corregir el problema:

```bash
# 1. Hacer commit y push de los cambios
git add .
git commit -m "fix(k8s): corregir health check timeout"
git push

# 2. El push disparará automáticamente un nuevo workflow
# O puedes re-ejecutar el anterior para confirmar que era temporal
gh run rerun 53081889997

# 3. Comparar los logs del run anterior vs el nuevo
gh run list --limit 2
```

### Ejemplo 5: Ver notificaciones de Slack

```bash
# Ver si las notificaciones se enviaron
gh run view <RUN_ID> --log | grep -i "slack\|notification"

# Ver el webhook utilizado
gh run view <RUN_ID> --log | grep "SLACK_WEBHOOK"

# Ver errores en notificaciones
gh run view <RUN_ID> --log-failed | grep -A 5 "slack"
```

---

## Tips y Trucos

### 1. Aliases útiles

Agrega estos aliases a tu `.bashrc` o `.zshrc`:

```bash
# Ver último workflow
alias ghrl='gh run list --limit 5'

# Watch último workflow
alias ghrw='gh run watch'

# Ver logs del último fallo
alias ghrf='gh run view --log-failed'

# Ver resumen del último run
alias ghrv='gh run view'

# Ver últimos workflows fallidos
alias ghrlf='gh run list --status failure --limit 10'
```

### 2. Buscar en múltiples runs

```bash
# Buscar un error específico en los últimos 10 workflows
for run_id in $(gh run list --limit 10 --json databaseId --jq '.[].databaseId'); do
  echo "=== Checking run $run_id ==="
  gh run view $run_id --log-failed | grep -i "paypalrestsdk" && echo "Found in $run_id"
done
```

### 3. Comparar dos workflows

```bash
# Guardar logs de dos runs diferentes
gh run view 18604907574 --log > run1.log
gh run view 18604764965 --log > run2.log

# Comparar diferencias
diff run1.log run2.log
```

### 4. Ver métricas de tiempo

```bash
# Ver duración de cada job
gh run view <RUN_ID> --json jobs --jq '.jobs[] | {name: .name, duration: .completedAt}'

# Ver tiempo total del workflow
gh run view <RUN_ID> --json status,conclusion,createdAt,updatedAt
```

### 5. Re-ejecutar workflow fallido

```bash
# Re-ejecutar el último workflow fallido
gh run rerun <RUN_ID>

# Re-ejecutar solo los jobs que fallaron
gh run rerun <RUN_ID> --failed
```

### 6. Descargar artefactos

```bash
# Listar artefactos de un workflow
gh run view <RUN_ID> --json artifacts --jq '.artifacts[] | {name: .name, size: .size_in_bytes}'

# Descargar todos los artefactos
gh run download <RUN_ID>

# Descargar artefacto específico
gh run download <RUN_ID> -n artifact-name
```

---

## Comandos de Referencia Rápida

### Para diagnóstico rápido de fallos:

```bash
# 1. Ver últimos runs
gh run list --limit 5

# 2. Ver resumen del run que falló
gh run view <RUN_ID>

# 3. Ver solo los errores
gh run view <RUN_ID> --log-failed

# 4. Buscar error específico
gh run view <RUN_ID> --log-failed | grep -i "<término_de_búsqueda>"

# 5. Ver job específico
gh run view <RUN_ID> --job=<nombre_del_job> --log
```

### Para análisis detallado:

```bash
# Ver logs completos
gh run view <RUN_ID> --log > full_logs.txt

# Ver estructura del workflow en JSON
gh run view <RUN_ID> --json

# Ver anotaciones (errores/warnings)
gh run view <RUN_ID> --json checks --jq '.jobs[].steps[] | select(.conclusion=="failure")'

# Ver variables de ambiente usadas
gh run view <RUN_ID> --log | grep -i "env\|export"
```

---

## Flujo de Trabajo Recomendado

### Cuando un workflow falla:

**1. Ver resumen:**
```bash
gh run view <RUN_ID>
```

**2. Identificar el paso que falló:**
- Busca la ❌ o ✗ en la salida

**3. Ver logs del fallo:**
```bash
gh run view <RUN_ID> --log-failed
```

**4. Buscar el error específico:**
```bash
gh run view <RUN_ID> --log-failed | grep -B 5 -A 5 -i "error"
```

**5. Analizar el contexto:**
- Ver qué paso anterior funcionó
- Revisar cambios recientes en código
- Verificar variables de entorno/secrets

**6. Corregir y re-ejecutar:**
```bash
# Hacer los cambios necesarios
git add .
git commit -m "fix: corregir error en workflow"
git push

# O re-ejecutar el mismo workflow sin push
gh run rerun <RUN_ID>
```

---

## Troubleshooting Común

### Error: "No module named 'X'" (Python)

```bash
# Verificar que el módulo esté en requirements.txt
cat requirements.txt | grep -i "<nombre_modulo>"

# Ver el paso de instalación
gh run view <RUN_ID> --log | grep -A 20 "Install requirements"

# Ver errores de pip
gh run view <RUN_ID> --log-failed | grep -i "pip\|could not find"
```

### Error: "Cannot find module" (Node.js)

```bash
# Verificar package.json
cat package.json | grep -i "<nombre_modulo>"

# Ver el paso de npm install
gh run view <RUN_ID> --log | grep -A 20 "npm install"

# Ver errores de npm
gh run view <RUN_ID> --log-failed | grep -i "npm err"
```

### Error: Docker build failed

```bash
# Ver errores de Dockerfile
gh run view <RUN_ID> --log-failed | grep -E "Step [0-9]+|RUN|ERROR"

# Ver si hay problemas con COPY
gh run view <RUN_ID> --log-failed | grep "COPY\|no such file"

# Ver problemas con capas de Docker
gh run view <RUN_ID> --log-failed | grep -i "layer\|cache"
```

### Error: Tests fallaron

```bash
# Ver qué tests corrieron
gh run view <RUN_ID> --log | grep "test_\|Test"

# Ver traceback
gh run view <RUN_ID> --log-failed | grep -A 30 "Traceback"

# Ver assertions fallidas
gh run view <RUN_ID> --log-failed | grep "AssertionError\|FAILED"
```

### Error: Secrets no configurados

```bash
# Listar secrets del repo
gh secret list

# Ver si un secret específico existe
gh secret list | grep SENTRY_DSN

# Agregar un nuevo secret
gh secret set SECRET_NAME

# Eliminar un secret
gh secret delete SECRET_NAME
```

### Error: Permisos insuficientes

```bash
# Ver errores de permisos
gh run view <RUN_ID> --log-failed | grep -i "permission\|denied\|unauthorized"

# Verificar token de GitHub
gh auth status

# Re-autenticar si es necesario
gh auth login
```

---

## 🎯 Resumen de Comandos Esenciales

| Acción | Comando |
|--------|---------|
| Ver últimos workflows | `gh run list --limit 5` |
| Ver workflows fallidos | `gh run list --status failure --limit 10` |
| Ver resumen de un workflow | `gh run view <RUN_ID>` |
| Ver logs de fallos | `gh run view <RUN_ID> --log-failed` |
| Watch en tiempo real | `gh run watch <RUN_ID>` |
| Buscar errores | `gh run view <RUN_ID> --log-failed \| grep -i "error"` |
| Re-ejecutar workflow | `gh run rerun <RUN_ID>` |
| Re-ejecutar solo fallos | `gh run rerun <RUN_ID> --failed` |
| Ver un job específico | `gh run view <RUN_ID> --job=deploy --log` |
| Listar secrets | `gh secret list` |
| Descargar artefactos | `gh run download <RUN_ID>` |
| Cancelar workflow | `gh run cancel <RUN_ID>` |

---

## 📚 Recursos Relacionados

- **[COMMIT_GUIDE.md](COMMIT_GUIDE.md)** - Guía de mensajes de commit
- [GitHub CLI Docs](https://cli.github.com/manual/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [gh run reference](https://cli.github.com/manual/gh_run)

---

## 🔗 Enlaces Útiles

**Ver workflows en GitHub Web:**
```
https://github.com/<OWNER>/<REPO>/actions
```

**Ver un run específico:**
```
https://github.com/<OWNER>/<REPO>/actions/runs/<RUN_ID>
```

**Documentación oficial de gh CLI:**
- https://cli.github.com/manual/gh_run
- https://cli.github.com/manual/gh_run_view
- https://cli.github.com/manual/gh_run_watch

---

## 🤝 Contribuir

¿Encontraste un bug o tienes una mejora?

1. Abre un [Issue](https://github.com/Hello-World-SpA/devtools/issues)
2. Describe el problema o mejora propuesta
3. Si es posible, incluye un ejemplo de uso

---

**¿Dudas o sugerencias?** Abre un [Issue](https://github.com/Hello-World-SpA/devtools/issues)

---

**Última actualización:** 18 Oct 2025