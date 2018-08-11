# -*- coding: utf-8 -*-
from urllib.parse import parse_qsl

def parse_request(request):
    return dict(parse_qsl(request.body.decode("utf-8")))