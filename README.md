**Instituto Vak Advaita (IVA)**  
   
    
   
     Plataforma educativa: monolito modular con Django. Núcleo común + apps de    dominio independientes, desplegadas como una sola aplicación.  
   
    
   
     
   
     **Requisitos**  
   
 Python 3.12+  
   
 PostgreSQL 16 (o SQLite para arranque rápido en desarrollo)  
   
 Docker (opcional, recomendado)  
   
    
   
     
   
    
   
     **Arranque rápido (sin Docker)**  
   
    
   
     
   
    
   
     **Debian 13**  
   
    
   
    
   
     sudo apt update  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
     sudo apt install python3 python3-venv python3-pip build-essential libpq-dev python3-dev  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
     # Crear el entorno virtual llamado 'env'  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
     python3 -m venv env  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
     # Activar el entorno virtual  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
     source env/bin/activate  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        
```  
 pip install -r requirements/development.txt            
      cp .env.example .env            # edita los valores            
      export USE_SQLITE=1             # opcional, evita montar PostgreSQL            
      python manage.py makemigrations            
      python manage.py migrate            
      python manage.py createsuperuser            
      python manage.py runserver            
                  
               
            
         
      
   
```  
**Arranque con Docker**  
```  
docker compose up --build            
      # en otra terminal:            
      docker compose exec web python manage.py migrate            
      docker compose exec web python manage.py createsuperuser            
               
            
         
      
   
```  
Dentro de Docker, Django se conecta a `db:5432`; el puerto `5434` solo publica  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
     PostgreSQL en `127.0.0.1:5434` para conexiones desde el equipo anfitrión.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
     **Estructura**  
   
 `config/` configuración dividida (`base`, `development`, `production`).  
   
 `apps/` una app por dominio funcional.  
   
 `templates/`, `static/`, `media/`.  
   
 `requirements/` dependencias por entorno.  
   
 `tests/` pruebas de reglas de negocio.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
     **Decisiones de diseño relevantes**  
   
 **Usuario personalizado** (`accounts.User`) basado en email desde el inicio.  
   
 **"Inscrito" se calcula** a partir de matrículas activas (`User.is_enrolled`),  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
      no es un rol persistente.  
   
 **Autorización siempre en servidor** (`apps/core/permissions.py`).  
   
 **Descargas protegidas** por endpoint con control de permisos y registro.  
   
 **Stripe**: la matrícula se activa SOLO tras verificar el webhook  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
      `checkout.session.completed`, de forma **idempotente**  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
      (`commerce.ProcessedWebhookEvent`). Nunca por el retorno a la página de éxito.  
   
 **i18n** con `gettext`, UTF-8 y almacenamiento Unicode en PostgreSQL;  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
      transliterador devanāgarī -> IAST en `apps/tools/transliteration.py`.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
     **Pruebas**  
```  
pytest            
                  
               
            
         
      
   
```  
*Las migraciones no se incluyen versionadas en este esqueleto; se generan con*  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
      *`python manage.py makemigrations` en el primer arranque.*  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    *python manage.py makemessages -l es*  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    *python manage.py makemessages -l sa*  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    *python manage.py makemessages -l ca*  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    *python manage.py makemessages -l pt*  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
   **ollama pull translategemma:12b**  
   
    
   
  **pip install ollama**  
   
    
   
     
   
    
   
  **import ollama**  
   
    
   
     
   
    
   
  **def traducir(texto):**  
   
    
   
     
   
    
   
      **prompt = f"""You are a professional Spanish (es) to Catalan (ca) translator.**  
   
    
   
  **Your goal is to accurately convey the meaning and nuances of the original Spanish text.**  
   
    
   
     
   
    
   
  **Produce only the Catalan translation, without explanations.**  
   
    
   
     
   
    
   
  **Please translate the following Spanish text into Catalan:**  
   
    
   
     
   
    
   
     
   
    
   
  **{texto}**  
   
    
   
  **"""**  
   
    
   
     
   
    
   
      **response = ollama.chat(**  
   
    
   
          **model="translategemma:12b",**  
   
    
   
          **messages=\[**  
   
    
   
              **{**  
   
    
   
                  **"role": "user",**  
   
    
   
                  **"content": prompt**  
   
    
   
              **}**  
   
    
   
          **\],**  
   
    
   
          **options={**  
   
    
   
              **"temperature": 0**  
   
    
   
          **}**  
   
    
   
      **)**  
   
    
   
     
   
    
   
      **return response\["message"\]\["content"\].strip()**    
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
      
   
     
   
    
   
     
   
    
   
    La idea fundamental es esta: el código se escribe una sola vez y Django selecciona las traducciones según el idioma activo del visitante.  
   
    
   
   **1. Cómo funciona \_() en Django**  
   
    
   
     
   
    
   
   Lo que has escrito es correcto:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    python  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    raise ValueError(\_("El email es obligatorio"))  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Y también:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    python  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    verbose_name = \_("usuario")  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    verbose_name_plural = \_("usuarios")  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    La función \_() es una abreviatura de gettext_lazy o gettext, según cómo la importes.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    En modelos, formularios y campos es preferible utilizar gettext_lazy, porque Django puede necesitar el texto antes de conocer el idioma definitivo del usuario.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Por ejemplo, al principio de tu archivo:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    python  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    from django.utils.translation import gettext_lazy as \_  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Así puedes escribir:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    python  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    class UserProfile(models.Model):  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        preferred_language = models.CharField(  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
            \_("idioma preferido"),  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
            max_length=5,  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
            default="es",  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        )  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        class Meta:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
            verbose_name = \_("usuario")  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
            verbose_name_plural = \_("usuarios")  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Y en tus validaciones:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    python  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    from django.utils.translation import gettext as \_  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    def validate_email(email):  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        if not email:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
            raise ValueError(\_("El email es obligatorio"))  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Una distinción importante:  
   
 gettext_lazy as \_: para modelos, campos, formularios y metadatos.  
   
 gettext as \_: para textos que se traducen en el momento de ejecutarse, como determinadas validaciones y funciones.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    No necesitas traducir manualmente el texto en Python.  
   
    
   
   **2. Configurar los idiomas desde settings.py**  
   
    
   
     
   
    
   
   En tu archivo settings.py, configura lo siguiente:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    python  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    from pathlib import Path  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    from django.utils.translation import gettext_lazy as \_  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    LANGUAGE_CODE = "es"  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    LANGUAGES = \[  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        ("es", \_("Español")),  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        ("sa", \_("Sánscrito")),  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        ("ca", \_("Catalán")),  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        ("pt", \_("Portugués")),  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    \]  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    USE_I18N = True  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    LOCALE_PATHS = \[  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        BASE_DIR / "locale",  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    \]  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Aquí BASE_DIR normalmente ya está definido en tu archivo.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Si quieres portugués brasileño, utiliza pt-br en lugar de pt.  
   
    
   
   **Activar el middleware**  
   
    
   
     
   
    
   
   En MIDDLEWARE, asegúrate de tener:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    python  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    MIDDLEWARE = \[  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        "django.middleware.security.SecurityMiddleware",  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        "django.contrib.sessions.middleware.SessionMiddleware",  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        "django.middleware.locale.LocaleMiddleware",  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        "django.middleware.common.CommonMiddleware",  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        # El resto de tus middlewares...  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    \]  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    El orden importa: LocaleMiddleware debe ir después de SessionMiddleware y antes de CommonMiddleware.  
   
    
   
     
   
    
   
     
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Django puede recorrer tu proyecto y localizar automáticamente todas las cadenas que hayas marcado con \_().  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Desde la terminal, en la carpeta donde está manage.py, ejecuta:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    bash  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
   python manage.py makemessages -l es \\  
   
    
   
     
   
    
   
       --ignore=env/\*  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
   python manage.py makemessages -l ca \\  
   
    
   
     
   
    
   
       --ignore=env/\* \\  
   
    
   
     
   
    
   
       --ignore=.venv/\* \\  
   
    
   
     
   
    
   
       --ignore=static/\* \\  
   
    
   
     
   
    
   
       --ignore=media/\*  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
   pip install polib deep-translator  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
   python manage.py makemessages -l es python manage.py makemessages -l sa python manage.py makemessages -l ca python manage.py makemessages -l pt  
   
    
   
     
   
    
   
      
   
    
   
      
   
    
   
     
   
    
   
    Una vez completadas las traducciones, ejecutas:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    bash  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
   python manage.py compilemessages  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    ¡Y listo! Django generará los archivos .mo, que son los que utiliza para servir las traducciones.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Cada vez que añadas textos nuevos, repetirás makemessages y compilemessages.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Django  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    +1  
   
    
   
   **4. ¿Y cómo se traducen los textos de HTML?**  
   
    
   
     
   
    
   
   También puedes hacerlo directamente en tus plantillas.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Por ejemplo, en login.html:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    HTML  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Ajustar líneasCopiar códigoVista previa  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    {% load i18n %}  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    \<h1>{% trans "Iniciar sesión" %}\</h1>  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    \<label>{% trans "Correo electrónico" %}\</label>  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    \<button>{% trans "Entrar" %}\</button>  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Para textos más largos:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    HTML  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Ajustar líneasCopiar códigoVista previa  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    {% blocktrans %}  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Bienvenido a nuestra plataforma.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Esperamos que disfrutes de tu experiencia.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    {% endblocktrans %}  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Django también los detectará al ejecutar makemessages.  
   
    
   
   **5. Tu campo preferred_language: cómo hacerlo funcionar realmente**  
   
    
   
     
   
    
   
   Esta parte merece especial atención porque hay una pequeña diferencia entre guardar el idioma y activar el idioma.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Tu código:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    python  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    preferred_language = models.CharField(  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        \_("idioma preferido"),  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        max_length=5,  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        default="es",  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    )  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Es perfectamente válido.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Pero hay algo importante: este campo solamente guarda la preferencia del usuario en la base de datos. No cambia automáticamente el idioma de la página.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Para que funcione necesitas conectar tres elementos:  
   
 El campo preferred_language guarda la elección.  
   
 Django recupera esa elección cuando el usuario inicia sesión.  
   
 Django activa ese idioma para las respuestas que recibe el usuario.  
   
    
   
   **A. Guardar el idioma elegido**  
   
    
   
     
   
    
   
   Por ejemplo, si un usuario selecciona catalán:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    python  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    user.preferred_language = "ca"  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    user.save()  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    En la base de datos quedará almacenado:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    text  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    preferred_language = ca  
   
    
   
   **B. Activar el idioma del usuario**  
   
    
   
     
   
    
   
   Django dispone de esta función:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    python  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    from django.utils import translation  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    translation.activate("ca")  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Pero no queremos escribirla manualmente en todas las vistas.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Lo ideal es implementar un middleware propio que consulte el idioma preferido del usuario autenticado.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Por ejemplo:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    python  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    from django.utils import translation  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    class UserLanguageMiddleware:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        def \_\_init\_\_(self, get_response):  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
            self.get_response = get_response  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        def \_\_call\_\_(self, request):  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
            if request.user.is_authenticated:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
                language = request.user.preferred_language  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
                if language:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
                    with translation.override(language):  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
                        response = self.get_response(request)  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
                    return response  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
            return self.get_response(request)  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Este middleware activa el idioma guardado para cada petición del usuario.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Importante: este ejemplo presupone que tu modelo de usuario tiene el campo preferred_language. Si utilizas un modelo de perfil separado, habrá que acceder a través de la relación correspondiente.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Colócalo después de AuthenticationMiddleware en MIDDLEWARE, para que request.user ya esté disponible.  
   
    
   
   **C. Crear un selector de idiomas**  
   
    
   
     
   
    
   
   En tu plantilla puedes tener algo así:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    HTML  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Ajustar líneasCopiar códigoVista previa  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    \<form action="{% url 'set_language' %}" method="post">  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        {% csrf_token %}  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        \<select name="language">  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
            \<option value="es">Español\</option>  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
            \<option value="sa">Sánscrito\</option>  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
            \<option value="ca">Català\</option>  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
            \<option value="pt">Português\</option>  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        \</select>  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        \<button type="submit">Cambiar idioma\</button>  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    \</form>  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Django proporciona una vista set_language para gestionar los cambios de idioma. Puedes conectarla en tu urls.py:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    python  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    from django.urls import path, include  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    urlpatterns = \[  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        path("i18n/", include("django.conf.urls.i18n")),  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    \]  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Esta vista utiliza la sesión o la cookie para recordar el idioma. Si quieres que además se conserve en preferred_language, tendrás que guardar esa elección en tu modelo cuando el usuario cambie el idioma.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Django  
   
    
   
   **6. Una recomendación adicional: traducir también las URL**  
   
    
   
     
   
    
   
   Si vas a desarrollar una web multilingüe desde el principio, puedes hacer que las direcciones tengan prefijos:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    text  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    tusitio.com/es/ tusitio.com/sa/ tusitio.com/ca/ tusitio.com/pt/  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Django permite hacerlo con i18n_patterns.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Por ejemplo:  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    python  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    from django.conf.urls.i18n import i18n_patterns  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    from django.urls import path  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
       
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    urlpatterns = i18n_patterns(  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
        path("", home, name="home"),  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    )  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Esto también ayuda a organizar el posicionamiento SEO de las diferentes versiones lingüísticas.  
   
    
   
   **7. Mi propuesta de organización para tu proyecto**  
   
    
   
   **Arquitectura multilingüe**  
   
    
   
     
   
    
   
   Código Python y Django  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Todos los textos marcados con gettext_lazy, gettext y las etiquetas de traducción de plantillas.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Sistema gettext  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Extracción y gestión de traducciones  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    es  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Español  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    sa  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Sánscrito  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    ca  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Catalán  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    pt  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Portugués  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Base de datos  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    preferred_language por usuario  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Web presentada en el idioma seleccionado  
   
    
   
   **8. Una cuestión importante antes de avanzar**  
   
    
   
     
   
    
   
   Hay una decisión de arquitectura que me gustaría aclarar contigo.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Django permite utilizar español como idioma original de los textos, pero su sistema gettext está pensado originalmente para proyectos cuyo idioma fuente es inglés. No impide utilizar español, aunque conviene tenerlo presente para organizar correctamente los catálogos y sus traducciones.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Te propongo mantener el español como idioma de escritura del código y utilizar los otros tres idiomas como traducciones independientes.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    ¿Qué versión de Django estás utilizando actualmente?  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    Te lo pregunto porque me gustaría prepararte una estructura completa y compatible con tu versión, incluyendo settings.py, middleware.py, models.py, urls.py y el selector de idiomas, para que la internacionalización quede resuelta desde los cimientos del proyecto.  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
   
   
    
   
    
   
¡Excelente! Ahora sí tenemos información suficiente para trabajar sobre tu proyecto real. Y hay buenas noticias: tu entorno está preparado para instalar Tailwind CSS 4 sin modificar la arquitectura Django que ya construiste.  
He revisado tu estructura y quiero destacar algo: tu proyecto ya tiene una organización bastante sólida. Estás utilizando un monolito modular con las aplicaciones dentro de apps/, configuración Django separada por entornos y plantillas centralizadas.  
No vamos a cambiar esa arquitectura.  
## **1. Diagnóstico de tu proyecto**  
Entorno de desarrollo  
Verificado  
  
|  |  |  
| - | - |  
| **Componente** |  **Tu entorno** |  
| Sistema operativo |  Linux (Ubuntu/Debian probable) |  
| Python |  3.13.5 |  
| Node.js |  24.22.2 |  
| npm |  11.19.1 |  
| Entorno virtual |  env/ |  
| Tailwind |  No instalado |  
| Django |  Configuración modular |  
  
Estructura frontend existente  
text  
templates/ ├── base.html ├── institutional/ │   └── home.html ├── academy/ ├── accounts/ └── partials/  static/ ├── css/ │   └── app.css └── js/  
No necesitamos reorganizarla  
Una observación: tree /F es una opción de Windows. En Linux utilizaremos tree -L 3, como hiciste correctamente después.  
## **2. Decisión de arquitectura para Tailwind**  
Vamos a conservar tu estructura y añadir solamente una carpeta assets/.  
La estructura resultante será:  
text  
iva/ │ ├── apps/ ├── config/ ├── assets/ │   └── css/ │       └── app.css          # Fuente Tailwind │ ├── static/ │   ├── css/ │   │   └── app.css          # CSS compilado │   └── js/ │ ├── templates/ │   ├── base.html │   ├── institutional/ │   ├── academy/ │   ├── accounts/ │   └── partials/ │ ├── manage.py ├── package.json └── package-lock.json  
Una decisión importante: no vamos a poner Node.js dentro de apps/. Tailwind es una herramienta de construcción del frontend, no una aplicación de negocio Django.  
# **3. Instalemos Tailwind CSS 4**  
Tu versión de Node.js es suficiente para esta instalación. La documentación oficial recomienda instalar tailwindcss junto con @tailwindcss/cli.  
   
Tailwind CSS  
+1  
Desde la raíz del proyecto, con tu entorno virtual activado, ejecuta:  
Paso 3.1. Crear la carpeta de recursos fuente  
bash  
mkdir -p assets/css  
Paso 3.2. Crear package.json  
Como todavía no tienes package.json, ejecuta:  
bash  
npm init -y  
Esto crea el archivo de configuración de npm.  
Paso 3.3. Instalar Tailwind  
bash  
npm install -D tailwindcss @tailwindcss/cli  
Espera a que finalice la instalación.  
Comprueba las versiones:  
bash  
npm list tailwindcss @tailwindcss/cli  
Deberías encontrar ambos paquetes instalados en la rama 4.x.  
# **4. Crear nuestro archivo fuente CSS**  
Antes de modificar el archivo que ya tienes en static/css/app.css, vamos a conservar una copia:  
bash  
cp static/css/app.css static/css/app.css.backup  
Ahora crea el archivo:  
bash  
nano assets/css/app.css  
Introduce este contenido:  
css  
@import "tailwindcss";  
   
/\*  
\========================================  
INSTITUTO VAK ADVAITA  
Sistema de diseño institucional  
\========================================  
\*/  
   
/\* Detección de plantillas Django \*/  
@source "../../templates";  
   
/\* Identidad visual \*/  
@theme {  
    --color-iva-brown: #59452F;  
    --color-iva-ochre: #745B3C;  
    --color-iva-ivory: #F5F0E6;  
    --color-iva-charcoal: #292722;  
}  
   
/\* Estilos globales \*/  
@layer base {  
    html {  
        scroll-behavior: smooth;  
    }  
   
    body {  
        font-family: Arial, Helvetica, sans-serif;  
    }  
}  
Guarda con Ctrl + O, pulsa Enter y sal con Ctrl + X.  
Hemos creado cuatro colores institucionales que podremos utilizar así:  
HTML  
Ajustar líneasCopiar códigoVista previa  
\<div class="bg-iva-brown text-white">  
    Instituto Vak Advaita  
\</div>  
# **5. Configurar los comandos de compilación**  
Vamos a utilizar npm pkg set para añadir los comandos sin sobrescribir el resto del archivo package.json.  
Ejecuta:  
bash  
npm pkg set "scripts.dev=npx @tailwindcss/cli -i ./assets/css/app.css -o ./static/css/app.css --watch"  
Y después:  
bash  
npm pkg set "scripts.build=npx @tailwindcss/cli -i ./assets/css/app.css -o ./static/css/app.css --minify"  
Tu package.json tendrá una sección similar a esta:  
json  
{   "scripts": {     "dev": "npx @tailwindcss/cli -i ./assets/css/app.css -o ./static/css/app.css --watch",     "build": "npx @tailwindcss/cli -i ./assets/css/app.css -o ./static/css/app.css --minify"   } }  
No necesitas copiar manualmente ese JSON: los comandos anteriores ya realizan la modificación.  
# **6. Primera compilación**  
Ejecuta:  
bash  
npm run build  
Si todo funciona, Tailwind generará:  
text  
static/css/app.css  
Puedes comprobarlo:  
bash  
ls -lh static/css/app.css  
Resultado esperado  
Tendrás un CSS compilado que contiene las clases utilizadas en tus plantillas Django.  
# **7. Comprobar la configuración de Django**  
Ahora vamos a verificar que Django encuentra correctamente los archivos estáticos.  
Ejecuta:  
bash  
grep -nE 'STATIC_URL|STATICFILES_DIRS|STATIC_ROOT|BASE_DIR' config/settings/base.py  
Quiero comprobar especialmente que tienes una configuración coherente con:  
python  
STATIC_URL = "static/"  
   
STATICFILES_DIRS = \[  
    BASE_DIR / "static",  
\]  
No añadas esta configuración todavía si ya tienes otra definición: primero revisaremos lo que existe.  
# **8. Cómo quedará nuestro flujo de trabajo**  
Una vez comprobada la compilación, trabajaremos con dos terminales:  
Terminal 1 — Tailwind  
Desarrollo continuo  
bash  
npm run dev  
Detecta cambios en las plantillas y recompila los estilos.  
Terminal 2 — Django  
Servidor local  
bash  
source env/bin/activate python manage.py runserver  
Ejecuta nuestra aplicación educativa.  
## **9. Siguiente objetivo: validar el frontend**  
Cuando terminemos esta instalación, vamos a realizar tres comprobaciones:  
1. Que Tailwind detecte las clases de templates/base.html y templates/institutional/home.html.  
2. Que Django sirva correctamente el CSS.  
3. Que la página principal se visualice con los colores y estilos institucionales.  
Después podremos construir componentes reutilizables en templates/partials/ y comenzar con HTMX.  
Tu tarea ahora: ejecuta los pasos 3 a 7 y compárteme:  
- El resultado de npm list tailwindcss @tailwindcss/cli.  
- El resultado de npm run build.  
- El resultado del comando grep de settings/base.py.  
Así revisaremos juntos la instalación antes de avanzar. No quiero que acumulemos errores de configuración sobre una base que todavía no hemos validado.  
¡Excelente! Tenemos nuestra primera compilación exitosa de Tailwind CSS 4.3.5. Ya superamos una parte importante de la configuración del frontend.  
Diagnóstico de instalación  
Correcto  
  
|  |  |  
| - | - |  
| **Elemento** |  **Resultado** |  
| Node.js |  24.22.2 |  
| npm |  11.19.1 |  
| Python |  3.13.5 |  
| Tailwind CSS |  4.3.5 |  
| Compilación |  Exitosa |  
| STATIC_URL |  Configurado |  
| STATIC_ROOT |  Configurado |  
| STATICFILES_DIRS |  Configurado |  
  
## **1. Revisemos tu configuración Django**  
Tu configuración es correcta:  
python  
STATIC_URL = "/static/"  
STATIC_ROOT = BASE_DIR / "staticfiles"  
STATICFILES_DIRS = \[BASE_DIR / "static"\]  
Quiero explicarte algo importante:  
- STATICFILES_DIRS: indica dónde están tus archivos estáticos durante el desarrollo.  
- STATIC_ROOT: indica dónde Django recopilará los archivos cuando ejecutes collectstatic.  
- STATIC_URL: define la URL desde la que se sirven los archivos.  
No necesitamos modificar nada aquí.  
## **2. Una pequeña corrección en tu terminal**  
Ejecutaste:  
bash  
list tailwindcss @tailwindcss/cli  
El comando correcto es:  
bash  
npm list tailwindcss @tailwindcss/cli  
Esto es solamente una consulta de npm para verificar las dependencias.  
## **3. Ahora vamos a comprobar que Tailwind realmente funciona**  
La compilación exitosa es buena señal, pero necesitamos comprobar que está detectando las clases de nuestras plantillas.  
Ejecuta:  
bash  
grep -o 'bg-stone-50' static/css/app.css | head  
Y también:  
bash  
grep -o 'text-4xl' static/css/app.css | head  
Si aparecen esos nombres, tendremos evidencia de que Tailwind está generando las clases utilizadas en nuestros HTML.  
## **4. Iniciemos el modo desarrollo**  
Abre una terminal y ejecuta:  
bash  
npm run dev  
Deberías obtener un mensaje parecido a:  
text  
≈ tailwindcss v4.3.5  Done in ...  
Déjalo funcionando. Este proceso vigilará los cambios en tus archivos.  
Abre otra terminal y ejecuta:  
bash  
source env/bin/activate python manage.py check  
Si Django no encuentra errores, inicia:  
bash  
python manage.py runserver  
Visita:  
[http://127.0.0.1:8000/ ](http://127.0.0.1:8000/?utm_source=chatgpt.com "http://127.0.0.1:8000/?utm_source=chatgpt.com")  
## **5. Una mejora importante para nuestro proyecto**  
Quiero anticipar algo de nuestra arquitectura: actualmente tienes una carpeta templates/partials/, lo cual es perfecto.  
Más adelante utilizaremos esta organización:  
text  
templates/ │ ├── base.html │ ├── partials/ │   ├── navbar.html │   ├── footer.html │   ├── messages.html │   ├── course_card.html │   └── pagination.html │ ├── institutional/ │   └── home.html │ ├── academy/ ├── accounts/ └── library/  
Esto permitirá que HTMX actualice componentes individuales sin tener que reconstruir páginas completas.  
## **6. Nuestro siguiente paso**  
Antes de continuar con el diseño visual, quiero validar tres cosas:  
Comprobación del frontend IVA  
Marca lo que ya hayas comprobado.  
Tailwind genera las clases CSS.  
python manage.py check termina correctamente.  
La página principal se visualiza correctamente.  
Enviar resultados  
Mi siguiente objetivo será construir el sistema de diseño del Instituto Vak Advaita, con tipografía académica, paleta institucional, navegación responsive y tarjetas reutilizables.  
Después incorporaremos nuestro primer componente HTMX real: una interacción entre el catálogo de cursos y Django.  
Vamos muy bien: ya tenemos Tailwind compilando y una arquitectura Django que no necesita ser alterada.  
¡Excelente! Tenemos nuestra primera compilación exitosa de Tailwind CSS 4.3.5. Ya superamos una parte importante de la configuración del frontend.  
Diagnóstico de instalación  
Correcto  
  
|  |  |  
| - | - |  
| **Elemento** |  **Resultado** |  
| Node.js |  24.22.2 |  
| npm |  11.19.1 |  
| Python |  3.13.5 |  
| Tailwind CSS |  4.3.5 |  
| Compilación |  Exitosa |  
| STATIC_URL |  Configurado |  
| STATIC_ROOT |  Configurado |  
| STATICFILES_DIRS |  Configurado |  
  
## **1. Revisemos tu configuración Django**  
Tu configuración es correcta:  
python  
STATIC_URL = "/static/"  
STATIC_ROOT = BASE_DIR / "staticfiles"  
STATICFILES_DIRS = \[BASE_DIR / "static"\]  
Quiero explicarte algo importante:  
- STATICFILES_DIRS: indica dónde están tus archivos estáticos durante el desarrollo.  
- STATIC_ROOT: indica dónde Django recopilará los archivos cuando ejecutes collectstatic.  
- STATIC_URL: define la URL desde la que se sirven los archivos.  
No necesitamos modificar nada aquí.  
## **2. Una pequeña corrección en tu terminal**  
Ejecutaste:  
bash  
list tailwindcss @tailwindcss/cli  
El comando correcto es:  
bash  
npm list tailwindcss @tailwindcss/cli  
Esto es solamente una consulta de npm para verificar las dependencias.  
## **3. Ahora vamos a comprobar que Tailwind realmente funciona**  
La compilación exitosa es buena señal, pero necesitamos comprobar que está detectando las clases de nuestras plantillas.  
Ejecuta:  
bash  
grep -o 'bg-stone-50' static/css/app.css | head  
Y también:  
bash  
grep -o 'text-4xl' static/css/app.css | head  
Si aparecen esos nombres, tendremos evidencia de que Tailwind está generando las clases utilizadas en nuestros HTML.  
## **4. Iniciemos el modo desarrollo**  
Abre una terminal y ejecuta:  
bash  
npm run dev  
Deberías obtener un mensaje parecido a:  
text  
≈ tailwindcss v4.3.5  Done in ...  
Déjalo funcionando. Este proceso vigilará los cambios en tus archivos.  
Abre otra terminal y ejecuta:  
bash  
source env/bin/activate python manage.py check  
Si Django no encuentra errores, inicia:  
bash  
python manage.py runserver  
Visita:  
[http://127.0.0.1:8000/ ](http://127.0.0.1:8000/?utm_source=chatgpt.com "http://127.0.0.1:8000/?utm_source=chatgpt.com")  
## **5. Una mejora importante para nuestro proyecto**  
Quiero anticipar algo de nuestra arquitectura: actualmente tienes una carpeta templates/partials/, lo cual es perfecto.  
Más adelante utilizaremos esta organización:  
text  
templates/ │ ├── base.html │ ├── partials/ │   ├── navbar.html │   ├── footer.html │   ├── messages.html │   ├── course_card.html │   └── pagination.html │ ├── institutional/ │   └── home.html │ ├── academy/ ├── accounts/ └── library/  
Esto permitirá que HTMX actualice componentes individuales sin tener que reconstruir páginas completas.  
## **6. Nuestro siguiente paso**  
Antes de continuar con el diseño visual, quiero validar tres cosas:  
Comprobación del frontend IVA  
Marca lo que ya hayas comprobado.  
Tailwind genera las clases CSS.  
python manage.py check termina correctamente.  
La página principal se visualiza correctamente.  
Enviar resultados  
Mi siguiente objetivo será construir el sistema de diseño del Instituto Vak Advaita, con tipografía académica, paleta institucional, navegación responsive y tarjetas reutilizables.  
Después incorporaremos nuestro primer componente HTMX real: una interacción entre el catálogo de cursos y Django.  
Vamos muy bien: ya tenemos Tailwind compilando y una arquitectura Django que no necesita ser alterada.  
   
