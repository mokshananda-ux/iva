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
   
  `apps/` una app por dominio funcional.ˉˉaˉ̵̶   a̶͞    a͞  
  `templates/`, `static/`, `media/`.  
   
  `requirements/` dependencias por entorno.  
   
  `tests/` pruebas de reglas de negocio.  
   
 **Decisiones de diseño relevantes**  
   
 **Usuario personalizado** (`accounts.User`) basado en email desde el inicio.  
   
 **"Inscrito" se calcula** a partir de matrículas activas (`User.is_enrolled`), no es un rol persistente.  
   
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
   
 *python manage.py makemessages -l sa*  
   
 *python manage.py makemessages -l pt*  
   
 **ollama pull translategemma:4b**  
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
          **model="translategemma:4b",**  
   
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
   
   
 **Decisión de arquitectura para Tailwind**  
Añadir na carpeta assets/.  
   
 La estructura resultante será:  
   
   
 iva/ │ ├── apps/ ├── config/ ├── assets/ │   └── css/ │       └── app.css          # Fuente Tailwind │ ├── static/ │   ├── css/ │   │   └── app.css          # CSS compilado │   └── js/ │ ├── templates/ │   ├── base.html │   ├── institutional/ │   ├── academy/ │   ├── accounts/ │   └── partials/ │ ├── manage.py ├── package.json └── package-lock.json  
   
 Una decisión importante: no vamos a poner Node.js dentro de apps/. Tailwind es una herramienta de construcción del frontend, no una aplicación de negocio Django.  
**Instalemos Tailwind CSS 4**  
Desde la raíz del proyecto, con tu entorno virtual activado, ejecuta:  
   
 bash  
   
 mkdir -p assets/css  
   
 Crear package.json  
   
 bash  
   
 npm init -y  
   
 Esto crea el archivo de configuración de npm.  
   
 Instalar Tailwind  
   
 bash  
   
 npm install -D tailwindcss @tailwindcss/cli  
   
 Comprueba las versiones:  
   
 bash  
   
 npm list tailwindcss @tailwindcss/cli  
   
   
**Crear archivo fuente CSS**  
bash  
   
 nano assets/css/app.css  
   
 Introduce este contenido:  
   
 css  
   
 @import "tailwindcss";  
   
    
   
 /\*  
   
 ========================================  
   
 INSTITUTO VAK ADVAITA  
   
 Sistema de diseño institucional  
   
 ========================================  
   
 \*/  
   
    
   
 /\* Detección de plantillas Django \*/  
   
 @source "../../templates";  
   
    
   
 /\* Identidad visual \*/  
   
 @theme {  
   
     --color-iva-zaffron:  #F4C430 ;

     --color-iva-olive:  #808000;;
   
     --color-iva-ivory: #F5F0E6;  
   
     --color-iva-ochre: #745B3C;  
   
     --color-iva-charcoal: #292722;

     --color-iva-background: #FAF9F6;
    
     --color-iva-border: #E7E2D9;
   
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
   
 \<div class="bg-iva-ochre text-white">  
   
     Instituto Vak Advaita  
   
 \</div>  
**5. Configurar los comandos de compilación**  
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
**6. Primera compilación**  
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
**7. Comprobar la configuración de Django**  
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
**Cómo quedará nuestro flujo de trabajo**  
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
Diagnóstico de instalación  
   
   
  
|  |  |  
| - | - |  
|   |    |  
| **Elemento** |  **Resultado** |  
| Node.js |  24.22.2 |  
| npm |  11.19.1 |  
| Python |  3.13.5 |  
| Tailwind CSS |  4.3.5 |  
| Compilación |  Exitosa |  
| STATIC_URL |  Configurado |  
| STATIC_ROOT |  Configurado |  
| STATICFILES_DIRS |  Configurado |  
  
   
**Revisemos tu configuración Django**  
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
   
   
