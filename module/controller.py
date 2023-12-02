#-*- coding:utf-8 -*-

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


@api_view(["POST"])
def inquiryChart(req) :
    data = chartService.inquiryChart(req.data['age'], req.data['gender'], req.data['year'], req.data['month'])
    return Response(data)


@api_view(["POST"])
def orderChart(req) :
    data = chartService.orderChart(req.data['age'], req.data['gender'], req.data['year'], req.data['month'])
    return Response(data)


@api_view(["POST"])
def dataAnalysis(req) :
    data  = None

    if (req.data['flag'] == 'i') :
        data = dataService.inquiryAnalysis(req.data['age'], req.data['gender'], req.data['year'], req.data['month'])
    else :
        data = dataService.orderAnalysis(req.data['age'], req.data['gender'], req.data['year'], req.data['month'])

    return Response(data)