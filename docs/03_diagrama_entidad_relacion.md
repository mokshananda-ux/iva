# 3. Diagrama Entidad-Relación — IVA

Imagen renderizada: `er_diagram.png` (en esta misma carpeta).  
Abajo, la fuente autoritativa en Mermaid (`erDiagram`), que se puede editar y
volver a renderizar.

## 3.1. Cardinalidades resumidas

- Un `Course` tiene muchos `CourseModule`; un módulo, muchas `Lesson`.
- Una `Lesson` tiene muchos `LessonResource` (vídeo, PDF, quiz, lab, foro).
- Un `User` tiene muchas `Enrollment`; cada `Enrollment` es de un `Course` y se
  liga a la `Order` que verificó su pago.
- Cada `Enrollment` tiene su propio `LessonProgress` por lección.
- Un `Certificate` pertenece a una `Enrollment` concreta (1:1), con `public_id`.
- `Order` → muchos `OrderItem`; `Order` → muchos `Payment`; `Payment` → `Refund`.
- `Product` se especializa en `DigitalBook` o `PhysicalBook` (1:1).
- `Collection` → muchos `Document`; cada descarga queda en `DownloadLog`.

## 3.2. Mermaid (erDiagram)

```mermaid
erDiagram
    USER ||--o| PROFILE : tiene
    USER ||--o{ ENROLLMENT : posee
    USER ||--o{ ORDER : realiza
    USER ||--o{ CART : tiene
    USER ||--o{ QUIZATTEMPT : intenta
    USER ||--o{ DOWNLOADLOG : genera

    COURSE ||--o{ COURSEMODULE : contiene
    COURSEMODULE ||--o{ LESSON : contiene
    LESSON ||--o{ LESSONRESOURCE : incluye
    LESSON ||--o{ QUIZ : evalua_con
    LESSON ||--o{ THREAD : discute_en

    COURSE ||--o{ ENROLLMENT : recibe
    ENROLLMENT ||--o{ LESSONPROGRESS : registra
    LESSON ||--o{ LESSONPROGRESS : medido_en
    ENROLLMENT ||--o| CERTIFICATE : emite
    ORDER ||--o{ ENROLLMENT : activa

    QUIZ ||--o{ QUESTION : tiene
    QUESTION ||--o{ ANSWEROPTION : ofrece
    QUIZ ||--o{ QUIZATTEMPT : recibe

    ORDER ||--o{ ORDERITEM : contiene
    ORDER ||--o{ PAYMENT : cobra_con
    PAYMENT ||--o{ REFUND : reembolsa
    ORDER ||--o| SHIPPINGDETAIL : envia_con
    PRODUCT ||--o{ ORDERITEM : vendido_en
    COURSE ||--o{ ORDERITEM : vendido_en

    PRODUCT ||--o| DIGITALBOOK : es
    PRODUCT ||--o| PHYSICALBOOK : es

    COLLECTION ||--o{ DOCUMENT : agrupa
    DOCUMENT ||--o{ DOWNLOADLOG : descargado_en

    USER {
        bigint id PK
        string email UK
        bool is_instructor
        bool is_staff
    }
    ENROLLMENT {
        bigint id PK
        bigint user_id FK
        bigint course_id FK
        bigint order_id FK
        string status
        datetime activated_at
    }
    LESSONPROGRESS {
        bigint id PK
        bigint enrollment_id FK
        bigint lesson_id FK
        bool video_watched
        bool quiz_passed
        bool lab_verified
        datetime completed_at
    }
    CERTIFICATE {
        bigint id PK
        bigint enrollment_id FK
        uuid public_id UK
        bool administrative_hold
    }
    ORDER {
        bigint id PK
        bigint user_id FK
        string status
        string currency
        decimal total_mxn
        string stripe_session_id
    }
    PRODUCT {
        bigint id PK
        string slug UK
        string available_format
        decimal price_mxn
    }
    DOCUMENT {
        bigint id PK
        bigint collection_id FK
        string access_level
        string protected_path
        int download_limit
    }
```

> Notación: `||--o{` = uno-a-muchos, `||--o|` = uno-a-uno/opcional,
> `PK` = clave primaria, `FK` = clave foránea, `UK` = única.
