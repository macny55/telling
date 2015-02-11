# -*- coding: utf-8 -*-
import cgi

from google.appengine.ext import db

class Result(db.Model):
  result_id = db.StringProperty()
  score = db.IntegerProperty()
  sex_id = db.StringProperty()
  result = db.StringProperty(multiline=True)
  drama_name = db.StringProperty()
  drama_image_1 = db.StringProperty()
  drama_image_2 = db.StringProperty()
  drama_image_3 = db.StringProperty()
  drama_image_1_url = db.StringProperty()
  drama_image_2_url = db.StringProperty()
  drama_image_3_url = db.StringProperty()
  drama_result = db.StringProperty(multiline=True)

class RequestToken(db.Model):
  token_key    = db.StringProperty(required=True)
  token_secret = db.StringProperty(required=True)

class SaveResult(db.Model):
  twitter_id = db.StringProperty()
  other_name = db.StringProperty()
  other_birthday = db.StringProperty()
  score = db.IntegerProperty()
  date = db.DateTimeProperty(auto_now_add=True)

class SaveProfile(db.Model):
  twitter_id = db.StringProperty()
  your_name = db.StringProperty()
  your_birthday = db.StringProperty()
  your_sex = db.StringProperty()
