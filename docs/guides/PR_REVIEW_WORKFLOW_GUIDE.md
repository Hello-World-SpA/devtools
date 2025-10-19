# Guía de Flujo de Trabajo de Pull Requests con Doble Revisión

## Tabla de Contenidos

- [Introducción](#introducción)
- [Cómo Funciona el Flujo](#cómo-funciona-el-flujo)
- [Beneficios del Sistema](#beneficios-del-sistema)
- [Comandos Esenciales de gh](#comandos-esenciales-de-gh)
- [Flujos de Trabajo Prácticos](#flujos-de-trabajo-prácticos)
- [Mejores Prácticas](#mejores-prácticas)
- [Ejemplos Reales](#ejemplos-reales)
- [Solución de Problemas](#solución-de-problemas)

---

## Introducción

Este repositorio implementa un sistema de **revisión de código con doble capa** que requiere **2 aprobaciones** antes de hacer merge a `main`. Esto asegura calidad de código y conocimiento compartido del equipo.

### Reglas del Repositorio

- ✅ Se requieren **2 aprobaciones** para hacer merge
- ✅ Los desarrolladores **NO pueden aprobar sus propios PRs**
- ✅ Los desarrolladores **NO pueden hacer push directo a `main`**
- ✅ El admin (yllorca) puede hacer bypass en casos de emergencia

---

## Cómo Funciona el Flujo

### Escenario 1: SubaruDev0 crea un PR

```
1. SubaruDev0 crea PR: feature/nueva-funcionalidad
   └── Estado: ⚠️ 0/2 aprobaciones

2. LondonDev-01 revisa y aprueba (peer review)
   └── Estado: ⚠️ 1/2 aprobaciones (bloqueado)

3. yllorca revisa y aprueba (admin review)
   └── Estado: ✅ 2/2 aprobaciones (listo para merge)
```

### Escenario 2: LondonDev-01 crea un PR

```
1. LondonDev-01 crea PR: fix/correccion-bug
   └── Estado: ⚠️ 0/2 aprobaciones

2. SubaruDev0 revisa y aprueba (peer review)
   └── Estado: ⚠️ 1/2 aprobaciones (bloqueado)

3. yllorca revisa y aprueba (admin review)
   └── Estado: ✅ 2/2 aprobaciones (listo para merge)
```

### Estados de un PR

#### PR Bloqueado (0 aprobaciones)

```
Pull Request #456: "Agregar autenticación OAuth"
by SubaruDev0

Reviewers:
├── LondonDev-01  ⏳ Review requested
├── yllorca       ⏳ Review requested

Checks:
├── ⚠️ 0 of 2 required approvals
├── ✅ All conversations resolved
└── 🔒 Merge blocked
```

#### PR con 1 Aprobación (aún bloqueado)

```
Pull Request #456: "Agregar autenticación OAuth"
by SubaruDev0

Reviewers:
├── LondonDev-01  ✅ Approved
├── yllorca       ⏳ Review requested

Checks:
├── ⚠️ 1 of 2 required approvals
├── ✅ All conversations resolved
└── 🔒 Merge blocked (1 more approval needed)
```

#### PR Listo para Merge (2 aprobaciones)

```
Pull Request #456: "Agregar autenticación OAuth"
by SubaruDev0

Reviewers:
├── LondonDev-01  ✅ Approved
├── yllorca       ✅ Approved

Checks:
├── ✅ 2 of 2 required approvals
├── ✅ All conversations resolved
└── 🎉 Ready to merge!
```

---

## Beneficios del Sistema

### 1. Revisión Entre Pares (Peer Review)

- ✅ Los desarrolladores revisan el código del otro
- ✅ Aprenden de las soluciones de sus compañeros
- ✅ Mantienen estándares consistentes
- ✅ Detectan errores más rápido

### 2. Capa de Supervisión (Admin Review)

- ✅ El admin ve todo el código antes de llegar a main
- ✅ Valida decisiones arquitectónicas
- ✅ Asegura calidad general del proyecto
- ✅ Tiene visibilidad completa del desarrollo

### 3. Mejor Calidad de Código

- 🔍 Doble revisión = menos bugs en producción
- 📚 Conocimiento compartido del equipo
- 🎯 Código más legible y mantenible
- 💡 Mentoría continua entre desarrolladores

---

## Comandos Esenciales de gh

### Ver PRs Pendientes

#### Ver PRs que esperan tu revisión

```bash
gh pr list --search "review-requested:@me"
```

**Salida esperada:**
```
#456  Agregar autenticación OAuth          feature/oauth-auth   SubaruDev0
#457  Corregir validación de formularios   fix/form-validation  LondonDev-01
```

#### Ver todos los PRs abiertos

```bash
gh pr list
```

#### Ver PRs por estado

```bash
# Solo PRs aprobados
gh pr list --search "review:approved"

# PRs con cambios solicitados
gh pr list --search "review:changes_requested"

# PRs creados por ti
gh pr list --author "@me"
```

### Revisar PRs

#### Ver detalles de un PR

```bash
gh pr view 456
```

**Incluye:**
- Título y descripción
- Estado de aprobaciones
- Checks en ejecución
- Comentarios y conversaciones

#### Ver detalles en formato JSON

```bash
gh pr view 456 --json reviewDecision,reviews,statusCheckRollup
```

#### Ver los cambios (diff) de un PR

```bash
gh pr diff 456
```

#### Hacer checkout de un PR para probar localmente

```bash
gh pr checkout 456
```

Esto crea una rama local y te posiciona en ella para probar los cambios.

### Aprobar PRs

#### Aprobar un PR

```bash
gh pr review 456 --approve
```

#### Aprobar con comentario

```bash
gh pr review 456 --approve -b "Excelente trabajo! El código se ve limpio y bien documentado."
```

#### Aprobar desde un archivo con comentario largo

```bash
gh pr review 456 --approve --body-file review-comment.md
```

### Solicitar Cambios

#### Solicitar cambios con comentario

```bash
gh pr review 456 --request-changes -b "Por favor agrega validación en línea 45 para evitar valores nulos."
```

#### Comentar sin aprobar ni rechazar

```bash
gh pr review 456 --comment -b "Algunas sugerencias menores, pero se ve bien en general."
```

### Crear y Gestionar PRs

#### Crear un PR desde tu rama actual

```bash
gh pr create --title "Agregar autenticación OAuth" --body "Implementa login con Google OAuth 2.0"
```

#### Crear PR interactivamente

```bash
gh pr create
```

Te preguntará:
- Título del PR
- Descripción
- Rama base (main)
- Asignar reviewers

#### Asignar reviewers a un PR existente

```bash
gh pr edit 456 --add-reviewer LondonDev-01,yllorca
```

#### Hacer merge de un PR (solo con permisos)

```bash
gh pr merge 456
```

Opciones de merge:
```bash
# Merge commit (mantiene historial completo)
gh pr merge 456 --merge

# Squash (combina commits en uno solo)
gh pr merge 456 --squash

# Rebase (aplica commits uno por uno)
gh pr merge 456 --rebase
```

### Comandos de Búsqueda Avanzada

#### PRs pendientes de revisión por usuario específico

```bash
gh pr list --search "review-requested:LondonDev-01"
```

#### PRs bloqueados esperando aprobaciones

```bash
gh pr list --search "status:failure"
```

#### PRs listos para merge

```bash
gh pr list --search "status:success review:approved"
```

#### Combinar criterios

```bash
gh pr list --search "review-requested:@me status:success"
```

---

## Flujos de Trabajo Prácticos

### Flujo Diario de un Desarrollador

#### 1. Comenzar el día

```bash
# Ver qué PRs necesitan tu revisión
gh pr list --search "review-requested:@me"

# Ver tus PRs abiertos
gh pr list --author "@me"
```

#### 2. Revisar un PR

```bash
# Ver detalles del PR
gh pr view 456

# Ver los cambios
gh pr diff 456

# Hacer checkout para probar localmente
gh pr checkout 456

# Ejecutar tests
npm test  # o el comando de test de tu proyecto

# Si todo está bien, aprobar
gh pr review 456 --approve -b "Probado localmente, funciona correctamente!"

# Si necesita cambios
gh pr review 456 --request-changes -b "Por favor revisa el manejo de errores en auth.js:45"

# Regresar a tu rama
git checkout tu-rama-de-trabajo
```

#### 3. Crear un PR

```bash
# Asegúrate de estar en tu rama
git checkout feature/nueva-funcionalidad

# Push de tus cambios
git push -u origin feature/nueva-funcionalidad

# Crear el PR
gh pr create --title "feat: agregar validación de email" \
  --body "Agrega validación de formato de email en formulario de registro" \
  --reviewer LondonDev-01,yllorca
```

### Flujo del Admin (yllorca)

#### Revisar todos los PRs pendientes

```bash
# Ver todos los PRs abiertos
gh pr list

# Ver PRs que necesitan tu revisión
gh pr list --search "review-requested:yllorca"

# Ver PRs con 1 aprobación (esperan tu segunda aprobación)
gh pr list --search "review:approved"
```

#### Revisar y aprobar PR

```bash
# Ver PR completo
gh pr view 456

# Ver cambios
gh pr diff 456

# Aprobar (segunda aprobación = listo para merge)
gh pr review 456 --approve -b "Validación arquitectónica aprobada. Listo para merge."

# Hacer merge
gh pr merge 456 --squash
```

#### Bypass en emergencias

```bash
# En caso de hotfix urgente, puedes hacer merge directo
# (tienes permisos de bypass)
gh pr merge 456 --admin --squash
```

### Flujo de Peer Review entre Desarrolladores

**SubaruDev0 revisa PR de LondonDev-01:**

```bash
# Ver PR de LondonDev-01
gh pr view 457

# Checkout para probar
gh pr checkout 457

# Probar los cambios
npm run dev
npm test

# Si hay un problema menor
gh pr review 457 --comment -b "Funciona bien, pero considera usar const en lugar de let en línea 23"

# Si hay problemas que bloquean merge
gh pr review 457 --request-changes -b "Falta manejo de error cuando el API no responde"

# Si todo está perfecto
gh pr review 457 --approve -b "Código limpio y bien testeado. Aprobado!"

# Regresar a tu rama
git checkout -
```

---

## Mejores Prácticas

### Para Creadores de PRs

#### 1. Descripción Clara

Usa este template:

```markdown
## ¿Qué hace este PR?
Agrega autenticación OAuth con Google

## ¿Por qué?
Para permitir login sin crear cuenta nueva y mejorar UX

## ¿Cómo probarlo?
1. Ir a /login
2. Clic en "Login with Google"
3. Verificar que redirecciona correctamente al dashboard
4. Verificar que se crea la sesión

## Checklist
- [x] Tests agregados
- [x] Documentación actualizada
- [x] Variables de entorno documentadas en .env.example
- [x] Sin errores de linter
```

#### 2. PRs Pequeños

- ✅ 1 feature o fix por PR
- ✅ Máximo 300-400 líneas cambiadas
- ✅ Fácil de revisar en 15-20 minutos
- ❌ Evitar PRs gigantes con múltiples features

#### 3. Commits Limpios

```bash
# Buenos commits
feat: agregar OAuth login
fix: corregir validación de email
docs: actualizar README con setup de OAuth

# Malos commits
update
changes
fix stuff
wip
```

### Para Reviewers

#### 1. Revisión Rápida

- ⏰ Revisar PRs el mismo día (máximo 24 horas)
- 🎯 Enfocarse en lógica, no solo estilo
- 💬 Comentarios constructivos y específicos

#### 2. Qué Revisar

**Checklist de revisión:**

```
□ ¿El código hace lo que dice que hace?
□ ¿Hay tests adecuados?
□ ¿Maneja errores correctamente?
□ ¿Es legible y mantenible?
□ ¿Sigue los estándares del proyecto?
□ ¿Hay código duplicado que debería refactorizarse?
□ ¿Las variables y funciones tienen nombres claros?
□ ¿Hay documentación si es necesario?
```

#### 3. Tipos de Comentarios

**Comentario de sugerencia:**
```
💡 Sugerencia: Podrías usar `Array.filter()` aquí para simplificar el código
```

**Comentario de problema:**
```
⚠️ Esto podría causar un error si `user` es null. Agrega validación.
```

**Comentario de aprobación:**
```
✅ Excelente manejo de errores aquí!
```

#### 4. Usar GitHub Conversations

```bash
# Ver conversaciones abiertas
gh pr view 456 --comments

# Marcar conversación como resuelta solo desde la web
# (gh cli no tiene comando para esto aún)
```

---

## Ejemplos Reales

### Ejemplo 1: Revisar PR con Cambios Necesarios

```bash
# SubaruDev0 creó PR #458
$ gh pr view 458

Pull Request #458: feat: agregar carrito de compras
SubaruDev0 wants to merge 15 commits into main from feature/shopping-cart

# LondonDev-01 revisa
$ gh pr checkout 458
$ npm test

# Oh no, 2 tests fallan!
$ gh pr review 458 --request-changes -b "$(cat <<'EOF'
Encontré algunos problemas:

1. ❌ Test `should add item to cart` falla
2. ❌ Test `should calculate total` falla
3. ⚠️ Falta validación cuando quantity < 0
4. 💡 Considera agregar un límite máximo de items

Por favor corrígelos y volveré a revisar.
EOF
)"

# SubaruDev0 hace los cambios y pushea
$ gh pr view 458
# Ahora muestra: "Changes requested by LondonDev-01"

# LondonDev-01 revisa de nuevo
$ git pull  # actualizar rama local
$ npm test  # ✅ Todos pasan

$ gh pr review 458 --approve -b "Todos los problemas resueltos. Aprobado!"

# Ahora solo falta aprobación de yllorca
```

### Ejemplo 2: Flujo Completo Exitoso

```bash
# LondonDev-01 crea feature
$ git checkout -b feature/email-notifications
# ... hace cambios ...
$ git add .
$ git commit -m "feat: agregar notificaciones por email"
$ git push -u origin feature/email-notifications

$ gh pr create --title "feat: agregar notificaciones por email" \
  --body "$(cat <<'EOF'
## ¿Qué hace este PR?
Implementa sistema de notificaciones por email usando SendGrid

## ¿Por qué?
Los usuarios solicitaron recibir alertas por email

## ¿Cómo probarlo?
1. Configurar SENDGRID_API_KEY en .env
2. Registrar nuevo usuario
3. Verificar que llega email de bienvenida

## Checklist
- [x] Tests agregados (email.test.js)
- [x] Variables documentadas en .env.example
- [x] Rate limiting implementado
EOF
)" --reviewer SubaruDev0,yllorca

# SubaruDev0 recibe notificación
$ gh pr list --search "review-requested:@me"
#459  feat: agregar notificaciones por email  feature/email-notifications  LondonDev-01

$ gh pr checkout 459
$ npm test  # ✅ Pasa
$ npm run dev  # prueba manual

$ gh pr review 459 --approve -b "Probado localmente. El sistema de rate limiting es buena idea. Aprobado!"

# yllorca hace segunda revisión
$ gh pr view 459
# Ve que ya tiene 1 aprobación de SubaruDev0

$ gh pr diff 459  # revisa cambios

$ gh pr review 459 --approve -b "Arquitectura sólida. Aprobado para merge."

# Ahora tiene 2/2 aprobaciones
$ gh pr merge 459 --squash

✓ Merged Pull Request #459 (feat: agregar notificaciones por email)
```

### Ejemplo 3: Admin Bypass de Emergencia

```bash
# Hotfix crítico en producción
$ git checkout -b hotfix/critical-security-patch
# ... arregla vulnerabilidad ...
$ git push -u origin hotfix/critical-security-patch

$ gh pr create --title "hotfix: critical security patch" \
  --body "Corrige vulnerabilidad CVE-2024-XXXX en dependencia"

# Como admin, yllorca puede hacer bypass
$ gh pr merge 460 --admin --squash

⚠️  Bypassing required reviews
✓ Merged Pull Request #460 (hotfix: critical security patch)

# Notificar al equipo del merge urgente
```

---

## Solución de Problemas

### Problema: No puedo hacer merge de mi PR

**Síntoma:**
```
! Pull request #456 is not mergeable: does not have the required approving reviews
```

**Solución:**
- Verifica que tienes 2 aprobaciones: `gh pr view 456 --json reviews`
- Si tienes solo 1, espera la segunda aprobación
- No puedes aprobar tu propio PR

### Problema: Mi aprobación no cuenta

**Síntoma:**
Tu aprobación aparece pero el PR sigue bloqueado.

**Causas posibles:**
1. Eres el autor del PR (no puedes aprobar tus propios PRs)
2. Hay cambios solicitados por otro reviewer que no se han resuelto
3. Hay conflicts que resolver

**Solución:**
```bash
gh pr view 456 --json reviewDecision,reviews
```

### Problema: Conflicto con main

**Síntoma:**
```
! Pull request #456 has conflicts with the base branch
```

**Solución:**
```bash
# Checkout del PR
gh pr checkout 456

# Actualizar con main
git fetch origin main
git merge origin/main

# Resolver conflictos
# ... editar archivos ...
git add .
git commit -m "chore: resolve merge conflicts"

# Push
git push
```

### Problema: gh command not found

**Solución:**

```bash
# macOS (Homebrew)
brew install gh

# Autenticar
gh auth login
```

### Problema: Ver por qué un PR está bloqueado

```bash
# Ver status checks y reviews
gh pr checks 456
gh pr view 456 --json statusCheckRollup,reviews

# Ver si hay conversaciones sin resolver
gh pr view 456 --comments
```

---

## Comandos de Referencia Rápida

```bash
# 📋 VER PRs
gh pr list                                    # Todos los PRs
gh pr list --search "review-requested:@me"   # PRs pendientes de tu revisión
gh pr list --author "@me"                    # Tus PRs
gh pr view 456                               # Ver detalles de PR

# 👀 REVISAR
gh pr diff 456                               # Ver cambios
gh pr checkout 456                           # Probar localmente
gh pr checks 456                             # Ver status de checks

# ✅ APROBAR
gh pr review 456 --approve                   # Aprobar
gh pr review 456 --approve -b "mensaje"      # Aprobar con comentario

# ⚠️ SOLICITAR CAMBIOS
gh pr review 456 --request-changes -b "..."  # Solicitar cambios
gh pr review 456 --comment -b "..."          # Comentar sin aprobar/rechazar

# 🚀 CREAR Y GESTIONAR
gh pr create                                 # Crear PR (interactivo)
gh pr create --title "..." --body "..."      # Crear PR directo
gh pr edit 456 --add-reviewer usuario        # Agregar reviewer

# 🔀 MERGE
gh pr merge 456                              # Merge (con 2 aprobaciones)
gh pr merge 456 --squash                     # Squash merge
gh pr merge 456 --admin                      # Admin bypass (solo yllorca)

# 🔍 BÚSQUEDA AVANZADA
gh pr list --search "status:success review:approved"
gh pr list --search "review-requested:usuario"
gh pr view 456 --json reviews,reviewDecision
```

---

## Recursos Adicionales

- 📖 [Documentación oficial de gh CLI](https://cli.github.com/manual/)
- 🔗 [GitHub CLI Reference](https://cli.github.com/manual/gh_pr)
- 💬 Para dudas, preguntar en el chat del equipo

---

## Resumen

Este flujo de trabajo implementa:

1. **🛡️ Doble capa de revisión**
   - Peer review (desarrollador a desarrollador)
   - Admin review (supervisión técnica)

2. **📚 Aprendizaje continuo**
   - Los desarrolladores aprenden revisando código del otro
   - Estándares consistentes en el equipo

3. **🎯 Alta calidad**
   - Código revisado por 2 personas mínimo
   - Menos bugs en producción
   - Mejor mantenibilidad

4. **👁️ Visibilidad completa**
   - El admin ve todo antes de merge
   - Validación de arquitectura y decisiones técnicas

**¡Usa `gh` para hacer el proceso rápido y eficiente!**