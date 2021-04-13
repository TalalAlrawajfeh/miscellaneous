#!/bin/bash

sudo yum install mysql-devel
bundle install --path vendor/cache

# rake db:create_migration NAME=create_products => Edit the generated migration file in db/migrate => bundle exec rake db:migrate