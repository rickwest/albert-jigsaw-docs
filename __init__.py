# -*- coding: utf-8 -*-

"""Search the Jigsaw Documentation"""

from os import path
import urllib.parse
import html
from algoliasearch.search_client import SearchClient

from albertv0 import *

__iid__ = "PythonInterface/v0.2"
__prettyname__ = "Jigsaw Docs"
__version__ = "0.1.0"
__trigger__ = "jig "
__author__ = "Rick West"
__dependencies__ = ["algoliasearch"]


client = SearchClient.create("BH4D9OD16A", "57a7f5b1e4e0a44c7e2f8e96abcbf674")
index = client.init_index("jigsaw")


icon = "{}/icon.svg".format(path.dirname(__file__))
google_icon = "{}/google.png".format(path.dirname(__file__))


def getSubtitles(hit):
    hierarchy = hit["hierarchy"]

    subtitles = []
    for x in range(2, 6):
        if hierarchy["lvl" + str(x)] is not None:
            subtitles.append(hierarchy["lvl" + str(x)])

    return subtitles


def sortByLevel(el):
    return el["hierarchy"]["lvl0"]


def handleQuery(query):
    items = []

    if query.isTriggered:

        if not query.isValid:
            return

        if query.string.strip():
            search = index.search(query.string, {"hitsPerPage": 5})

            hits = search["hits"]

            if len(hits) is not 0:
                hits.sort(key=sortByLevel)

            for hit in hits:

                if len(getSubtitles(hit)) is not 0:
                    subtitle = "[{}] - {}".format(
                        hit["hierarchy"]["lvl0"], " » ".join(getSubtitles(hit))
                    )
                else:
                    subtitle = "[{}]".format(hit["hierarchy"]["lvl0"])

                items.append(
                    Item(
                        id=__prettyname__,
                        icon=icon,
                        text=html.unescape(hit["hierarchy"]["lvl1"]),
                        subtext=html.unescape(subtitle),
                        actions=[
                            UrlAction("Open in the Jigsaw Documentation", hit["url"])
                        ],
                    )
                )

            if len(items) == 0:
                term = "tighten jigsaw {}".format(query.string)

                google = "https://www.google.com/search?q={}".format(
                    urllib.parse.quote(term)
                )

                items.append(
                    Item(
                        id=__prettyname__,
                        icon=google_icon,
                        text="Search Google",
                        subtext='No match found. Search Google for: "{}"'.format(term),
                        actions=[UrlAction("No match found. Search Google", google)],
                    )
                )

                items.append(
                    Item(
                        id=__prettyname__,
                        icon=icon,
                        text="Open Docs",
                        subtext="No match found. Open jigsaw.tighten.co/docs...",
                        actions=[
                            UrlAction(
                                "Open the Jigsaw Documentation",
                                "https://jigsaw.tighten.co/docs",
                            )
                        ],
                    )
                )

        else:
            items.append(
                Item(
                    id=__prettyname__,
                    icon=icon,
                    text="Open Docs",
                    subtext="Open jigsaw.tighten.co/docs...",
                    actions=[
                        UrlAction(
                            "Open the Jigsaw Documentation", "https://jigsaw.tighten.co/docs"
                        )
                    ],
                )
            )

    return items
