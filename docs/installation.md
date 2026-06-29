# Installation

## Prerequisites

-   Docker
-   Docker Compose

## Clone the repository

``` bash
git clone https://github.com/vheikkiniemi/SmartNodes
cd SmartNodes
cp .env.example .env
```

Edit the `.env` file to match your environment.

## Start the platform

``` bash
docker compose up -d --build
```

Verify the services:

``` bash
docker compose ps
```

Stop the platform:

``` bash
docker compose down
```
