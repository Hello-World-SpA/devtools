# Guía de Conversaciones y Checklists en Pull Requests

## Tabla de Contenidos

- [Introducción](#introducción)
- [Conversaciones vs Comentarios](#conversaciones-vs-comentarios)
- [Require Conversation Resolution](#require-conversation-resolution)
- [Cómo Usar Conversaciones](#cómo-usar-conversaciones)
- [Checklists en PRs](#checklists-en-prs)
- [Templates de PR con Checklists](#templates-de-pr-con-checklists)
- [Comandos gh para Conversaciones](#comandos-gh-para-conversaciones)
- [Mejores Prácticas](#mejores-prácticas)
- [Ejemplos Reales](#ejemplos-reales)

---

## Introducción

Esta guía explica cómo usar **conversaciones** (conversations) y **checklists** en Pull Requests de GitHub para:

- ✅ Asegurar que todos los comentarios de revisión sean atendidos
- ✅ Prevenir que se olviden tareas importantes antes del merge
- ✅ Mejorar la comunicación entre revisores y autores
- ✅ Mantener un registro claro de decisiones tomadas

---

## Conversaciones vs Comentarios

### ¿Qué es un Comentario Simple?

Un **comentario simple** es informativo y no requiere acción:

```
✨ "Excelente refactor aquí!"
💡 "FYI: Este patrón lo usamos también en el módulo de auth"
📚 "Para referencia futura: https://docs.example.com/best-practices"
```

**Características:**
- No bloquea el merge
- Solo proporciona información
- No requiere respuesta obligatoria

### ¿Qué es una Conversación?

Una **conversación** (conversation/thread) requiere resolución:

```
⚠️ "Falta validación cuando user es null en línea 45"
🔍 "¿Por qué usamos setTimeout aquí? ¿No deberíamos usar Promises?"
💡 "Considera usar Array.filter() en lugar de este loop manual"
```

**Características:**
- **Requiere resolución antes del merge** (si está habilitada la regla)
- Implica una acción o cambio necesario
- Crea un thread de discusión
- Puede marcarse como "Resolved" ✅

---

## Require Conversation Resolution

### ¿Qué es?

Es una **regla de protección de rama** que impide hacer merge hasta que todas las conversaciones estén marcadas como "resueltas".

### ¿Cómo funciona?

#### Flujo Típico:

```
1. Revisor inicia conversación:
   "Este código podría optimizarse usando list comprehension"

2. Autor responde y hace cambios:
   "Tienes razón, lo cambio en el próximo commit"
   [Hace commit abc123 con el cambio]

3. Revisor verifica y resuelve:
   "Perfecto, se ve bien ahora"
   [Marca como "Resolved" ✅]

4. GitHub permite el merge:
   ✅ All conversations resolved
   ✅ Ready to merge
```

### Estados de un PR con Conversaciones

#### PR Bloqueado (conversaciones sin resolver)

```
Pull Request #456: "Agregar autenticación OAuth"

Checks:
├── ✅ 2 of 2 required approvals
├── ⚠️ 3 conversations not resolved
│   ├── Thread 1: Validación de email
│   ├── Thread 2: Manejo de errores de API
│   └── Thread 3: Tests faltantes
└── 🔒 Merge blocked until conversations are resolved
```

#### PR Listo (conversaciones resueltas)

```
Pull Request #456: "Agregar autenticación OAuth"

Checks:
├── ✅ 2 of 2 required approvals
├── ✅ All conversations resolved (3/3)
└── ✅ Ready to merge
```

### Beneficios

#### 1. Evita Merges Prematuros

**❌ Sin esta regla:**
```
Revisor: "Hay un bug crítico en línea 45"
[Autor hace merge sin ver el comentario]
[Bug llega a producción 🔥]
```

**✅ Con esta regla:**
```
Revisor: "Hay un bug crítico en línea 45"
[Botón de merge bloqueado 🔒]
Autor: DEBE resolver el problema primero
[Bug se evita ✅]
```

#### 2. Asegura que Nada se Olvide

- Todos los comentarios son atendidos
- Ninguna sugerencia queda en el aire
- Mejor calidad de código
- Menos bugs en producción

#### 3. Documentación Clara

- Registro de qué se discutió
- Cómo se resolvió cada tema
- Útil para auditorías futuras
- Historia de decisiones técnicas

### ¿Quién Puede Resolver Conversaciones?

En GitHub, pueden resolver conversaciones:

1. **El autor del comentario** (el revisor que inició la conversación)
2. **El autor del PR** (quien creó el pull request)
3. **Colaboradores con permisos de write o superior**

**Recomendación:** Es mejor que el **revisor que inició la conversación** la marque como resuelta después de verificar que el cambio es correcto.

---

## Cómo Usar Conversaciones

### En la Interfaz Web de GitHub

#### Iniciar una Conversación

1. Ve al PR en GitHub
2. Ve a la pestaña "Files changed"
3. Haz hover sobre una línea de código
4. Click en el ícono "+"
5. Escribe tu comentario
6. Click en "Start a review" o "Add single comment"

#### Marcar como Resuelta

1. Ve a la conversación en el PR
2. El autor responde y hace los cambios
3. El revisor verifica los cambios
4. Click en "Resolve conversation"

### Usando gh CLI

#### Ver comentarios y conversaciones

```bash
# Ver todos los comentarios de un PR
gh pr view 456 --comments

# Ver detalles del PR incluyendo conversaciones
gh pr view 456
```

**Salida esperada:**
```
Pull Request #456
...

Conversations:
──────────────────────────────────────────────
@LondonDev-01 commented on src/auth.js:45
⚠️ UNRESOLVED

Falta validación cuando user es null

  @SubaruDev0 replied:
  Tienes razón, voy a agregarlo

──────────────────────────────────────────────
@yllorca commented on src/api.js:120
✅ RESOLVED

Considera usar async/await en lugar de .then()

  @SubaruDev0 replied:
  Cambiado en commit abc123
```

#### Agregar comentarios con gh

```bash
# Comentar en el PR en general
gh pr comment 456 --body "Necesitamos agregar tests para esta funcionalidad"

# Comentar en línea específica (requiere usar la API)
gh api repos/:owner/:repo/pulls/456/reviews \
  -f body="Comentario de revisión" \
  -f event=COMMENT
```

**Nota:** gh CLI actualmente no soporta marcar conversaciones como resueltas directamente. Esto debe hacerse desde la interfaz web.

---

## Checklists en PRs

### ¿Qué son los Checklists?

Los **checklists** son listas de tareas en la descripción del PR usando markdown:

```markdown
## Checklist

- [x] Tests agregados
- [x] Documentación actualizada
- [ ] Performance verificado
- [ ] Revisión de seguridad
```

GitHub renderiza esto como checkboxes interactivas que puedes marcar/desmarcar.

### Beneficios de los Checklists

1. **Visibilidad inmediata** - Ver qué falta de un vistazo
2. **Responsabilidad** - El autor sabe qué debe completar
3. **Estandarización** - Todos los PRs siguen los mismos criterios
4. **Calidad** - No se olvidan pasos importantes

### Sintaxis de Checklists

```markdown
## Checklist Pre-Merge

- [ ] Tarea pendiente
- [x] Tarea completada
- [ ] Otra tarea pendiente
```

**Atajos:**
- `- [ ]` = checkbox vacía (pendiente)
- `- [x]` = checkbox marcada (completada)

### Tipos de Checklists Útiles

#### 1. Checklist del Autor (Pre-Review)

```markdown
## Checklist del Autor

- [x] El código compila sin errores
- [x] Todos los tests pasan
- [x] No hay console.log() o código de debug
- [x] Variables y funciones tienen nombres descriptivos
- [ ] Agregué tests para los nuevos cambios
- [ ] Actualicé la documentación si es necesario
- [ ] Verifiqué que no hay regresiones
```

#### 2. Checklist de Testing

```markdown
## Checklist de Testing

- [x] Tests unitarios agregados
- [x] Tests de integración actualizados
- [ ] Tests end-to-end si es necesario
- [x] Cobertura de tests >80%
- [x] Tests pasan en CI/CD
```

#### 3. Checklist de Seguridad

```markdown
## Checklist de Seguridad

- [x] No hay API keys o secrets en el código
- [x] Inputs del usuario están validados
- [x] Queries a BD usan prepared statements
- [x] Autenticación y autorización verificadas
- [ ] Dependencias actualizadas sin vulnerabilidades
```

#### 4. Checklist de Revisión (Para Revisores)

```markdown
## Para el Revisor

Verifica:
- [ ] El código hace lo que dice que hace
- [ ] La lógica es clara y mantenible
- [ ] Manejo de errores es adecuado
- [ ] No hay código duplicado
- [ ] Tests cubren casos edge
```

---

## Templates de PR con Checklists

### Template Básico

```markdown
## ¿Qué hace este PR?

[Descripción breve del cambio]

## ¿Por qué?

[Razón del cambio]

## ¿Cómo probarlo?

1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

## Checklist

- [ ] Tests agregados
- [ ] Documentación actualizada
- [ ] Sin errores de linter
- [ ] Probado localmente
```

### Template Completo (Feature Nueva)

```markdown
## 🎯 ¿Qué hace este PR?

Agrega autenticación OAuth con Google y GitHub

## 💡 ¿Por qué?

Los usuarios solicitaron login social para no crear cuentas nuevas

## 📋 Cambios Principales

- Implementación de OAuth 2.0
- Integración con Google API
- Integración con GitHub API
- Manejo de sesiones con JWT

## 🧪 ¿Cómo probarlo?

### Setup

1. Agregar keys en `.env`:
   ```
   GOOGLE_CLIENT_ID=xxx
   GOOGLE_CLIENT_SECRET=xxx
   GITHUB_CLIENT_ID=xxx
   GITHUB_CLIENT_SECRET=xxx
   ```

2. Instalar dependencias:
   ```bash
   npm install
   ```

### Pruebas Manuales

1. Ir a `/login`
2. Click en "Login with Google"
3. Verificar redirección a Google
4. Autorizar la app
5. Verificar que redirecciona al dashboard
6. Verificar que se creó la sesión

### Repetir con GitHub

1. Ir a `/login`
2. Click en "Login with GitHub"
3. Seguir flujo similar

## ✅ Checklist del Autor

### Código
- [x] El código compila sin errores
- [x] Todos los tests pasan localmente
- [x] Sin console.log() o código de debug
- [x] Variables con nombres descriptivos
- [x] Código sigue convenciones del proyecto

### Testing
- [x] Tests unitarios agregados (`auth.test.js`)
- [x] Tests de integración agregados (`oauth-flow.test.js`)
- [x] Cobertura >85%
- [x] Tests pasan en CI/CD
- [ ] Tests e2e (opcional para este PR)

### Documentación
- [x] Variables de entorno documentadas en `.env.example`
- [x] README actualizado con setup de OAuth
- [x] Comentarios en código complejo
- [ ] Swagger/API docs actualizados (no aplica)

### Seguridad
- [x] No hay secrets en el código
- [x] Tokens almacenados de forma segura
- [x] Validación de inputs implementada
- [x] Rate limiting configurado
- [x] CSRF protection habilitado

### Performance
- [x] Sin queries N+1
- [x] Caching implementado donde corresponde
- [ ] Lazy loading (no necesario)

## 🔍 Para el Revisor

Por favor verifica:
- [ ] Flujo OAuth es seguro
- [ ] Manejo de errores es robusto
- [ ] Tests cubren casos edge
- [ ] No hay vulnerabilidades de seguridad
- [ ] Documentación es clara

## 📸 Screenshots (opcional)

[Si aplica, agregar screenshots del UI]

## 🔗 Referencias

- [Google OAuth Docs](https://developers.google.com/identity/protocols/oauth2)
- [GitHub OAuth Docs](https://docs.github.com/en/apps/oauth-apps)
- Issue relacionado: #123
```

### Template para Bug Fix

```markdown
## 🐛 Bug Fix

Corrige error de validación en formulario de registro

## 📝 Descripción del Bug

El formulario de registro permitía emails sin el símbolo @

## 🔧 Solución

Agregada validación regex para formato de email

## 🧪 ¿Cómo probarlo?

1. Ir a `/register`
2. Intentar registrar con email inválido: `usuario.com`
3. Verificar que muestra error: "Email inválido"
4. Probar con email válido: `usuario@example.com`
5. Verificar que permite el registro

## ✅ Checklist

- [x] Bug reproducido
- [x] Fix implementado
- [x] Test agregado para prevenir regresión
- [x] No afecta otras partes del código
- [x] Probado localmente

## 🔗 Referencias

- Issue: #456 "Emails inválidos son aceptados"
```

### Template para Refactor

```markdown
## ♻️ Refactoring

Refactorizar módulo de autenticación para mejor mantenibilidad

## 🎯 Objetivo

- Separar lógica de negocio de controladores
- Agregar layer de servicios
- Mejorar testeabilidad

## 📋 Cambios

- Creado `AuthService` con lógica de negocio
- Movidos métodos de `AuthController` a servicio
- Agregados tests unitarios para servicio
- Sin cambios en funcionalidad externa

## ⚠️ Breaking Changes

Ninguno - cambios internos solamente

## ✅ Checklist

- [x] Todas las funcionalidades existentes funcionan igual
- [x] Tests existentes siguen pasando
- [x] Nuevos tests agregados
- [x] Cobertura de tests aumentó de 65% a 88%
- [x] No hay cambios en APIs públicas

## 🧪 Verificación

```bash
# Todos los tests deben pasar
npm test

# Coverage aumentado
npm run coverage
```
```

---

## Comandos gh para Conversaciones

### Ver Estado de Conversaciones

```bash
# Ver PR con todos sus detalles
gh pr view 456

# Ver comentarios específicamente
gh pr view 456 --comments

# Ver en JSON (útil para scripts)
gh pr view 456 --json comments
```

### Filtrar PRs con Conversaciones

```bash
# Ver PRs con conversaciones activas (aproximado)
gh pr list --search "comments:>0"

# Ver tus PRs que tienen comentarios
gh pr list --author "@me" --search "comments:>0"
```

### Agregar Comentarios

```bash
# Comentar en el PR
gh pr comment 456 --body "Por favor resuelve los problemas de seguridad antes del merge"

# Comentar desde archivo
gh pr comment 456 --body-file review-notes.md
```

### Ver Diferencias en PR

```bash
# Ver diff completo
gh pr diff 456

# Ver archivos cambiados
gh pr diff 456 --name-only
```

**Nota:** Para marcar conversaciones como resueltas, debes usar la interfaz web de GitHub. gh CLI no tiene comando directo para esto.

---

## Mejores Prácticas

### Para Revisores

#### ✅ Buenas Prácticas

**1. Sé específico y constructivo**

```markdown
✅ BIEN:
"Esta validación debería incluir el caso cuando user.email es null.
Sugiero agregar un check: if (!user?.email) return false;"

❌ MAL:
"Mal"
"Cambiar esto"
```

**2. Usa conversaciones para cambios necesarios**

```markdown
✅ Conversación (requiere acción):
"⚠️ Falta manejo de error cuando la API retorna 500"

✅ Comentario simple (informativo):
"💡 FYI: También usamos este patrón en el módulo de payments"
```

**3. Proporciona contexto**

```markdown
✅ BIEN:
"En línea 45: Esta query podría causar N+1. Considera usar
.select_related('user', 'profile') para optimizar.
Referencia: docs/performance-guide.md"

❌ MAL:
"N+1 aquí"
```

**4. Categoriza tus comentarios**

```markdown
🔴 BLOCKER: Debe corregirse antes del merge
🟡 SUGERENCIA: Nice to have
💡 TIP: Información útil
📚 APRENDE: Recurso educativo
```

**5. Aprueba Y comenta**

```markdown
Puedes aprobar el PR y dejar sugerencias menores:

"Aprobado! El código funciona bien.

Sugerencias para el futuro (no bloquean):
- Considera usar const en lugar de let en línea 23
- Podrías extraer esta lógica a una función helper"
```

### Para Autores de PRs

#### ✅ Buenas Prácticas

**1. Responde antes de resolver**

```markdown
✅ BIEN:
Revisor: "Falta validación de null"
Autor: "Buen punto! Agregué la validación en commit abc123"
[Espera a que el revisor verifique]
[Revisor marca como resuelto]

❌ MAL:
Revisor: "Falta validación de null"
[Autor marca como resuelto sin responder]
```

**2. Usa el checklist proactivamente**

```markdown
✅ Completa el checklist ANTES de pedir revisión:

## Checklist Pre-Review

- [x] Tests agregados
- [x] Linter sin errores
- [x] Probado localmente
- [x] Documentación actualizada

[Pide revisión solo cuando todo esté ✓]
```

**3. Explica cambios complejos**

```markdown
Si un cambio es no-obvio, explícalo:

## Nota sobre implementación

En `auth.js` usé un WeakMap en lugar de Map porque:
1. Previene memory leaks
2. Las keys son objetos que pueden ser garbage collected
3. Mejor performance en este caso de uso

Referencias:
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap
```

**4. Mantén el PR actualizado**

```markdown
Si hay feedback importante, edita la descripción:

## ⚠️ IMPORTANTE (Actualización)

Cambié la estrategia de autenticación de JWT a sesiones
basado en el feedback de @yllorca en conversación #3.

Razón: Mejor seguridad para nuestro caso de uso.
```

**5. Divide PRs grandes**

```markdown
❌ MAL:
Un PR gigante con:
- Nueva feature
- Refactoring
- Bug fixes
- Actualización de deps

✅ BIEN:
PR #1: Actualizar dependencias
PR #2: Refactoring del módulo auth
PR #3: Nueva feature de OAuth
PR #4: Fix bug de validación
```

### Para el Equipo

#### 1. Establece Convenciones

Crea un `.github/pull_request_template.md` en tu repo:

```markdown
## Descripción

[Describe los cambios]

## Tipo de Cambio

- [ ] Bug fix (non-breaking change)
- [ ] Nueva feature (non-breaking change)
- [ ] Breaking change (fix o feature que rompe funcionalidad existente)
- [ ] Refactoring
- [ ] Documentación

## ¿Cómo se probó?

[Describe las pruebas]

## Checklist

- [ ] Mi código sigue las convenciones del proyecto
- [ ] He realizado self-review de mi código
- [ ] He comentado código complejo
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan nuevos warnings
- [ ] He agregado tests
- [ ] Tests nuevos y existentes pasan localmente
- [ ] Cambios dependientes han sido merged
```

#### 2. Define SLAs de Revisión

```markdown
## SLAs del Equipo

- ⏰ Primera revisión: Dentro de 24 horas
- 🔄 Re-revisión después de cambios: Dentro de 4 horas
- 🚨 Hotfixes: Dentro de 2 horas
- 📦 PRs grandes (>500 líneas): Avisar con anticipación
```

#### 3. Etiquetas de PRs

Usa labels para categorizar:

```
🐛 bug          - Bug fixes
✨ feature      - Nuevas features
♻️ refactor     - Refactoring
📚 docs         - Solo documentación
🔒 security     - Seguridad
⚡ performance  - Optimización
🧪 tests        - Tests
```

---

## Ejemplos Reales

### Ejemplo 1: Conversación sobre Bug de Seguridad

**Revisor (LondonDev-01) comenta en `auth.js:45`:**

```markdown
🔴 BLOCKER: Vulnerabilidad de seguridad

Este código permite SQL injection:

```python
query = f"SELECT * FROM users WHERE email = '{email}'"
```

Debe usar prepared statements:

```python
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (email,))
```

Referencias:
- https://owasp.org/www-community/attacks/SQL_Injection
```

**Autor (SubaruDev0) responde:**

```markdown
Tienes toda la razón, gracias por detectarlo!

Cambié a prepared statements en commit abc123.
También agregué un test para verificar que los inputs son sanitizados.

¿Puedes revisar si ahora se ve bien?
```

**Revisor verifica y marca como resuelto:**

```markdown
✅ Perfecto! Ahora está seguro. El test también se ve bien.

Resolviendo esta conversación.
```

### Ejemplo 2: Checklist en Acción

**PR #458: Agregar sistema de notificaciones por email**

```markdown
## 📧 ¿Qué hace este PR?

Implementa sistema de notificaciones por email usando SendGrid

## 🎯 Features

- Email de bienvenida al registrarse
- Notificación de password reset
- Alertas de actividad sospechosa
- Resumen semanal de actividad

## ✅ Checklist del Autor

### Desarrollo
- [x] Código implementado
- [x] Configuración de SendGrid
- [x] Templates de email creados
- [x] Variables de entorno documentadas

### Testing
- [x] Tests unitarios (`email-service.test.js`)
- [x] Tests de integración con mock de SendGrid
- [x] Probado con cuenta real de SendGrid en dev
- [ ] Tests e2e (pendiente - @yllorca ¿es necesario?)

### Seguridad
- [x] Rate limiting (máx 10 emails/hora por usuario)
- [x] Validación de formato de email
- [x] No se exponen emails en logs
- [x] API key en variable de entorno

### Documentación
- [x] README actualizado con setup de SendGrid
- [x] `.env.example` actualizado
- [x] Comentarios en código complejo
- [x] JSDoc agregado a funciones públicas

### Performance
- [x] Emails enviados de forma asíncrona (no bloquean requests)
- [x] Queue implementada para batch sending
- [ ] Monitoring de delivery rates (próximo PR)

## 🔍 Para Revisores

@LondonDev-01 @yllorca

Por favor verifiquen:
- [ ] Lógica de rate limiting es correcta
- [ ] Templates de email se ven bien en diferentes clientes
- [ ] Error handling es robusto
- [ ] No hay vulnerabilidades

**PREGUNTA:** ¿Necesitamos agregar tests e2e o los de integración son suficientes?
```

**Estado en GitHub:**

```
Pull Request #458
├── ✅ 0/2 approvals (waiting)
├── ⏳ 1 conversation active
│   └── @yllorca: "Los tests de integración son suficientes por ahora"
├── ✅ Checklist: 18/20 items completed (90%)
└── ⚠️ Waiting for reviews
```

### Ejemplo 3: Resolución de Conflicto de Diseño

**Revisor (yllorca) inicia conversación en `api.js:120`:**

```markdown
🟡 DISEÑO: Pregunta sobre arquitectura

Veo que estás usando callbacks aquí:

```javascript
fetchUser(id, (error, user) => {
  if (error) handleError(error);
  processUser(user);
});
```

¿Alguna razón específica para no usar async/await?

```javascript
try {
  const user = await fetchUser(id);
  processUser(user);
} catch (error) {
  handleError(error);
}
```

Es más legible y consistente con el resto del código.
```

**Autor (SubaruDev0) responde:**

```markdown
Buena pregunta!

La razón es que `fetchUser` es una función legacy de una librería externa
que solo soporta callbacks. Podría wrappearla en una Promise:

```javascript
const fetchUserAsync = (id) => {
  return new Promise((resolve, reject) => {
    fetchUser(id, (error, user) => {
      if (error) reject(error);
      else resolve(user);
    });
  });
};
```

¿Te parece bien esa solución?
```

**Revisor (yllorca) responde:**

```markdown
Perfecto! Eso es exactamente lo que yo haría.

Incluso podrías usar `util.promisify` si estás en Node.js:

```javascript
const { promisify } = require('util');
const fetchUserAsync = promisify(fetchUser);
```

Cualquiera de las dos opciones está bien. Marca como resuelto cuando lo implementes.
```

**Autor implementa y responde:**

```markdown
Implementado con `util.promisify` en commit def456!
Mucho más limpio, gracias por la sugerencia.
```

**Revisor marca como resuelto:**

```markdown
✅ Excelente! Se ve mucho mejor ahora.
```

---

## Resumen

### Conversaciones

- **Úsalas** cuando se requiere acción o cambio
- **Requieren resolución** antes del merge (si la regla está activa)
- **Mejor calidad** de código y menos bugs

### Checklists

- **Template consistente** para todos los PRs
- **Visibilidad** de qué falta completar
- **Estandarización** del proceso de revisión

### Comandos Clave

```bash
# Ver conversaciones
gh pr view 456 --comments

# Agregar comentario
gh pr comment 456 --body "mensaje"

# Ver estado de PR
gh pr view 456
```

### Mejores Prácticas

1. **Revisores:** Sé específico, constructivo y claro
2. **Autores:** Responde antes de resolver conversaciones
3. **Equipo:** Usa templates y convenciones consistentes

---

## Recursos Adicionales

- 📖 [Guía de Flujo de PRs](PR_REVIEW_WORKFLOW_GUIDE.md)
- 📖 [Guía de Mensajes de Commit](COMMIT_GUIDE.md)
- 🔗 [GitHub Docs: Pull Request Reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests)
- 🔗 [GitHub Docs: Protected Branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)

---

**¡Usa conversaciones y checklists para mejorar la calidad y colaboración de tu equipo!**