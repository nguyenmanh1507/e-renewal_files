#!/usr/local/bin/ruby
# -*- coding: utf-8 -*-

require 'yaml'
require 'erb'
require 'cgi'
require 'cgi/session'
require 'cgi/handler'

class Handler < CGI::Handler
  ERB_FILE = File.join(File.dirname(__FILE__), 'inquiry.erb')

  def gen_html(binding)
    ERB.new(File.read(ERB_FILE), nil, '-').result(binding)
  end

  def get_binding
    params = session['params'] ? YAML.load(session['params']) : {}
    error = params[:error] ? params[:error] : {}

    params.default = ''
    binding
  end  

  def execute
    cgi.out{ gen_html(get_binding) }
  end
end

Handler.new.run




