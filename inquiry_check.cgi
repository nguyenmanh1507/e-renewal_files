#!/usr/local/bin/ruby
# -*- coding: utf-8 -*-

require 'logger'
require 'yaml'
require 'erb'
require 'cgi'
require 'pp'
require 'cgi/session'
require 'cgi/handler'

class Handler < CGI::Handler
  def add_error(name, str)
    error = @params[:error]
    error[name] = [] if error[name].nil?
    error[name].push str
  end
  
  def validate
    validate_name
    validate_furigana 
    validate_website 
    validate_tel 
    validate_mail 
    validate_message
    validate_check
  end

  def validate_name
    if blank?(@params['sei']) or blank?(@params['mei'])
      add_error('name', "氏名は必須項目です。")
    end
  end
  def validate_furigana
    if blank?(@params['sei_furigana']) or blank?(@params['mei_furigana'])
      add_error('name', "フリガナは必須項目です。")
    elsif !zenkakku_katakana?(@params['sei_furigana']) or !zenkakku_katakana?(@params['mei_furigana'])
      add_error('name', "フリガナは全角カタカナでご入力ください。")
    end    
  end
  def validate_website
    url = @params['url']
    if not blank? url
      if not hankaku? url
        add_error('url', "URLは半角英数字でご入力ください。")
      end
    end
  end

  def validate_tel
    tel = @params['tel']
    if not blank? tel
      if not tel =~ /^\d+(-\d+)+$/
        add_error('tel', "電話番号は半角数字、ハイフン付きでご入力ください。")
      end
    end
  end
  def validate_mail
    mail = @params['mail']
    if blank? mail
      add_error('mail', "メールアドレスは必須項目です。")
    elsif not hankaku? mail
      add_error('mail', "メールアドレスは半角英数字でご入力ください。")
    end    
  end
  def validate_message
    if blank? @params['message']
      add_error('message', "お問い合せ内容は必須項目です。")
    end
  end

  def validate_check
    if blank? @params['check']
      add_error('check', "利用目的の同意は必須項目です。")
    end
  end

  def write_log
    logger.info "\nFailed check\n"+@params.pretty_inspect
  end  

  def execute
    @params = cgi.params
    # flatten
    @params.each {|key, val|
      @params[key] = val[0] if not val.nil?
      @params[key].strip! if not @params[key].nil?
    }
    @params[:error] = {}

    validate
    session['params'] = @params.to_yaml
    if blank?(@params[:error])
      redirect_to 'inquiry_confirm.cgi'
    else
      write_log
      redirect_to 'inquiry_input.cgi'
    end
  end
end

Handler.new.run


