FROM alexellis2/unicorn-hat:dev
RUN sudo pip install redis

ADD *.py ./

CMD ["sudo","-E", "python2", "app.py"]
