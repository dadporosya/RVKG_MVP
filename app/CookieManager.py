import uuid
from flask import make_response, request
import _helpers as h

COOKIE_LABEL = "my_cookie_name"

def generateCookie():
    return str(uuid.uuid4())

def setCookie(response=None, cookie: str | None = None, lifeTime: int | None = None):
    if not cookie:
        cookie = generateCookie()

    if not lifeTime:
        lifeTime = int(h.getTimeInSec(weeks=1))

    if not response:
        response = make_response("Cookie set!")
    response.set_cookie(
        COOKIE_LABEL,
        cookie,
        max_age=lifeTime
    )

    return response

# def setCookie(cookie:str|None=None, lifeTime:int|None=None):
#     if not cookie:
#         cookie = generateCookie()
#
#     if not lifeTime:
#         lifeTime = int(h.getTimeInSec(weeks=1))
#
#     response = make_response("Cookie set!")
#     response.set_cookie(COOKIE_LABEL,
#                         cookie,
#                         max_age=lifeTime)
#
#     return response

def getCookie() -> str | None:
    return request.cookies.get(COOKIE_LABEL)