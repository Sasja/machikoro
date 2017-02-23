#!/usr/bin/env python
import json
import os.path
import simpleflock

class Ranking:
    def __init__(self, fn):
        self.fn = fn
        self._lockfn = ".machilock"
        if os.path.isfile(fn):
            with open(fn, "r") as f:
                data = json.load(f)
        else:
            with open(fn, "w") as f:
                json.dump({},f)

    def addEntry(self, url, branch, commit, score):
        with simpleflock.SimpleFlock(self._lockfn):
            entryId = str(abs(hash((url,branch,commit))))
            with open(self.fn, "r") as f:
                data = json.load(f)
            data[entryId] = {
                    "url":url,
                    "branch":branch,
                    "commit":commit,
                    "score":score }
            with open(self.fn, "w") as f:
                json.dump(data, f)

    def getEntryId(self, url, branch, commit):
        with simpleflock.SimpleFlock(self._lockfn):
            with open(self.fn, "r") as f: data = json.load(f)
            matches = [entryId for entryId,e in data.items() if (
                    e["url"] == url
                and e["branch"] == branch
                and e["commit"] == commit )]
            assert len(matches) == 1
            return matches[0]

    def updateScore(self, data, entryId, newScore):
        with simpleflock.SimpleFlock(self._lockfn):
            with open(self.fn, "r") as f:
                data = json.load(f)
            data[entryId]["score"] = newScore
            with open(self.fn, "w") as f:
                json.dump(data, f)

    def getRanking(self):
        with simpleflock.SimpleFlock(self._lockfn):
            with open(self.fn, "r") as f:
                data = json.load(f)
            ranking = sorted(data.values(), key=lambda x: x["score"], reverse=True)
            print(ranking)
            return "\n".join([
                "{: <8} | {: <53} | {: <23} | {: <13}".format(
                    str(i["score"])[:5],
                    i["url"][:50],
                    i["branch"][:20],
                    i["commit"][:10]
                    )
                for i in ranking])
