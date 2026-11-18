# ROS2 DockerLab

ROS 2 Humble için Docker tabanlı, tek komutla açılan bir geliştirme ortamı ve bu ortamda
çalışan örnek bir paket (`turtle_patrol`).

## Problem ve kullanıcı

**Problem:** ROS 2 her Ubuntu sürümüne yalnızca bir dağıtımla bağlıdır. Humble Ubuntu 22.04'e,
Jazzy 24.04'e bağlıdır. Dersler ve örnek kodlar çoğunlukla Humble'a göre hazırlanır, ama öğrencilerin
bilgisayarında farklı bir Ubuntu ya da farklı bir ROS sürümü kurulu olur. Doğru sürümü kurmak
saatler alır, host sistemi bozabilir ve "bende çalışıyordu" sorunlarına yol açar.

**Çözüm:** Bu depo, host'ta hangi sürüm kurulu olursa olsun `make build && make up` ile aynı
ROS 2 Humble ortamını açar. Kaynak kod host'ta durur ve konteynere bağlanır. GUI araçları
(turtlesim, rviz) host ekranında çalışır. `turtle_patrol` paketi bu ortamda yazılıp test
edilmiş, kendi kodunuz için başlangıç noktası olarak kullanabileceğiniz bir örnektir.

**Kimin için:**
- ROS 2 öğrenen ve kurulumla uğraşmak istemeyen öğrenciler
- Herkesin aynı ortamda çalışmasını isteyen ders yürütücüleri ve laboratuvar sorumluları
- Host'ta Jazzy kullanırken Humble projelerini de çalıştırması gereken geliştiriciler

## İş takip panosu

Geliştirme GitHub Projects panosunda kart bazlı takip edilir:
**[ROS2 DockerLab Panosu](https://github.com/users/soykuvvetberat34/projects/7)**

- Sütunlar: **Yapılacak → Devam Ediyor → Tamamlandı**
- Kart metinleri ve kabul kriterleri: [docs/kartlar.md](docs/kartlar.md)
- Her kart ayrı bir `feature/<no>-<ad>` branch'inde geliştirilir ve `Closes #N` içeren bir PR ile kapanır.

## Gereksinimler

- Linux (Ubuntu 22.04/24.04 üzerinde denendi) ve X11 masaüstü oturumu
- Docker Engine 24+ ve Docker Compose v2 (`docker compose`)
- GNU Make
- Host'ta ROS 2 kurulu olması **gerekmez**. Kuruluysa da (ör. Jazzy) çakışmaz, çünkü
  konteyner `ROS_DOMAIN_ID=42` kullanır.

## Çalıştırma

```bash
git clone https://github.com/soykuvvetberat34/ros2-dockerlab.git
cd ros2-dockerlab
make build      # imajı derle (ilk sefer birkaç dakika sürer)
make up         # konteyneri arka planda başlat
make shell      # konteynerde bash aç (ROS ortamı hazır)
make down       # işin bitince konteyneri kapat
```

Tüm komutları görmek için `make help` yazın.

## Özellik 1: Docker ile ROS 2 Humble ortamı

Kart: [#1](https://github.com/soykuvvetberat34/ros2-dockerlab/issues/1)

`osrf/ros:humble-desktop` tabanlı imaj, host'taki `ros2_ws/` klasörünü konteynerde
`/ros2_ws` olarak bağlar. Kodu host'ta istediğiniz editörle yazıp konteynerde derleyebilirsiniz.
GUI uygulamaları X11 üzerinden host ekranında açılır.

**Nasıl denenir:**

```bash
make check       # ROS_DISTRO=humble ve /ros2_ws içeriğini yazdırır
make turtlesim   # turtlesim penceresi host ekranında açılır (Ctrl+C ile kapatın)
```

Mount'u denemek için: host'ta `touch ros2_ws/deneme.txt`, ardından `make check`.
Dosya konteyner listesinde görünür.

## Özellik 2: turtle_patrol paketi (kare devriye)

Kart: [#2](https://github.com/soykuvvetberat34/ros2-dockerlab/issues/2)

`patrol` düğümü `/turtle1/pose` konusunu dinler ve `/turtle1/cmd_vel` konusuna hız komutu
yayınlar. Başlangıç pozundan karenin dört köşesini hesaplar. Her köşede önce yerinde döner,
sonra düz ilerler. Tur bitince durur. Geometri ve kontrol mantığı ROS'tan bağımsız
`geometry.py` modülündedir, bu yüzden birim testiyle doğrulanabilir.

| Parametre       | Varsayılan | Açıklama                   |
|-----------------|-----------:|----------------------------|
| `side_length`   | 3.0        | Kare kenarı (turtlesim birimi) |
| `linear_speed`  | 1.5        | En yüksek ileri hız        |
| `angular_speed` | 1.5        | En yüksek dönüş hızı       |
| `laps`          | 1          | Tur sayısı                 |

**Nasıl denenir:**

```bash
make test                     # paketi derler, birim + stil testlerini çalıştırır
make patrol                   # turtlesim açılır, kaplumbağa kare çizer ve durur
make patrol SIDE=2.0 LAPS=2   # daha küçük kare, iki tur
```

## Proje yapısı

```
ros2-dockerlab/
├── Dockerfile               # ROS 2 Humble + colcon + test araçları
├── docker-compose.yml       # ros2_ws mount'u ve X11 yönlendirmesi
├── Makefile                 # build / up / shell / turtlesim / test / patrol / stop
├── docs/kartlar.md          # Pano kartları ve kabul kriterleri
├── scripts/create_board.sh  # Kartlardan issue açıp panoya ekler
└── ros2_ws/src/turtle_patrol/
    ├── turtle_patrol/
    │   ├── geometry.py      # Kare köşeleri ve hız hesabı (saf Python)
    │   └── patrol_node.py   # ROS 2 düğümü
    ├── launch/patrol.launch.py
    └── test/                # birim, flake8, pep257 testleri
```
