Requisitos
Python 3.7+
pip
virtualenv (opcional, pero recomendado)
Instalación
Sigue estos pasos para instalar y ejecutar la aplicación en tu entorno local.

Clonar el Repositorio
Primero, clona el repositorio de GitHub:

git clone https://github.com/rojored7/Tusdatos.git
cd tu-repositorio

Configurar el Entorno Virtual
Es recomendable utilizar un entorno virtual para gestionar las dependencias. Puedes crear y activar uno usando virtualenv:

# Instalar virtualenv si aún no está instalado
pip install virtualenv

# Crear un entorno virtual
virtualenv venv

# Activar el entorno virtual
# En Windows
.\venv\Scripts\activate
# En Unix o MacOS
source venv/bin/activate


Instalar las Dependencias
Instala las dependencias necesarias para ejecutar la aplicación:

pip install -r requirements.txt


Ejecutar la Aplicación
Utiliza uvicorn para ejecutar la aplicación en tu entorno local:

uvicorn main:app --reload


Acceder a la Aplicación
Abre un navegador y visita http://localhost:8000 para ver la interfaz de usuario de FastAPI y probar los endpoints de la API.


Pruebas
Para ejecutar las pruebas automatizadas, usa el siguiente comando:

pytest
