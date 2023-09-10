FROM ubuntu

RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get install -y pip && \
    pip install pandas && \
    pip install dash && \
    pip install numpy

WORKDIR /app

COPY ./front.py /app/front.py
COPY ./iterational_solution.py /app/iterational_solution.py

CMD ["python3", "serv2/script.py"]