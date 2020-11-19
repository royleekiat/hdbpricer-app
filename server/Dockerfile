FROM python:3.6-slim
COPY . /app
WORKDIR /app
# if using alpine build, RUN apt-get --no-cache add musl-dev linux-headers g++ gfortran build-base openblas-dev libffi-dev
RUN pip install --upgrade cython
RUN ./install.sh
EXPOSE 5000 
ENTRYPOINT [ "python" ] 
CMD [ "app.py" ] 

# docker build --tag hdbpricer-backend .
# docker run --name hdbpricer-backend -p 5000:5000 hdbpricer-backend 