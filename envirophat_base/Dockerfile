FROM alexellis2/python-gpio-arm:v6-dev
RUN apt update && apt -qy install \
                            git \
                            python-smbus

RUN sudo pip install redis

RUN git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
RUN cd Adafruit_Python_GPIO && \
 sudo python setup.py install

RUN git clone https://github.com/adafruit/Adafruit_Python_BME280
RUN mv Adafruit_Python_BME280/* ./

RUN git clone https://github.com/adafruit/Adafruit_DotStar_Pi
RUN cd Adafruit_DotStar_Pi && \
  sudo python setup.py install
