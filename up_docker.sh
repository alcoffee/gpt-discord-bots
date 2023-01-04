docker rm -f gpt-discord-bots
docker run --restart=always -d \
    -v "$PWD:/gpt-discord-bots/" \
    -w /gpt-discord-bots \
    --name gpt-discord-bots -it python:3.9-slim-bullseye bash
docker exec -it gpt-discord-bots bash
