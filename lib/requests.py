from requests.models import Request
from requests.sessions import Session, merge_setting, merge_cookies
from requests.cookies import RequestsCookieJar
from requests.utils import get_encodings_from_content
from urllib3 import disable_warnings

from lib.data import CONF


def session_request(self, method, url, params=None, data=None, headers=None,
                    cookies=None, files=None, auth=None, timeout=None,
                    allow_redirects=True, proxies=None, hooks=None,
                    stream=None, verify=False, cert=None, json=None):
    conf = CONF.get("requests", {})
    if timeout is None:
        timeout = conf.get("timeout", 30)  # 默认30秒超时
    merged_cookies = merge_cookies(merge_cookies(RequestsCookieJar(),
                                                 self.cookies), cookies or
                                   (conf.cookie if "cookie" in conf else None))

    req = Request(method=method.upper(), url=url,
                  headers=merge_setting(headers, conf["headers"] if "headers"
                                        in conf else {}),
                  files=files,
                  data=data or {},
                  json=json,
                  params=params or {},
                  auth=auth,
                  cookies=merged_cookies,
                  hooks=hooks,
                 )
    prep = self.prepare_request(req)
    proxies = proxies or (conf["proxies"] if "proxies" in conf else {})

    send_kwargs = {
        "timeout": timeout,
        "allow_redirects": allow_redirects,
        "proxies": proxies,
        "stream": stream,
        "verify": verify,
        "cert": cert
    }
    resp = self.send(prep, **send_kwargs)

    if resp.encoding == "ISO-8859-1":
        encodings = get_encodings_from_content(resp.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = resp.apparent_encoding

        resp.encoding = encoding
    return resp


def patch_session():
    Session.request = session_request


def _disable_warnings():
    disable_warnings()

