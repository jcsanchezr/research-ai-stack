FROM node:24-bookworm-slim

ARG DSH_VERSION=0.1.5-rc.1

RUN npm install -g "@deepseek-ai/dsh@${DSH_VERSION}" \
    && npm cache clean --force

RUN mkdir -p /workspace /home/node/.dsh \
    && chown -R node:node /workspace /home/node

USER node
WORKDIR /workspace

ENTRYPOINT ["sleep"]
CMD ["infinity"]
