FROM node:20-slim

RUN corepack enable

WORKDIR /app

COPY package.json yarn.lock .yarnrc.yml ./
COPY .yarn .yarn

RUN yarn install --immutable

COPY . .

EXPOSE 5173

CMD ["yarn", "dev", "--host"]
