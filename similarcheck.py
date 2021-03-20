import os
from data.emoticons.all import all_emoticons as cjson

path = os.path.dirname(os.path.abspath(__file__))

age_double = 0.3
charm_double = 0.3
mask_double = 20
glasses_double = 20
beard_double = 20
positive_double = 5
negative_double = 5
neutral_double = 5
smile_double = 0.5


def rSimilarEmoticon(receivejson):
    if receivejson == {}:
        return "404"
    print(cjson)
    print(cjson[0]["age"])

    similarnum = 0
    similarscore = 999999
    #sumの値が0に近いほど類似
    for i in range(0,len(cjson)):
        print("a")
        score = 0
        score += abs(cjson[i]["age"] - receivejson["age"]) * age_double
        score += abs(cjson[i]["is_mask"] - receivejson["is_mask"]) * mask_double
        score += abs(cjson[i]["glasses"] - receivejson["glasses"]) * glasses_double
        score += abs(cjson[i]["is_beard"] - receivejson["is_beard"]) * beard_double
        score += abs(cjson[i]["charm_score"] - receivejson["charm_score"]) * charm_double
        score += abs(cjson[i]["is_positive"] - receivejson["is_positive"]) * positive_double
        score += abs(cjson[i]["neutral"] - receivejson["neutral"]) * neutral_double
        score += abs(cjson[i]["is_positive"] - receivejson["is_positive"]) * positive_double
        score += abs(cjson[i]["smile_score"] - receivejson["smile_score"]) * smile_double

        if similarscore > score:
            similarscore = score
            similarnum = i

    print(similarnum)
    print(similarscore)
    return receivejson[similarnum]["emoticon"]
