docker rm -f gpt-discord-bots && \
    docker run --restart=always \
    -v "$PWD:/gpt-discord-bots/" \
    -w /gpt-discord-bots \
    --name gpt-discord-bots -it python:3.9-slim-bullseye \
    bash
