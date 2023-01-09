FROM python
RUN mkdir /home/app
WORKDIR /home/app
COPY ./requirements.txt ./
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
COPY ./ ./
EXPOSE 5000
CMD python3 -m flask run -h 0.0.0.0