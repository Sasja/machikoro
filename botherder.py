#!/usr/bin/env python
import docker

client = docker.from_env()

class ContainedAi:
    def __init__(self):
        pass
    def deploy(self):
        self.container = client.containers.run(
            "machitest",
            detach = True,
            ports={1337:1234}
            )
    def destroy(self):
        self.container.kill()






#    print container
#    for line in container.logs(stream = True):
#        print line
