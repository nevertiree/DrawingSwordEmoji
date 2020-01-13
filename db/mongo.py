# -*- coding: utf-8 -*-

import pymongo
import os
import json

client = pymongo.MongoClient(host='localhost', port=27017)
db = client['DrawingSword']
drawing_sword = db['OCR']

def insert():

    with open(os.path.join("data", "content", "ocr_result_4.csv"), "r", encoding="utf-8") as f:
        for line in f:
            result = drawing_sword.insert(json.loads(line))
            print(result)

def query(target_word):
    results = drawing_sword.find(filter={'words_result.words':{'$regex':target_word}},
                                projection={"_id":0, "words_result_num":0, "words_result.probability":0 })
    sorted_results = results.sort("words_result.probability.average", pymongo.DESCENDING)
    print(sorted_results)
    for result in sorted_results:
        print(result)

if __name__ == "__main__":
    input_key = input("输入想查询的《亮剑》关键字（例如：团长）:")
    query(input_key)
    # insert()