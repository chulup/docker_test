FROM tatsushid/tinycore-python:latest

ADD src/localinfo.py /opt/

CMD ["python3 /opt/localinfo.py"]
