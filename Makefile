SERVICE := ros2
COMPOSE := docker compose
# Terminal yoksa (CI, betik) TTY isteme
TTY     := $(shell [ -t 0 ] || echo -T)
ROS_ENV := source /opt/ros/humble/setup.bash; [ -f /ros2_ws/install/setup.bash ] && source /ros2_ws/install/setup.bash;
EXEC    := $(COMPOSE) exec $(TTY) $(SERVICE) bash -c

.PHONY: help build up down shell check xhost turtlesim

help: ## Komutları listele
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-10s %s\n", $$1, $$2}'

build: ## Docker imajını derle
	$(COMPOSE) build

up: ## Konteyneri arka planda başlat
	$(COMPOSE) up -d

down: ## Konteyneri durdur ve sil
	$(COMPOSE) down

shell: up ## Konteynerde bash aç
	$(COMPOSE) exec $(SERVICE) bash

check: up ## ROS sürümünü ve workspace bağlantısını göster
	$(EXEC) '$(ROS_ENV) echo "ROS_DISTRO=$$ROS_DISTRO"; ls -la /ros2_ws'

xhost:
	@xhost +local:root >/dev/null 2>&1 || echo "Uyarı: xhost çalışmadı, GUI açılmayabilir."

turtlesim: up xhost ## Turtlesim penceresini aç
	$(EXEC) '$(ROS_ENV) ros2 run turtlesim turtlesim_node'
