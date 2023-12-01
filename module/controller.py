from rest_framework.response import Response
from rest_framework.decorators import api_view

from module import memberService
from module import chartService
from module import dataService


@api_view(["GET"])
def memberAgeGender(req) :
    data = memberService.memberAgeGender()
    return Response(data)


@api_view(["GET"])
def memberAddress(req) :
    data = memberService.memberAddress()
    return Response(data)


@api_view(["GET"])
def inquiryChart(req) :
    return ""


@api_view(["GET"])
def orderChart(req) :
    return ("")


@api_view(["GET"])
def dataAnalysis(req) :
    return ""