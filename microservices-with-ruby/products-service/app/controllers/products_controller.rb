require 'sinatra'
require 'json'

get '/' do
    status 200
    body ''
end

get '/product' do
    all_products = Product.all
    if all_products == nil or all_products.empty?
        Product.create(name: "MyProduct", description: "A Product", picture: "A Picture Base64")
    end
    product = all_products.first
    product.to_json
end