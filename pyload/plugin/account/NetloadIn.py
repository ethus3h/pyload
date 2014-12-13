# -*- coding: utf-8 -*-

import re
from time import time

from pyload.plugin.Account import Account


class NetloadIn(Account):
    __name    = "NetloadIn"
    __type    = "account"
    __version = "0.22"

    __description = """Netload.in account plugin"""
    __license     = "GPLv3"
    __authors     = [("RaNaN", "RaNaN@pyload.org"),
                       ("CryNickSystems", "webmaster@pcProfil.de")]


    def loadAccountInfo(self, user, req):
        page = req.load("http://netload.in/index.php", get={'id': 2, 'lang': "de"})
        left = r'>(\d+) (Tag|Tage), (\d+) Stunden<'
        left = re.search(left, page)
        if left:
            validuntil = time() + int(left.group(1)) * 24 * 60 * 60 + int(left.group(3)) * 60 * 60
            trafficleft = -1
            premium = True
        else:
            validuntil = None
            premium = False
            trafficleft = None
        return {"validuntil": validuntil, "trafficleft": trafficleft, "premium": premium}


    def login(self, user, data, req):
        page = req.load("http://netload.in/index.php", None,
                        {"txtuser": user, "txtpass": data['password'], "txtcheck": "login", "txtlogin": "Login"},
                        cookies=True)
        if "password or it might be invalid!" in page:
            self.wrongPassword()