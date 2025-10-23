FROM node:22-alpine

RUN apk update && apk upgrade && apk add --no-cache && rm -rf /var/cache/apk/*

ENV PORT=3000

COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
EXPOSE ${PORT}
CMD ["npm", "start"]