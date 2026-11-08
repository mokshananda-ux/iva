# 1. Revisión crítica del documento de arquitectura (v0.3)

> Rol: instructor de Ingeniería de Software. Lectura crítica del documento del
> Instituto Vak Advaita (IVA), con fortalezas, riesgos y mejoras concretas.

## 1.1. Valoración general

El documento está por encima de la media de un proyecto estudiantil: hay un
criterio arquitectónico claro (monolito modular), una pila coherente y, sobre
todo, dos decisiones acertadas que muchos equipos senior pasan por alto:

1. **Usuario personalizado desde el inicio.** Cambiar el modelo `User` después
   de la primera migración en Django es caro y arriesgado. Empezar con uno
   propio es la decisión correcta.
2. **Activación de matrícula por webhook, idempotente.** Es exactamente el
   patrón que exige una pasarela de pago seria. No activar por el retorno a la
   página de éxito es una regla que evita fraude y matrículas fantasma.

El resto de la revisión asume que el proyecto es real y debe sobrevivir al
crecimiento, no solo aprobar una entrega.

## 1.2. Fortalezas

- **Separación `publishing` / `commerce`.** Distinguir "qué se vende" (catálogo)
  de "cómo se cobra" (transacciones) es una frontera de dominio limpia.
- **"Inscrito" como estado calculado, no como rol.** Modelar la inscripción a
  partir de las matrículas activas, y no como un flag persistente, evita
  inconsistencias (usuarios "inscritos" sin pago válido). Excelente.
- **Autorización en el servidor y descargas verificadas.** La interfaz no es la
  frontera de seguridad. Bien planteado.
- **Instalación diferida de dependencias** (Celery, Redis, DRF). Evita cargar el
  proyecto con infraestructura sin necesidad real. Buen juicio de YAGNI.
- **i18n y Unicode desde el inicio** (gettext, UTF-8, PostgreSQL). Imprescindible
  en un proyecto con sánscrito, IAST y devanāgarī.

## 1.3. Riesgos y debilidades (con mejora propuesta)

### a) El modelo de "lección completada" está declarado en prosa, no en reglas
El texto describe cuándo se completa una lección (vídeo obligatorio, quiz con
nota mínima, labs verificados). Esto debe vivir en **un único lugar del
código**, no repartido en vistas o plantillas.

> **Mejora:** encapsular la regla en un servicio/propiedad (`LessonProgress.
> is_complete` y `academy.services`). Así se prueba con un test unitario y no se
> duplica. Ya implementado en el repositorio entregado.

### b) "Labs se verifican", pero no se define qué es un Lab
Es el punto más ambiguo del documento. ¿Un lab es un ejercicio autoevaluado, una
entrega revisada por un instructor, un cuaderno interactivo? El criterio de
certificación depende de ello.

> **Mejora:** definir el `Lab` como una entidad propia con estados
> (`pendiente`, `enviado`, `verificado`, `rechazado`) y responsable de la
> verificación (automática o docente). Hasta definirlo, el flag `lab_verified`
> es un marcador provisional.

### c) Precios y moneda: decimal, no float, y multi-moneda desde el modelo
Mezclar cobros nacionales (MXN, OXXO) e internacionales abre un problema de
moneda. El documento lo menciona pero no lo modela.

> **Mejora:** usar siempre `DecimalField` para dinero (nunca `float`), guardar
> la **moneda** junto al importe en la orden, y registrar el importe tal y como
> lo confirmó Stripe (no recalcular a posteriori). Considerar almacenar montos
> en la unidad menor (centavos) para evitar errores de redondeo.

### d) Idempotencia: bien el principio, falta el mecanismo
El documento dice "procesar eventos de forma idempotente" pero no dice cómo.

> **Mejora:** tabla de eventos procesados con `event_id` único de Stripe (ver
> `commerce.ProcessedWebhookEvent`) + transacción atómica + `select_for_update`
> sobre la orden. Implementado en el repositorio.

### e) Protección de PDF: expectativas realistas
El propio documento ya lo reconoce ("objetivo realista... disuadir"). Conviene
subrayarlo: marca de agua + endpoint autenticado + registro **disuaden y
auditan**, pero no impiden la copia de un usuario legítimo. No vendas DRM fuerte
que no vas a tener.

> **Mejora:** marca de agua personalizada por usuario (email/ID) en el PDF
> servido, URLs firmadas de corta duración y cuota por usuario. Aceptar que el
> objetivo es trazabilidad, no imposibilidad.

### f) `OrderItem` polimórfico (curso vs. producto)
Una orden puede contener cursos y libros. Modelarlo con dos FKs opcionales
(`course`, `product`) es pragmático pero frágil (hay que validar que exactamente
una esté presente).

> **Mejora:** añadir un `CheckConstraint` que garantice exactamente un objetivo
> según `item_type`, o migrar a `GenericForeignKey` si crecen los tipos
> vendibles. Documentado como decisión consciente.

### g) Borrado de datos con historial contable
Matrículas, órdenes y pagos no deben desaparecer por un `CASCADE` accidental.

> **Mejora:** `on_delete=PROTECT` en relaciones con valor contable/legal
> (`Order.user`, `Enrollment.course`, `Certificate.enrollment`) y borrado lógico
> (estado `cancelled`) en vez de físico. Aplicado en los modelos.

### h) Faltan apps en la tabla de responsabilidades
El árbol de carpetas incluye `resources`, `tools` y `forums`, pero algunas no
aparecían con la misma claridad en el diseño de dominio. Se han incluido con una
responsabilidad mínima y explícita para que el mapa carpeta-dominio sea 1:1.

### i) Observabilidad y operación, ausentes
No hay mención de logging estructurado, métricas, trazas, copias de seguridad ni
estrategia de migraciones de datos.

> **Mejora:** definir desde pronto logging estructurado, healthcheck, backups
> de PostgreSQL y un plan de migraciones. No es sobre-ingeniería; es lo mínimo
> para producción.

### j) Pruebas: declaradas, pero sin estrategia
Se menciona Pytest, pero no qué se prueba. En este dominio, lo crítico es:
reglas de completitud de lección, emisión de certificado, idempotencia del
webhook y matriz de permisos.

> **Mejora:** priorizar tests de esas cuatro reglas (el repositorio incluye un
> punto de partida en `tests/test_domain.py`).

## 1.4. Preguntas abiertas que el equipo debería cerrar

1. ¿Qué es exactamente un "Lab" y quién lo verifica?
2. ¿Se permiten reembolsos de cursos ya iniciados? ¿Qué pasa con la matrícula?
3. ¿Un mismo usuario puede recomprar un curso (nueva matrícula) tras cancelar?
4. ¿Los certificados caducan o se revocan? (el campo de bloqueo administrativo
   lo permite, pero falta la política).
5. ¿Qué idiomas son de interfaz y cuáles de contenido académico? (sánscrito es
   contenido, no idioma de UI).

## 1.5. Veredicto

Arquitectura sólida para la fase actual. Las mejoras no cambian el enfoque:
refuerzan reglas de negocio en código (no en prosa), blindan el dinero y los
datos contables, y cierran ambigüedades (Labs, reembolsos, caducidad). El
monolito modular es la decisión adecuada; no introduzcas microservicios hasta
que exista una razón de escala o de equipo que lo justifique.
