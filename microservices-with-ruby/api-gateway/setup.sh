#!/bin/bash

sudo yum install mysql-devel
bundle install --path vendor/cache

# rake db:create_migration NAME=create_<model_name> => Edit the generated migration file in db/migrate => bundle exec rake db:migrate
