import os
from data.emoticons.calm import calm_emoticons
from data.emoticons.happy import happy_emoticons
from data.emoticons.sad import sad_emoticons

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
    print(receivejson)
    print("aaa\n\n\n\n")
    print(sad_emoticons)
    print(happy_emoticons)
    print(calm_emoticons)
    sadjson = sad_emoticons
    happyjson = happy_emoticons
    calmjson = calm_emoticons

    for data in happyjson:
        sadjson.append(data)
    for data in calmjson:
        sadjson.append(data)

    cjson = sadjson

    print(cjson)

    similarnum = 0
    similarscore = 999999
    #sumの値が0に近いほど類似
    for i in range(0,len(cjson)):
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
