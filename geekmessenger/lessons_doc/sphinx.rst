pip install Sphinx

sphinx-quickstart

make html

make latexpdf

sphinx-build -b html sourcedir builddir
sphinx-build -b html doc\source doc\build

sphinx-apidoc [options] -o outputdir packagedir [pathnames]
sphinx-apidoc -o doc\source\code app


