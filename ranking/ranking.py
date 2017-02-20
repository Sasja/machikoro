#!/usr/bin/env python
import json

class Ranking:
    def __init__(self, fn):
        self.fn = fn
        with open(self.fn, "a+") as f:
            try:
                self.data = json.load(f)
            except:
                self.data = {}
    def _save(self):
        with open(self.fn, "w+") as f:
            json.dump(self.data, f)
    def addEntry(self, url, branch, commit, score):
        entryId = str(abs(hash((url,branch,commit))))
        self.data[entryId] = {
                "url":url,
                "branch":branch,
                "commit":commit,
                "score":score
            }
        self._save()
    def getEntryId(self, url, branch, commit):
        matches = [entryId for entryId,e in self.data.items() if (
                e["url"] == url
            and e["branch"] == branch
            and e["commit"] == commit )]
        assert len(matches) == 1
        return matches[0]
    def updateScore(self, entryId, newScore):
        self.data[entryId]["score"] = newScore
        self._save()
    def getRanking(self):
        ranking = sorted(self.data.values(), key=lambda x: x["score"], reverse=True)
        return [(i["score"],
                 i["url"] + "_" + i["branch"] + "_" + i["commit"][:10])
                for i in ranking]
