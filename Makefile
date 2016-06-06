
install:
	virtualenv venv
	./venv/bin/pip install nodeenv
	./venv/bin/nodeenv -p --node=5.11.0 --prebuilt
	./venv/bin/pip install -r py_requirements.txt
	./venv/bin/npm install -g gulp-cli
	./venv/bin/npm install -g bower
	./venv/bin/npm install .
	. venv/bin/activate && bower install

update:
	./venv/bin/pip install -r py_requirements.txt
	./venv/bin/npm install .
	. venv/bin/activate && bower install

clean:
	-rm -r bower_components build/* node_modules venv 2> /dev/null || true
