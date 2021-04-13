#!/bin/bash

echo "Enter a name for the new service:"
read service_name

echo "Enter a database name for the new service:"
read database_name

if [[ -z $service_name ]]
then
    echo "You haven't entered a service name. Aborting..."
    exit
fi

if [[ -z $database_name ]]
then
    echo "You haven't entered a database name. Aborting..."
    exit
fi

mkdir $service_name

cd $service_name

mkdir app
mkdir config

touch config.ru

echo 'source "https://rubygems.org"' > Gemfile
echo '' >> Gemfile
echo 'gem "sinatra"' >> Gemfile
echo 'gem "rake"' >> Gemfile
echo 'gem "mysql2"' >> Gemfile
echo 'gem "activerecord"' >> Gemfile
echo 'gem "sinatra-activerecord"' >> Gemfile
echo 'gem "json"' >> Gemfile
echo 'gem "rest-client"' >> Gemfile

echo "require './config/application'" > Rakefile
echo "require 'sinatra/activerecord/rake'" >> Rakefile

touch README.md

echo '#!/bin/bash' > run.sh
echo '' >> run.sh
echo 'bundle exec rake db:migrate' >> run.sh
echo 'ruby config/application.rb -p $SINATRA_PORT -o 0.0.0.0' >> run.sh

echo '#!/bin/bash' > setup.sh
echo '' >> setup.sh
echo 'sudo yum install mysql-devel' >> setup.sh
echo 'bundle install --path vendor/cache' >> setup.sh
echo '' >> setup.sh
echo '# rake db:create_migration NAME=create_<model_name> => Edit the generated migration file in db/migrate => bundle exec rake db:migrate' >> setup.sh

cd config

echo 'mysql: &mysql' > database.yml
echo '  adapter: mysql2' >> database.yml
echo "  host: <%= ENV['DATABASE_HOST'] %>" >> database.yml
echo "  port: <%= ENV['DATABASE_PORT'] %>" >> database.yml
echo "  username: <%= ENV['DATABASE_USERNAME'] %>" >> database.yml
echo "  password: <%= ENV['DATABASE_PASSWORD'] %>" >> database.yml
echo "  database: $database_name" >> database.yml
echo '' >> database.yml
echo 'development:' >> database.yml
echo '  <<: *mysql' >> database.yml
echo '' >> database.yml
echo 'production:' >> database.yml
echo '  <<: *mysql' >> database.yml
echo '' >> database.yml
echo 'test:' >> database.yml
echo '  <<: *mysql' >> database.yml

echo "require 'bundler'" > application.rb
echo ''  >> application.rb
echo 'Bundler.require'  >> application.rb
echo ''  >> application.rb
echo "require 'socket'"  >> application.rb
echo "require 'rest-client'"  >> application.rb
echo ''  >> application.rb
echo '$:'" << File.expand_path('../', __FILE__)"  >> application.rb
echo "Dir['./app/**/*.rb'].sort.each { |file| require file }"  >> application.rb
echo "set :root, Dir['./app']"  >> application.rb
echo ''  >> application.rb
echo '#'  >> application.rb
echo '# register this service in consul'  >> application.rb
echo '#'  >> application.rb
echo ''  >> application.rb
echo 'ip_address = Socket.ip_address_list.find { |ai| ai.ipv4? && !ai.ipv4_loopback? }.ip_address'  >> application.rb
echo ''  >> application.rb
echo 'request = {'  >> application.rb
echo "  'ID' => '$service_name-' + ENV['SERVICE_ID'],"  >> application.rb
echo "  'Name' => '$service_name',"  >> application.rb
echo "  'Address' => ip_address,"  >> application.rb
echo "  'Port' => ENV['SINATRA_PORT'].to_i,"  >> application.rb
echo "  'Check' => {"  >> application.rb
echo "    'HTTP' => 'http://' + ip_address + ':' + ENV['SINATRA_PORT'],"  >> application.rb
echo "    'Method' => 'GET',"  >> application.rb
echo "    'Interval'=> '10s',"  >> application.rb
echo "    'Timeout' => '5s',"  >> application.rb
echo "    'DeregisterCriticalServiceAfter' => '30s'"  >> application.rb
echo "  }"  >> application.rb
echo "}"  >> application.rb
echo ''  >> application.rb
echo "RestClient.put(ENV['CONSUL_URL'] + '/v1/agent/service/register', request.to_json, :content_type => 'application/json')"  >> application.rb
echo ''  >> application.rb
echo "# to get the ip address of the host in a docker container use IPSocket.getaddress(ENV['HOSTNAME'])"  >> application.rb
echo ''  >> application.rb

cd ../app

mkdir controllers
mkdir models

cd controllers

echo "require 'sinatra'" > sample_controller.rb
echo "require 'json'" >> sample_controller.rb
echo ''  >> sample_controller.rb
echo '# please leave this empty get request for health check or change health check api in config/application.rb'  >> sample_controller.rb
echo "get '/' do"  >> sample_controller.rb
echo '    status 200' >> sample_controller.rb
echo "    body ''"  >> sample_controller.rb
echo 'end'  >> sample_controller.rb

cd ../..

echo 'FROM ruby:latest' > Dockerfile
echo '' >> Dockerfile
echo 'LABEL maintainer="talal@bluekangaroo.co"' >> Dockerfile
echo '' >> Dockerfile
echo '# these are default values, to override them run docker with flag -e VARNAME=varvalue' >> Dockerfile
echo 'ENV PATH="/usr/src/app/'$service_name':${PATH}"' >> Dockerfile
echo 'ENV DATABASE_HOST=172.17.0.2'  >> Dockerfile
echo 'ENV DATABASE_PORT=3306'  >> Dockerfile
echo 'ENV DATABASE_USERNAME=root'  >> Dockerfile
echo 'ENV DATABASE_PASSWORD=root'  >> Dockerfile
echo 'ENV SINATRA_PORT=5000'  >> Dockerfile
echo 'ENV CONSUL_URL=http://172.17.0.2:8500'  >> Dockerfile
echo 'ENV SERVICE_ID=1'  >> Dockerfile
echo ''  >> Dockerfile
echo 'RUN apt-get update &\'  >> Dockerfile
echo '    apt-get upgrade'  >> Dockerfile
echo ''  >> Dockerfile
echo 'RUN mkdir -p /usr/src/app/'$service_name  >> Dockerfile
echo ''  >> Dockerfile
echo 'COPY . /usr/src/app/'$service_name  >> Dockerfile
echo 'WORKDIR /usr/src/app/'$service_name  >> Dockerfile
echo ''  >> Dockerfile
echo 'RUN rm -rf /usr/src/app/'$service_name'/vendor/cache'  >> Dockerfile
echo 'RUN bundle install --path vendor/cache'  >> Dockerfile
echo 'RUN chmod a+rwx run.sh'  >> Dockerfile
echo ''  >> Dockerfile
echo 'EXPOSE ${SINATRA_PORT}/tcp'  >> Dockerfile
echo ''  >> Dockerfile
echo 'CMD ["run.sh"]'  >> Dockerfile

cd ..

echo '' >> run-all.sh
echo '' >> run-all.sh
echo '#' >> run-all.sh 
echo '# '$service_name' setup' >> run-all.sh
echo '#' >> run-all.sh
echo '' >> run-all.sh
echo 'docker exec -it test-container mysql --user=root --password=$ROOT_PASSWORD --execute="CREATE DATABASE '$database_name';"'  >> run-all.sh
echo ''  >> run-all.sh
echo 'cd '$service_name  >> run-all.sh
echo 'docker build -t '$service_name' .'  >> run-all.sh
echo 'cd ..'  >> run-all.sh
echo ''  >> run-all.sh
echo 'docker run -e DATABASE_HOST=$E_DATABASE_HOST \' >> run-all.sh
echo '           -e DATABASE_USERNAME=root \' >> run-all.sh
echo '           -e DATABASE_PASSWORD=$ROOT_PASSWORD \' >> run-all.sh
echo '           -e CONSUL_URL=http://$CONSUL_HOST:8500 \' >> run-all.sh
echo '           -e SERVICE_ID=1 \' >> run-all.sh
echo '           -d '$service_name >> run-all.sh

