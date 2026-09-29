FROM nginx:1.29-alpine

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY start-gateway.sh /usr/local/bin/start-gateway

USER nginx

ENTRYPOINT ["/usr/local/bin/start-gateway"]
