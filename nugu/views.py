from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from pprint import pprint
from nugu.get_recommendations import main as reco
from nugu.edit_distance import main as e_distance
@csrf_exempt
def message(request):
    d = json.load(request)
    return_list = ''
    pprint(d)
    action = d['action']
    parameters = action['parameters']
    actions = action['actionName']
    # print(list(parameters.keys()))
    # condition = list(parameters.keys())
    # print(condition[0])

    if actions == "answer.like":

        movie_name = parameters['movie_name']
        v = movie_name['value']
        new_v = e_distance(v)
        return_name = reco('3', new_v)

        count = 0
        for i in return_name[:5]:
            count += 1
            print(return_name[4])
            if not count == 5:
                return_list = return_list + i + ','
            else:
                return_list = return_list + i

        print(return_list)
        # print(request.action)
        return JsonResponse({
            "version": "2.0",
            "resultCode": "OK",
            "output": {
                "movie_name": v,
                "result_movie": return_list
            }
        })
    elif actions == "answer.genre":
        movie_name = parameters['movie_genre']
        v = movie_name['value']
        print(v)
        # new_v = e_distance(v)
        return_name = reco('2', v)
        print(return_name)

        count = 0
        for i in return_name[:5]:
            count += 1
            print(return_name[4])
            if not count == 5:
                return_list = return_list + i + ','
            else:
                return_list = return_list + i

        print(return_list)
        # print(request.action)
        return JsonResponse({
            "version": "2.0",
            "resultCode": "OK",
            "output": {
                "movie_genre": v,
                "result_genre": return_list
            }
        })
    elif actions == "answer.idle":
        print("00001")
        return_name = reco('1', '1')
        print("00002")
        print(return_name)
        count = 0
        for i in return_name[:5]:
            count += 1
            print(return_name[4])
            if not count == 5:
                return_list = return_list + i + ','
            else:
                return_list = return_list + i

        print(return_list)
        # print(request.action)
        return JsonResponse({
            "version": "2.0",
            "resultCode": "OK",
            "output": {
                "return_idle": return_list
            }
        })



# Create your views here.
