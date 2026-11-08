**Instituto Vak Advaita (IVA)**  
   
    
   
     
   
    
   
   Plataforma educativa: monolito modular con Django. Núcleo común + apps de  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    dominio independientes, desplegadas como una sola aplicación.  
   
    
   
     
   
    
   
   **Requisitos**  
- Python 3.12+  
- PostgreSQL 16 (o SQLite para arranque rápido en desarrollo)  
- Docker (opcional, recomendado)  
   
    
   
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
- `config/` configuración dividida (`base`, `development`, `production`).  
- `apps/` una app por dominio funcional.  
- `templates/`, `static/`, `media/`.  
- `requirements/` dependencias por entorno.  
- `tests/` pruebas de reglas de negocio.  
   
    
   
   **Decisiones de diseño relevantes**  
- **Usuario personalizado** (`accounts.User`) basado en email desde el inicio.  
- **"Inscrito" se calcula** a partir de matrículas activas (`User.is_enrolled`),  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    no es un rol persistente.  
- **Autorización siempre en servidor** (`apps/core/permissions.py`).  
- **Descargas protegidas** por endpoint con control de permisos y registro.  
- **Stripe**: la matrícula se activa SOLO tras verificar el webhook  
   
    
   
     
   
    
   
    `checkout.session.completed`, de forma **idempotente**  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
    (`commerce.ProcessedWebhookEvent`). Nunca por el retorno a la página de éxito.  
- **i18n** con `gettext`, UTF-8 y almacenamiento Unicode en PostgreSQL;  
   
    
   
     
   
    
   
      
   
    
   
     
   
    
   
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
   
    
   
     
   
    
 ollama pull translategemma:12b  
pip install ollama  
   
import ollama  
   
def traducir(texto):  
   
    prompt = f"""You are a professional Spanish (es) to Catalan (ca) translator.  
Your goal is to accurately convey the meaning and nuances of the original Spanish text.  
   
Produce only the Catalan translation, without explanations.  
   
Please translate the following Spanish text into Catalan:  
   
   
{texto}  
"""  
   
    response = ollama.chat(  
        model="translategemma:12b",  
        messages=\[  
            {  
                "role": "user",  
                "content": prompt  
            }  
        \],  
        options={  
            "temperature": 0  
        }  
    )  
   
    return response\["message"\]\["content"\].strip()    
   
    
   
    
-   
    
   
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
- gettext_lazy as \_: para modelos, campos, formularios y metadatos.  
- gettext as \_: para textos que se traducen en el momento de ejecutarse, como determinadas validaciones y funciones.  
   
    
   
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
1. El campo preferred_language guarda la elección.  
2. Django recupera esa elección cuando el usuario inicia sesión.  
3. Django activa ese idioma para las respuestas que recibe el usuario.  
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
   
    
   
     
