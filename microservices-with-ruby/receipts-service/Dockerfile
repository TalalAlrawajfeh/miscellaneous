FROM ruby:latest

LABEL maintainer="talal@bluekangaroo.co"

# these are default values, to override them run docker with flag -e VARNAME=varvalue
ENV PATH="/usr/src/app/receipts-service:${PATH}"
ENV DATABASE_HOST=172.17.0.2
ENV DATABASE_PORT=3306
ENV DATABASE_USERNAME=root
ENV DATABASE_PASSWORD=root
ENV SINATRA_PORT=5000
ENV CONSUL_URL=http://172.17.0.2:8500
ENV SERVICE_ID=1

RUN apt-get update &\
    apt-get upgrade

RUN mkdir -p /usr/src/app/receipts-service

COPY . /usr/src/app/receipts-service
WORKDIR /usr/src/app/receipts-service

RUN rm -rf /usr/src/app/receipts-service/vendor/cache
RUN bundle install --path vendor/cache
RUN chmod a+rwx run.sh

EXPOSE ${SINATRA_PORT}/tcp

CMD ["run.sh"]
