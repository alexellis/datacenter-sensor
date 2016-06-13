FROM alexellis2/python-gpio-flask:v6

RUN sudo pip install redis

ADD ./*.py ./

EXPOSE 5000

CMD ["sudo", "-E", "python", "app.py"]

