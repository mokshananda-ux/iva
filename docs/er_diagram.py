"""Genera el diagrama Entidad-Relación del IVA como PNG (matplotlib)."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

DOMAIN_COLORS = {
    "accounts": "#E8F0FE",
    "academy": "#E6F4EA",
    "assessments": "#FEF7E0",
    "certificates": "#F3E8FD",
    "commerce": "#FCE8E6",
    "publishing": "#E0F7FA",
    "library": "#F1F3F4",
}
EDGE = "#5f6368"

# entidad: (x, y, w, h, dominio, [atributos], PK/clave)
ENT = {
    "User": (0.5, 10.6, 2.6, 1.5, "accounts",
             ["PK id", "email (unique)", "is_instructor", "is_staff"]),
    "Profile": (0.5, 8.9, 2.6, 1.1, "accounts",
                ["PK id", "FK user (1:1)", "display_name"]),
    "Course": (4.2, 10.6, 2.7, 1.3, "academy",
               ["PK id", "slug", "title", "price_mxn"]),
    "CourseModule": (4.2, 8.9, 2.7, 1.1, "academy",
                     ["PK id", "FK course", "order"]),
    "Lesson": (4.2, 7.3, 2.7, 1.2, "academy",
               ["PK id", "FK module", "is_sample"]),
    "LessonResource": (4.2, 5.6, 2.7, 1.3, "academy",
                       ["PK id", "FK lesson", "kind", "is_mandatory"]),
    "Enrollment": (8.1, 10.4, 2.9, 1.6, "academy",
                   ["PK id", "FK user", "FK course", "FK order", "status"]),
    "LessonProgress": (8.1, 8.4, 2.9, 1.5, "academy",
                       ["PK id", "FK enrollment", "FK lesson", "completed_at"]),
    "Quiz": (4.2, 3.9, 2.7, 1.2, "assessments",
             ["PK id", "FK lesson", "pass_score"]),
    "Question": (4.2, 2.3, 2.7, 1.0, "assessments",
                 ["PK id", "FK quiz", "text"]),
    "AnswerOption": (4.2, 0.8, 2.7, 1.0, "assessments",
                     ["PK id", "FK question", "is_correct"]),
    "QuizAttempt": (0.5, 2.3, 2.7, 1.3, "assessments",
                    ["PK id", "FK quiz", "FK user", "score", "passed"]),
    "Certificate": (12.1, 10.4, 2.9, 1.6, "certificates",
                    ["PK id", "FK enrollment (1:1)", "public_id (uuid)", "admin_hold"]),
    "Order": (8.1, 5.9, 2.9, 1.6, "commerce",
              ["PK id", "FK user", "status", "total_mxn", "stripe_session_id"]),
    "OrderItem": (12.1, 5.9, 2.9, 1.5, "commerce",
                  ["PK id", "FK order", "FK course?", "FK product?"]),
    "Payment": (8.1, 3.9, 2.9, 1.3, "commerce",
                ["PK id", "FK order", "stripe_payment_intent", "succeeded"]),
    "Refund": (8.1, 2.3, 2.9, 1.0, "commerce",
               ["PK id", "FK payment", "amount_mxn"]),
    "Cart": (12.1, 3.9, 2.9, 1.0, "commerce",
             ["PK id", "FK user", "is_open"]),
    "Product": (12.1, 2.3, 2.9, 1.2, "publishing",
                ["PK id", "slug", "available_format", "price_mxn"]),
    "DigitalBook": (12.1, 0.7, 1.4, 1.1, "publishing",
                    ["PK id", "FK product", "download_limit"]),
    "PhysicalBook": (13.6, 0.7, 1.4, 1.1, "publishing",
                     ["PK id", "FK product", "stock"]),
    "Collection": (0.5, 5.9, 2.7, 1.0, "library",
                   ["PK id", "slug", "title"]),
    "Document": (0.5, 4.2, 2.7, 1.3, "library",
                 ["PK id", "FK collection", "access_level", "protected_path"]),
    "DownloadLog": (0.5, 0.8, 2.7, 1.1, "library",
                    ["PK id", "FK user", "FK document"]),
}

# (origen, destino, cardinalidad)
REL = [
    ("User", "Profile", "1:1"),
    ("Course", "CourseModule", "1:N"),
    ("CourseModule", "Lesson", "1:N"),
    ("Lesson", "LessonResource", "1:N"),
    ("User", "Enrollment", "1:N"),
    ("Course", "Enrollment", "1:N"),
    ("Enrollment", "LessonProgress", "1:N"),
    ("Lesson", "LessonProgress", "1:N"),
    ("Enrollment", "Certificate", "1:1"),
    ("Order", "Enrollment", "1:N"),
    ("Lesson", "Quiz", "1:N"),
    ("Quiz", "Question", "1:N"),
    ("Question", "AnswerOption", "1:N"),
    ("Quiz", "QuizAttempt", "1:N"),
    ("User", "QuizAttempt", "1:N"),
    ("User", "Order", "1:N"),
    ("Order", "OrderItem", "1:N"),
    ("Order", "Payment", "1:N"),
    ("Payment", "Refund", "1:N"),
    ("User", "Cart", "1:N"),
    ("Product", "OrderItem", "1:N"),
    ("Product", "DigitalBook", "1:1"),
    ("Product", "PhysicalBook", "1:1"),
    ("Collection", "Document", "1:N"),
    ("Document", "DownloadLog", "1:N"),
    ("User", "DownloadLog", "1:N"),
]


def center(name):
    x, y, w, h = ENT[name][:4]
    return (x + w / 2, y + h / 2)


def border_point(name, tx, ty):
    """Punto en el borde de la caja `name` en dirección al punto (tx,ty)."""
    x, y, w, h = ENT[name][:4]
    cx, cy = x + w / 2, y + h / 2
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    sx = (w / 2) / abs(dx) if dx else float("inf")
    sy = (h / 2) / abs(dy) if dy else float("inf")
    s = min(sx, sy)
    return cx + dx * s, cy + dy * s


fig, ax = plt.subplots(figsize=(19, 13))
ax.set_xlim(0, 15.2)
ax.set_ylim(0, 12.6)
ax.axis("off")
ax.set_title("Instituto Vak Advaita — Diagrama Entidad-Relación",
             fontsize=18, fontweight="bold", pad=14)

# Relaciones primero (debajo de las cajas).
for a, b, card in REL:
    ca, cb = center(a), center(b)
    xa, ya = border_point(a, *cb)
    xb, yb = border_point(b, *ca)
    ax.annotate("", xy=(xb, yb), xytext=(xa, ya),
                arrowprops=dict(arrowstyle="-", color=EDGE, lw=1.0, alpha=0.45))
    mx, my = (xa + xb) / 2, (ya + yb) / 2
    ax.text(mx, my, card, fontsize=7.5, color="#c0392b",
            ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))

# Cajas de entidad.
for name, (x, y, w, h, dom, attrs) in ENT.items():
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
        fc=DOMAIN_COLORS[dom], ec="#3c4043", lw=1.3, zorder=3))
    ax.text(x + w / 2, y + h - 0.22, name, fontsize=10, fontweight="bold",
            ha="center", va="center", zorder=4)
    ax.plot([x + 0.1, x + w - 0.1], [y + h - 0.42, y + h - 0.42],
            color="#3c4043", lw=0.7, zorder=4)
    for i, attr in enumerate(attrs):
        ax.text(x + 0.12, y + h - 0.62 - i * 0.24, attr, fontsize=7.3,
                ha="left", va="center", zorder=4)

# Leyenda de dominios.
legend_x = 0.3
for i, (dom, color) in enumerate(DOMAIN_COLORS.items()):
    lx = legend_x + i * 2.1
    ax.add_patch(FancyBboxPatch((lx, 12.05), 0.3, 0.3,
                 boxstyle="round,pad=0.02", fc=color, ec="#3c4043", lw=0.8))
    ax.text(lx + 0.4, 12.2, dom, fontsize=8, va="center")

plt.tight_layout()
out = __file__.replace("er_diagram.py", "er_diagram.png")
plt.savefig(out, dpi=140, bbox_inches="tight")
print("guardado:", out)
