require 'sinatra'
require 'json'

# please leave this empty get request for health check or change health check api in config/application.rb
get '/' do
    status 200
    body ''
end

post '/receipt' do
	headers['Location']  = get_receipts_service_instance_url
	status 302
	body ''
end

def get_receipts_service_instance_url
  json_response = RestClient.get(ENV['CONSUL_URL'] + '/v1/catalog/service/receipts-service')
  instances = JSON.parse(json_response.body)
  receipts_service_instance = instances[0]
  address = receipts_service_instance['ServiceAddress']
  port = receipts_service_instance['ServicePort']

  return "http://#{address}:#{port}"
end

