import docker

client = docker.from_env()

container = client.containers.run("machitest", detach = True)

print container
for line in container.logs(stream = True):
    print line

    container.stop()
