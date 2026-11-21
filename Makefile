SERVICE := ros2
COMPOSE := docker compose
# Terminal yoksa (CI, betik) TTY isteme
TTY     := $(shell [ -t 0 ] || echo -T)
ROS_ENV := source /opt/ros/humble/setup.bash; [ -f /ros2_ws/install/setup.bash ] && source /ros2_ws/install/setup.bash;
EXEC    := $(COMPOSE) exec $(TTY) $(SERVICE) bash -c

.PHONY: help build up down shell check stop xhost turtlesim colcon test patrol clean

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

# Aynı anda tek simülasyon olsun: önceki turtlesim/patrol süreçlerini kapat
stop: ## Çalışan turtlesim ve patrol süreçlerini durdur
	-@$(COMPOSE) exec -T $(SERVICE) pkill -f 'turtlesim_node|turtle_patrol|patrol.launch' >/dev/null 2>&1 || true

xhost:
	@xhost +local:root >/dev/null 2>&1 || echo "Uyarı: xhost çalışmadı, GUI açılmayabilir."

turtlesim: up stop xhost ## Turtlesim penceresini aç
	$(EXEC) '$(ROS_ENV) ros2 run turtlesim turtlesim_node'

# Konteyner root olarak çalıştığı için colcon çıktılarını host kullanıcısına geri ver
FIX_OWNER := chown -R $(shell id -u):$(shell id -g) /ros2_ws/build /ros2_ws/install /ros2_ws/log
SIDE ?= 3.0
LAPS ?= 1
SIDES ?= 4

colcon: up ## ros2_ws içindeki paketleri derle
	$(EXEC) '$(ROS_ENV) cd /ros2_ws && colcon build --symlink-install; rc=$$?; $(FIX_OWNER); exit $$rc'

test: colcon ## Paketleri test et (birim + flake8 + pep257)
	$(EXEC) '$(ROS_ENV) cd /ros2_ws && colcon test --event-handlers console_direct+; colcon test-result --verbose; rc=$$?; $(FIX_OWNER); exit $$rc'

patrol: colcon stop xhost ## Turtlesim aç, kaplumbağa çokgen çizsin (SIDES=4 SIDE=3.0 LAPS=1)
	$(EXEC) '$(ROS_ENV) source /ros2_ws/install/setup.bash && ros2 launch turtle_patrol patrol.launch.py side_length:=$(SIDE) laps:=$(LAPS) sides:=$(SIDES)'

clean: up ## colcon çıktılarını sil
	$(EXEC) 'rm -rf /ros2_ws/build /ros2_ws/install /ros2_ws/log'
