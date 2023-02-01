# tfg-2023
PROYECTO DE FIN DE GRADO DE LA UNIVERSIDAD DE SEVILLA REALIZADO POR PABLO GUTIERREZ CEBALLOS Y ROMAN FLORES RODRIGUEZ.

VALOR GROUPS ES UNA APLICACIÓN WEB PENSADA PARA JUGADORES DE VALORANT QUE QUIERAN ENCONTRAR EQUIPO, TENER ACCESO A ESTADISTICAS
Y PODER PARTICIPAR EN TORNEOS.

SIN ANIMO DE LUCRO.

To get this project up and running locally on your computer:

Set up the Python development environment. We recommend using a Python virtual environment.
Note: This has been tested against Django 3.1.2 (and may not work or be "optimal" for other versions).

Assuming you have Python setup, run the following commands (if you're on Windows you may use py or py -3 instead of python to start Python):
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py test # Run the standard tests. These should all pass.
python3 manage.py createsuperuser # Create a superuser
python3 manage.py runserver
Open a browser to http://127.0.0.1:8000/admin/ to open the admin site
Create a few test objects of each type.
Open tab to http://127.0.0.1:8000 to see the main site, with your new objects.
