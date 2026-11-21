# ROS2 DockerLab

Docker içinde çalışan bir ROS 2 Humble ortamı ve bu ortamda yazdığım küçük bir örnek paket
(`turtle_patrol`).

## Neden bu proje?

ROS 2'nin her sürümü belli bir Ubuntu sürümüne bağlı. Derste Humble kullanıyoruz, Humble de
Ubuntu 22.04 istiyor. Benim bilgisayarımda ve birçok arkadaşımda farklı bir Ubuntu ya da farklı
bir ROS sürümü kurulu olduğu için ders örneklerini çalıştırmak sorun oluyordu. Doğru sürümü
kurmak uzun sürüyor ve bazen sistemi bozuyor.

Bu projede ROS 2 Humble'ı bir Docker konteynerine koydum. Bilgisayarda hangi sürüm kurulu olursa
olsun `make build` ve `make up` ile herkes aynı ortamı açabiliyor. Kodlar bilgisayarda duruyor,
konteyner sadece derleyip çalıştırıyor. Turtlesim gibi pencereli programlar da normal ekranda açılıyor.

Kimler kullanabilir:
- ROS 2 öğrenen ve kurulumla uğraşmak istemeyen öğrenciler
- Labda herkesin aynı ortamda çalışmasını isteyen hocalar ve asistanlar

## Pano

İşleri GitHub Projects'te takip ettim:
https://github.com/users/soykuvvetberat34/projects/7

Panoda "Yapılacak", "Devam Ediyor" ve "Tamamlandı" sütunları var. Kartların metinleri
[docs/kartlar.md](docs/kartlar.md) dosyasında da duruyor. Her kart için ayrı bir branch açıp
PR ile main'e birleştirdim.

## Gerekenler

- Linux (Ubuntu 24.04'te denedim)
- Docker ve Docker Compose
- make

Bilgisayarda ROS kurulu olması gerekmiyor.

## Çalıştırma

```bash
git clone https://github.com/soykuvvetberat34/ros2-dockerlab.git
cd ros2-dockerlab
make build    # imajı oluşturur, ilk seferde birkaç dakika sürüyor
make up       # konteyneri başlatır
make shell    # konteynerin içine girer
make down     # konteyneri kapatır
```

`make help` bütün komutları listeler.

## Özellik 1: Docker ile ROS 2 Humble ortamı

Kart: [#1](https://github.com/soykuvvetberat34/ros2-dockerlab/issues/1), PR: [#6](https://github.com/soykuvvetberat34/ros2-dockerlab/pull/6)

İmaj `osrf/ros:humble-desktop` üzerine kurulu. Bilgisayardaki `ros2_ws/` klasörü konteynerde
`/ros2_ws` olarak görünüyor, yani kodu istediğim editörde yazıp konteynerde derleyebiliyorum.

Denemek için:

```bash
make check       # ROS_DISTRO=humble yazmalı ve /ros2_ws içeriği listelenmeli
make turtlesim   # turtlesim penceresi açılmalı (Ctrl+C ile kapanır)
```

Klasör bağlantısını denemek için `touch ros2_ws/deneme.txt` yazıp tekrar `make check`
çalıştırın, dosya listede görünür.

## Özellik 2: turtle_patrol paketi

Kart: [#2](https://github.com/soykuvvetberat34/ros2-dockerlab/issues/2), PR: [#7](https://github.com/soykuvvetberat34/ros2-dockerlab/pull/7)

`patrol` düğümü kaplumbağanın konumunu (`/turtle1/pose`) okuyor ve ona hız komutu
(`/turtle1/cmd_vel`) gönderiyor. Başladığı yerden bir kare çizip duruyor. Köşelerde önce
dönüyor, sonra düz gidiyor. Hesaplamaları `geometry.py` dosyasına ayırdım, böylece ROS
olmadan test edebildim.

Ayarlanabilen parametreler:

| Parametre       | Varsayılan | Açıklama           |
|-----------------|-----------:|--------------------|
| `side_length`   | 3.0        | Kenar uzunluğu     |
| `linear_speed`  | 1.5        | En yüksek ileri hız |
| `angular_speed` | 1.5        | En yüksek dönüş hızı |
| `laps`          | 1          | Tur sayısı         |

Denemek için:

```bash
make test                     # testleri çalıştırır
make patrol                   # kaplumbağa kare çizer
make patrol SIDE=2.0 LAPS=2   # daha küçük kare, iki tur
```

### Ek: farklı şekiller

Kart: [#4](https://github.com/soykuvvetberat34/ros2-dockerlab/issues/4), PR: [#8](https://github.com/soykuvvetberat34/ros2-dockerlab/pull/8)

Sonradan `sides` parametresini ekledim. Kare yerine üçgen, altıgen gibi başka şekiller de
çizilebiliyor. Verilmezse 4 kabul ediliyor, yani yine kare çiziyor.

```bash
make patrol SIDES=3            # üçgen
make patrol SIDES=6 SIDE=2.0   # altıgen
```

Turtlesim ekranı küçük olduğu için kenar sayısı artınca `SIDE` değerini düşürmek gerekiyor,
yoksa kaplumbağa duvara çarpıyor.

## Dosyalar

```
ros2-dockerlab/
├── Dockerfile               # ROS 2 Humble imajı
├── docker-compose.yml       # klasör bağlantısı ve ekran ayarı
├── Makefile                 # kısa komutlar
├── docs/kartlar.md          # pano kartları
├── scripts/create_board.sh  # kartları GitHub'a issue olarak ekleyen betik
└── ros2_ws/src/turtle_patrol/
    ├── turtle_patrol/
    │   ├── geometry.py      # köşe ve hız hesapları
    │   └── patrol_node.py   # ROS 2 düğümü
    ├── launch/patrol.launch.py
    └── test/                # testler
```
