# AWS free-tier deployment

This deployment runs the React frontend, FastAPI API, Postgres, and Redis on one EC2 instance with Docker Compose. It is intended for a personal demo or low-traffic project, not production trading.

## 1. Create the EC2 instance

1. Open the AWS EC2 console in the region you want to use.
2. Launch Ubuntu Server 24.04 LTS on an instance type marked free-tier eligible in your account. `t2.micro` or `t3.micro` is usually enough for a demo, but eligibility depends on your account and AWS region.
3. Use at least 20 GB of gp3 root storage.
4. Create or select a key pair and download the `.pem` file.
5. In the security group, allow:
   - SSH (TCP 22) from **My IP only**
   - HTTP (TCP 80) from `0.0.0.0/0`
6. Do not expose ports 5432 or 6379.

AWS free-tier rules and prices change. Check the EC2 pricing page and billing dashboard before launching, and set an AWS Budget alert.

## 2. Install Docker and clone the app

SSH into the instance, then run:

```bash
sudo apt update
sudo apt install -y ca-certificates curl git
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker "$USER"
newgrp docker
git clone https://github.com/Jashnoor-gill/QuantOS.git
cd QuantOS
cp .env.example .env
```

Generate values for `.env` and edit it:

```bash
openssl rand -base64 32
openssl rand -base64 48
nano .env
```

Set `POSTGRES_PASSWORD` and `SECRET_KEY` to the generated values. Set `APP_ORIGIN` to `http://YOUR_EC2_PUBLIC_IP`.

## 3. Start the stack

```bash
docker compose up -d --build
docker compose ps
curl http://localhost/api/health
```

Open `http://YOUR_EC2_PUBLIC_IP` in a browser. API documentation is available at `http://YOUR_EC2_PUBLIC_IP/api/docs`.

## 4. Updates and logs

```bash
cd QuantOS
git pull
docker compose up -d --build
docker compose logs -f --tail=100
```

The database and Redis data are stored in Docker volumes. Back up the Postgres volume before making important changes. An Elastic IP is recommended if you need the public address to remain stable after stopping and starting the instance.

## HTTPS and domain names

For a public site, point a domain's DNS A record at the instance and put an HTTPS reverse proxy such as Caddy in front of this stack. HTTP on port 80 is enough to verify the free-tier deployment, but it should not be used for real credentials or trading activity.