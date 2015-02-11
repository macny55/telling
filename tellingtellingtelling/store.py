# -*- coding: utf-8 -*-

import data
from google.appengine.ext import db


def save_result(result_id,score,result):
    data.Result.get_or_insert(key_name=result_id,result_id=result_id,score=int(score),result=result)

def update_result(result_id,drama_name,sex_id,drama_image_1,drama_image_2,drama_image_3,drama_image_1_url,drama_image_2_url,drama_image_3_url,drama_result):
    query = db.GqlQuery("SELECT * FROM Result WHERE __key__ = key('Result' , :1)" , result_id)
    result = data.Result(key_name=result_id+'-'+sex_id,result_id=result_id,sex_id=sex_id, score=query[0].score,result=query[0].result,drama_name=drama_name,drama_image_1=drama_image_1,drama_image_2=drama_image_2,drama_image_3=drama_image_3,drama_image_1_url=drama_image_1_url,drama_image_2_url=drama_image_2_url,drama_image_3_url=drama_image_3_url,drama_result=drama_result)
    result.put()


