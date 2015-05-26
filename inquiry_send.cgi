#!/usr/local/bin/ruby
# -*- coding: utf-8 -*-

require 'net/smtp'
require 'logger'
require 'yaml'
require 'erb'
require 'cgi'
require 'cgi/session'
require 'cgi/handler'

class Handler < CGI::Handler
  FROM = 'renewal_inquiry@mmj.ne.jp'
  TO = 'in-e-renewal@ml.mmj.ne.jp'
  ERB_FILE = File.join(File.dirname(__FILE__), 'mail.erb')

  def mail_body params
    ERB.new(File.read(ERB_FILE), nil, '-').result(binding)
  end
  
  def send_mail params
    Net::SMTP.start('localhost', 25) {|smtp|
      smtp.send_mail(mail_body(params), FROM, TO)
    }    
  end

  def write_log(params)
    logger.info("\n"+mail_body(params))
  end
  
  def execute
    if session['params'].nil? or session['params'].empty?
      redirect_to 'index.html'
      return
    end    
    params = YAML.load(session['params'])
    session.delete
    
    write_log params
    send_mail params
    
    redirect_to 'complete.html'
  end
end

Handler.new.run
