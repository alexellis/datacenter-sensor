FROM alexellis2/python-gpio-flask:v6
WORKDIR /root/

RUN sudo pip install redis

ADD ./*.py ./

EXPOSE 5000

CMD ["python", "app.py"]
