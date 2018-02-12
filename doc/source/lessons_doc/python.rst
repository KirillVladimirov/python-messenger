
Консольные команды python
=========================


python
------
python -m http.server 8888

python -m SimpleHTTPServer 8888


pyqt5
-----
pyuic5 messanger_window.ui -o messanger_window.py

pyuic5 geekmessenger\app\client\templates\client_window.ui > geekmessenger\app\client\templates\client_window.py


pytest
------
py.test --timeout=300

py.test --cov=myproj tests/

py.test --pep8


pip
---
python -m venv .env

source .env/bin/activate

.env\Scripts\activate.bat

pip search astronomy

pip install novas

pip install requests==2.6.0

pip install --upgrade requests

pip show requests

pip list

pip freeze > requirements.txt

pip install -r requirements.txt


Sphinx
------
pip install Sphinx

sphinx-quickstart

make html

make latexpdf

sphinx-build -b html sourcedir builddir
sphinx-build -b html doc\source doc\build

sphinx-apidoc [options] -o outputdir packagedir [pathnames]
sphinx-apidoc -o doc\source\code app