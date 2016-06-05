FROM alexellis2/unicorn-hat:dev
RUN sudo pip install redis

ADD app.py ./

CMD ["sudo", "python2", "app.py"]
