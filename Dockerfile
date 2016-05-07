FROM python:2.7

RUN useradd -ms /bin/bash camplng

USER camplng

WORKDIR /home/camplng/

ADD . ./

CMD ["bash"]
