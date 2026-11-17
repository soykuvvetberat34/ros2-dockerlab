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
**<PANO_LINKI_BURAYA>**

- Sütunlar: **Yapılacak → Devam Ediyor → Tamamlandı**
- Kart metinleri ve kabul kriterleri: [docs/kartlar.md](docs/kartlar.md)
- Her kart ayrı bir `feature/<no>-<ad>` branch'inde geliştirilir ve `Closes #N` içeren bir PR ile kapanır.
