#!/usr/bin/env python
import json
import os.path

class Ranking:
    def __init__(self, fn):
        self.fn = fn
        if os.path.isfile(fn):
            with open(fn, "w+") as f:
                # test contents
                data = json.load(f)
        else:
            with open(fn, "w+") as f:
                # create empty json
                f.write("[]")
            
    def _atomicOp(self, operation, *args, **kwargs):
        with open(self.fn, "w+") as f:
            data = json.load(f)
            operation(data, *args, **kwargs)
            json.dump(data, f)

    def _getData(self):
        with open(self.fn, "w+") as f:
            data = json.load(f)
        return data

    def _addEntry(self, data, url, branch, commit, score):
        entryId = str(abs(hash((url,branch,commit))))
        data[entryId] = {
                "url":url,
                "branch":branch,
                "commit":commit,
                "score":score }

    def addEntry(self, *args, **kwargs):
        self._atomicOp(self._addEntry, *args, **kwargs)

    def getEntryId(self, url, branch, commit):
        data = self._getData()
        matches = [entryId for entryId,e in data.items() if (
                e["url"] == url
            and e["branch"] == branch
            and e["commit"] == commit )]
        assert len(matches) == 1
        return matches[0]

    def _updateScore(self, data, entryId, newScore):
        data[entryId]["score"] = newScore

    def updateScore(self, *args, **kwargs):
        self._atomicOp(self._updateScore, *args, **kwargs)

    def getRanking(self):
        data = self._getData()
        ranking = sorted(data.values(), key=lambda x: x["score"], reverse=True)
        return [(i["score"],
                 i["url"] + "_" + i["branch"] + "_" + i["commit"][:10])
                for i in ranking]
