#!/bin/bash

bundle exec rake db:migrate
ruby config/application.rb -p $SINATRA_PORT -o 0.0.0.0