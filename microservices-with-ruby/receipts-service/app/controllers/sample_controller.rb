require 'sinatra'
require 'json'
require 'rest-client'

# please leave this empty get request for health check or change health check api in config/application.rb
get '/' do
    status 200
    body ''
end

post '/receipt' do
  json_response = RestClient.get("#{get_products_service_instance_url}/product")
  product = JSON.parse(json_response.body)
  status 201
  body "A receipt has been created for product #{product['name']}"
end

def get_products_service_instance_url
  json_response = RestClient.get(ENV['CONSUL_URL'] + '/v1/catalog/service/products-service')
  instances = JSON.parse(json_response.body)
  products_service_instance = instances[0]
  address = products_service_instance['ServiceAddress']
  port = products_service_instance['ServicePort']

  return "http://#{address}:#{port}"
end
