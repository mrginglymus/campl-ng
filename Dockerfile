FROM python:2.7

RUN virtualenv venv \
  && . venv/bin/activate \
  && pip install nodeenv \
  && nodeenv -p --node=5.11 --prebuilt \
  && deactivate \
  && . venv/bin/activate \
  && pip install -r py_requirements.txt \
  && npm install -g grunt-cli \
  && npm install . \
  && bower install .


CMD ["bash"]