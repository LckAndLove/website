# ---- Stage 1: Build ----
# 使用 Node.js 镜像作为构建环境
# node:20-alpine 是一个轻量级的 Node.js 镜像
FROM node:20-alpine AS build

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json (或 yarn.lock)
# 这样可以利用 Docker 的层缓存机制，只有在依赖变化时才重新安装
COPY package*.json ./

# 安装项目依赖
RUN npm install

# 复制所有项目文件到工作目录
COPY . .

# 运行构建命令，生成静态文件
RUN npm run build

# ---- Stage 2: Production ----
# 使用 Nginx 作为一个非常轻量级的 Web 服务器来托管静态文件
FROM nginx:1.27-alpine

# 将构建阶段生成的静态文件（位于 /app/dist）复制到 Nginx 的默认网站目录
COPY --from=build /app/dist /usr/share/nginx/html

# ---- Stage 2: Production ----
# 使用 Nginx 作为一个非常轻量级的 Web 服务器来托管静态文件
FROM nginx:1.27-alpine

# 将构建阶段生成的静态文件（位于 /app/dist）复制到 Nginx 的默认网站目录
COPY --from=build /app/dist /usr/share/nginx/html

# 删除 Nginx 的默认配置
RUN rm /etc/nginx/conf.d/default.conf

# 复制我们自定义的 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d

# 暴露 80 端口（Nginx 默认端口）
EXPOSE 80

# 当容器启动时，Nginx 会自动在前台运行