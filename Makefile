
install:
	virtualenv venv -p python3
	./venv/bin/pip install nodeenv
	./venv/bin/nodeenv -p --node=8.9.3 --prebuilt
	./venv/bin/pip install -r requirements.txt
	. venv/bin/activate && npm install -g gulp-cli
	. venv/bin/activate && npm install -g bower
	. venv/bin/activate && npm install .
	. venv/bin/activate && bower install

update:
	./venv/bin/pip install -r py_requirements.txt
	. venv/bin/activate && npm install .
	. venv/bin/activate && bower install

clean:
	-rm -r bower_components build/* node_modules venv 2> /dev/null || true
