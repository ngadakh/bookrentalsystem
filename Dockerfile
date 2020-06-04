FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y software-properties-common
RUN apt-add-repository universe
RUN apt-get update
RUN apt-get update && apt-get install \
  -y --no-install-recommends python3 python3-virtualenv
RUN apt-get install -y python3-pip python-dev build-essential
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ADD . /bookrentalsystem
WORKDIR /bookrentalsystem
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["run.py"]
