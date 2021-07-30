from __future__ import annotations

import requests
import re
import json
import sys
from typing import List
from dataclasses import dataclass

@dataclass(frozen=True)
class Vid:
    q240: str = None
    q480: str = None
    q720: str = None
    q1080: str = None

    @classmethod
    def highest(cls, obj: Vid):
        if obj.q1080: return obj.q1080
        elif obj.q720: return obj.q720
        elif obj.q480: return obj.q480
        elif obj.q240: return obj.q240
        else: return None

class PronDownloader:
    def __init__(self, url):
        self.url = url

    def parseUrl(self, url) -> List[dict]:
        response: str = requests.get(url).text
        data = response.split(";")

        for var in data:
            if "qualityItems" in var:
                data = json.loads(re.sub("var qualityItems\w+ = ", '', var))
                break
        return data

    def phDownloader(self):
        urls = self.parseUrl(self.url)

        pron = Vid(
            q240=urls[0]["url"],
            q480=urls[1]["url"],
            q720=urls[2]["url"],
            q1080=urls[3]["url"],
        )
        return Vid.highest(pron)
