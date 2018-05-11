FROM docker.io/centos
ENV PYTHON_VERSION 2.7.12
RUN mkdir /home/htjc/TestDepart/dockerPro/code
RUN mkdir /home/htjc/TestDepart/dockerPro/code/db
WORKDIR /home/htjc/TestDepart/dockerPro/code
ADD ./TestManager/requirements.txt /home/htjc/TestDepart/dockerPro/code/
RUN pip install -r requirements.txt
ADD . /home/htjc/TestDepart/dockerPro/code/