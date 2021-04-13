require 'bundler'

Bundler.require

require 'socket'
require 'rest-client'

$: << File.expand_path('../', __FILE__)
Dir['./app/**/*.rb'].sort.each { |file| require file }
set :root, Dir['./app']

#
# register this service in consul
#

ip_address = Socket.ip_address_list.find { |ai| ai.ipv4? && !ai.ipv4_loopback? }.ip_address

request = {
  'ID' => 'api-gateway-' + ENV['SERVICE_ID'],
  'Name' => 'api-gateway',
  'Address' => ip_address,
  'Port' => ENV['SINATRA_PORT'].to_i,
  'Check' => {
    'HTTP' => 'http://' + ip_address + ':' + ENV['SINATRA_PORT'],
    'Method' => 'GET',
    'Interval'=> '10s',
    'Timeout' => '5s',
    'DeregisterCriticalServiceAfter' => '30s'
  }
}

RestClient.put(ENV['CONSUL_URL'] + '/v1/agent/service/register', request.to_json, :content_type => 'application/json')

# to get the ip address of the host in a docker container use IPSocket.getaddress(ENV['HOSTNAME'])

