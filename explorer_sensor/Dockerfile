FROM alexellis2/python-gpio-arm:v6-dev
RUN pip2 install redis
RUN pip2 install explorerhat
RUN sudo apt-get -qy install python-smbus

ADD *.py ./

CMD ["sudo", "-E", "python2", "app.py"]
