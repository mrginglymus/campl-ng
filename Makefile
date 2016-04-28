
install:
	virtualenv venv
	./venv/bin/pip install nodeenv
	./venv/bin/nodeenv -p --node=5.11.0 --prebuilt
	./venv/bin/pip install -r py_requirements.txt
	./venv/bin/npm install -g gulp-cli
	./venv/bin/npm install .
	./node_modules/bower/bin/bower install

update:
	./venv/bin/pip install -r py_requirements.txt
	./venv/bin/npm install .
	./node_modules/bower/bin/bower install

clean:
	-rm -r .sass-cache bower_components build/* node_modules venv