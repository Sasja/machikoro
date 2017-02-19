#!/usr/bin/env python
import docker

client = docker.from_env()

class ContainedAi:
    def __init__(self, port):
        self.port = port
    def deploy(self):
        self.container = client.containers.run(
            "machitest",
            detach = True,
            ports={1337:self.port}
            )
    def destroy(self):
        self.container.kill()
