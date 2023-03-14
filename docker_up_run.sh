docker rm -f discord
docker run -v "$PWD/src:/gpt-discord-bot/" -d \
        --name discord -it gpt-discord-bots
<<<<<<< Updated upstream
=======
docker logs discord -f
>>>>>>> Stashed changes
