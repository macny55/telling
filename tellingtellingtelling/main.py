#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import images
from google.appengine.ext import db
import webapp2 as webapp
import os
from django.http import HttpResponse, HttpResponseRedirect
from setting import *
import cookie
import logging
import htmlentitydefs
import re
import datetime
import data
import tweepy
import random
from tweepy import OAuthHandler
def is_dev():
    return os.environ["SERVER_SOFTWARE"].find("Development") != -1
SESSION_EXPIRE = 200
CALLBACK_URL = 'http://localhost:9080/login_callback' if is_dev() else 'http://tellingtellingtelling.appspot.com/login_callback'
CALLBACK = 'http://localhost:9080' if is_dev() else 'http://tellingtellingtelling.appspot.com/judge'

#Twitter API --------------------------------------------------------------------#
def token_api(access_token):
    token = pair_dic(access_token)
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(token[u'oauth_token'], token[u'oauth_token_secret'])
    api = tweepy.API(auth_handler=auth)
    return auth, api

def pair_dic(string):
    elems = string.split(u'&')
    return dict([tuple(e.split(u'=')) for e in elems])

def get_usr_name(access_token):
    tmp ,api = token_api(access_token)
    if api:
        time_line = api.user_timeline(count=5)
    else:
        return -1
    if time_line:
        #time_line[0]は最新のツイート
        usr_name = time_line[0].author.screen_name
        return usr_name
    else:
        return 0

class OAuthLogin(webapp.RequestHandler):
    def get(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL,secure=True)
        auth_url = auth.get_authorization_url()
        request_token = data.RequestToken(token_key=auth.request_token.key, token_secret=auth.request_token.secret)
        request_token.put()
        self.redirect(auth_url)

class OAuthLoginCallBack(webapp.RequestHandler):
    def get(self):
        request_token_key = self.request.get("oauth_token")
        request_verifier  = self.request.get('oauth_verifier')
        auth = tweepy.OAuthHandler(CONSUMER_KEY,  CONSUMER_SECRET)
        request_token = data.RequestToken.gql("WHERE token_key=:1",  request_token_key).get()

        if request_token is None:
            self.redirect('/again_result')
        else:
            auth.set_request_token(request_token.token_key,  request_token.token_secret)
            access_token = auth.get_access_token(request_verifier)
            usr_name = get_usr_name(str(access_token))
            cookie.set_cookie(self, str(access_token), SESSION_EXPIRE)
            cookie.set_cookie_usr_name(self, str(usr_name), SESSION_EXPIRE)
            self.redirect('/share_result')

class OAuthLogout(webapp.RequestHandler):
    def get(self):
        cookie.del_cookie(self)
        self.redirect('/')

#/Twitter API --------------------------------------------------------------------#

#関数-----------------------------------------------------------------------------#
# 実体参照 & 文字参照を通常の文字に戻す
def htmlentity2unicode(text):
    # 正規表現のコンパイル
    reference_regex = re.compile(u'&(#x?[0-9a-f]+|[a-z]+);', re.IGNORECASE)
    num16_regex = re.compile(u'#x\d+', re.IGNORECASE)
    num10_regex = re.compile(u'#\d+', re.IGNORECASE)
    
    result = u''
    i = 0
    while True:
        # 実体参照 or 文字参照を見つける
        match = reference_regex.search(text, i)
        if match is None:
            result += text[i:]
            break
        
        result += text[i:match.start()]
        i = match.end()
        name = match.group(1)
        
        # 実体参照
        if name in htmlentitydefs.name2codepoint.keys():
            result += unichr(htmlentitydefs.name2codepoint[name])
        # 文字参照
        elif num16_regex.match(name):
            # 16進数
            result += unichr(int(u'0'+name[1:], 16))
        elif num10_regex.match(name):
            # 10進数
            result += unichr(int(name[1:]))

    return result

#　星座を返す
def serch_constellation(month,day):
    seiza = { 1 : 10, 2 : 11, 3 : 12, 4 : 1,5 : 2, 6 : 3, 7 : 4, 8 : 5,9 : 6, 10 : 7, 11 : 8, 12 : 9 }
    if day > 22:
        if month == 12:
            return seiza[1]
        else:
            return seiza[month + 1]
    else :
        return seiza[month]

#/関数----------------------------------------------------------------------------#

class TopPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__),'view/top.html')
        self.response.out.write(template.render(path,{}))

class Profile(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'view/profile.html')
        self.response.out.write(template.render(path,{}))

#class Judge(webapp.RequestHandler):
#    def get(self):
#        path = os.path.join(os.path.dirname(__file__), 'view/result.html')
#        self.response.out.write(template.render(path, {}))
#
#    def post(self):
#        login = 0
#        twitter_name = ''
#        token = cookie.load_cookie(self)
#        if token != 'deleted' and token != '':
#            login = 1
#            twitter_name = cookie.load_cookie_usr_name(self)
#        your_name = self.request.get('your-name')
#        your_birthday = self.request.get('your-birthday')
#        your_sex = self.request.get('your-sex')
#        other_name = self.request.get('other-name')
#        other_birthday = self.request.get('other-birthday')
#        
#        if your_sex == "female":
#            female_birthday = datetime.datetime.strptime(your_birthday, '%Y-%m-%d')
#            male_birthday   = datetime.datetime.strptime(other_birthday, '%Y-%m-%d')
#        else:
#            female_birthday = datetime.datetime.strptime(other_birthday, '%Y-%m-%d')
#            male_birthday   = datetime.datetime.strptime(your_birthday, '%Y-%m-%d')
#
#        female_constellation = serch_constellation(int(female_birthday.month),int(female_birthday.day))
#        male_constellation = serch_constellation(int(male_birthday.month),int(male_birthday.day))
#        affinity_id = (female_constellation - 1) * 12 + male_constellation
#        query = db.GqlQuery("SELECT * FROM Result WHERE __key__ = key('Result' , :1)" , str(affinity_id))
#        horoscope_score = query[0].score
#        horoscope_result = query[0].result
#        path = os.path.join(os.path.dirname(__file__), 'view/result.html')
#        self.response.out.write(template.render(path, {'your_name':your_name,
#                                                       'your_birthday':your_birthday,
#                                                       'your_sex':your_sex,
#                                                       'other_name':other_name,
#                                                       'other_birthday':other_birthday,
#                                                       'score':horoscope_score,
#                                                       'result':horoscope_result,
#                                                       'login':login,
#                                                       'twitter_name':twitter_name
#                                                       }))

class Judge(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'view/drama_result.html')
        self.response.out.write(template.render(path, {}))

    def post(self):
        your_name = self.request.get('your-name')
        your_birthday = self.request.get('your-birthday')
        your_sex = self.request.get('your-sex')
        other_name = self.request.get('other-name')
        other_birthday = self.request.get('other-birthday')
        if your_sex == "female":
            female_birthday = datetime.datetime.strptime(your_birthday, '%Y-%m-%d')
            male_birthday   = datetime.datetime.strptime(other_birthday, '%Y-%m-%d')
            sex_id = '2'
        else:
            female_birthday = datetime.datetime.strptime(other_birthday, '%Y-%m-%d')
            male_birthday   = datetime.datetime.strptime(your_birthday, '%Y-%m-%d')
            sex_id = '1'
        female_constellation = serch_constellation(int(female_birthday.month),int(female_birthday.day))
        male_constellation = serch_constellation(int(male_birthday.month),int(male_birthday.day))
        affinity_id = (female_constellation - 1) * 12 + male_constellation
        query = db.GqlQuery("SELECT * FROM Result WHERE __key__ = key('Result' , :1)" , str(affinity_id)+'-'+sex_id)
        horoscope_result = query[0].drama_result
        drama_name = query[0].drama_name
        image_no = random.randint(1,3)
        if image_no == 1:
            drama_image = query[0].drama_image_1
            drama_image_url = query[0].drama_image_1_url
        elif image_no == 2:
            drama_image = query[0].drama_image_2
            drama_image_url = query[0].drama_image_2_url
        elif image_no == 3:
            drama_image = query[0].drama_image_3
            drama_image_url = query[0].drama_image_3_url
        path = os.path.join(os.path.dirname(__file__), 'view/drama_result.html')
        self.response.out.write(template.render(path, {'your_name':your_name,
                                                       'your_birthday':your_birthday,
                                                       'your_sex':your_sex,
                                                       'other_name':other_name,
                                                       'other_birthday':other_birthday,
                                                       'result':horoscope_result,
                                                       'drama_image':drama_image,
                                                       'drama_image_url':drama_image_url,
                                                       'drama_name':drama_name
                                                       }))

class DataStore(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'view/data_store.html')
        self.response.out.write(template.render(path, {}))

    def post(self):
        import store
        result_id = self.request.get('id')
        score = self.request.get('score')
        result = self.request.get('result')
        store.save_result(result_id,score,result)
        path = os.path.join(os.path.dirname(__file__), 'view/data_store.html')
        self.response.out.write(template.render(path, {}))

class DataUpdate(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'view/data_update.html')
        self.response.out.write(template.render(path, {}))

    def post(self):
        import store
        result_id = self.request.get('id')
        drama_name = self.request.get('drama_name')
        sex_id = self.request.get('sex_id') #1=man,2=woman
        drama_image_1 = self.request.get('drama_image_1')
        drama_image_2 = self.request.get('drama_image_2')
        drama_image_3 = self.request.get('drama_image_3')
        drama_image_1_url = self.request.get('drama_image_1_url')
        drama_image_2_url = self.request.get('drama_image_2_url')
        drama_image_3_url = self.request.get('drama_image_3_url')
        drama_result = self.request.get('drama_result')
        store.update_result(result_id,drama_name,sex_id,drama_image_1,drama_image_2,drama_image_3,drama_image_1_url,drama_image_2_url,drama_image_3_url,drama_result)
        path = os.path.join(os.path.dirname(__file__), 'view/data_update.html')
        self.response.out.write(template.render(path, {}))

class Register(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'view/register.html')
        self.response.out.write(template.render(path, {}))

class SaveResult(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'view/top.html')
        self.response.out.write(template.render(path, {}))

    def post(self):
        
        #20141222 result.htmlのデータを保存する処理を書く
        # 保存先はSaveResultとSaveProfile

        path = os.path.join(os.path.dirname(__file__), 'view/register.html')
        self.response.out.write(template.render(path, {}))

class ShareResult(webapp.RequestHandler):
    def get(self):
        token = cookie.load_cookie(self)
        twitter_name = cookie.load_cookie_usr_name(self)
        get_flag = 1
        path = os.path.join(os.path.dirname(__file__), 'view/share.html')
        self.response.out.write(template.render(path, {'twitter_name':twitter_name,
                                                       'get_flag':get_flag
                                                      }))

    def post(self):
        token = cookie.load_cookie(self)
        twitter_name = ''
        get_flag = 0
        if token != 'deleted' and token != '':
            twitter_name = cookie.load_cookie_usr_name(self)
        else:
            self.redirect('/login')
        drama_name = self.request.get('drama_name')
        drama_image = self.request.get('drama_image')
        drama_image_url = self.request.get('drama_image_url')
        path = os.path.join(os.path.dirname(__file__), 'view/share.html')
        self.response.out.write(template.render(path, {'twitter_name':twitter_name,
                                                       'drama_name':drama_name,
                                                       'drama_image':drama_image,
                                                       'drama_image_url':drama_image_url,
                                                       'get_flag':get_flag
                                                      }))

class AgainResult(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'view/top.html')
        self.response.out.write(template.render(path, {}))

    def post(self):
        tweet_content = self.request.get('tweet')
        drama_image = self.request.get('drama_image')
        drama_image_url = self.request.get('drama_image_url')
        token = cookie.load_cookie(self)
        tmp ,api = token_api(token)
        api.update_status(tweet_content +' '+ drama_image_url +' http://tellingtellingtelling.appspot.com/')
        path = os.path.join(os.path.dirname(__file__), 'view/again.html')
        self.response.out.write(template.render(path, {}))

app = webapp.WSGIApplication([
    ('/', TopPage),
    ('/profile', Profile),
    ('/judge', Judge),
    ('/login', OAuthLogin),
    ('/login_callback', OAuthLoginCallBack),
    ('/logout', OAuthLogout),
    ('/register', Register),
    ('/save_result', SaveResult),
    ('/share_result', ShareResult),
    ('/again_result', AgainResult),
    ('/data_store', DataStore),
    ('/data_update', DataUpdate)
], debug=True)
