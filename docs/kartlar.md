# Pano Kartları

Bu dosya GitHub Projects panosundaki kartların kaynağıdır. `scripts/create_board.sh`
her `## Kart` başlığını ayrı bir issue olarak açar ve panoya "Yapılacak" durumunda ekler.

## Kart 1: Docker ile ROS 2 Humble geliştirme ortamı

**Kullanıcı hikâyesi:** Bir öğrenci olarak, bilgisayarımda hangi ROS 2 sürümü kurulu olursa olsun
tek komutla ROS 2 Humble ortamı açabilmek istiyorum, böylece kurulumla uğraşmadan derse odaklanabilirim.

**Kapsam:**
- `osrf/ros:humble-desktop` tabanlı Dockerfile
- `ros2_ws` klasörünü konteynere bağlayan docker-compose.yml
- Sık kullanılan komutlar için Makefile (`build`, `up`, `shell`, `down`, `turtlesim`)
- GUI uygulamaları için X11 yönlendirmesi

**Kabul kriterleri:**
- [ ] `make build` hatasız tamamlanıyor
- [ ] `make up` sonrası konteynerde `echo $ROS_DISTRO` komutu `humble` döndürüyor
- [ ] Host'taki `ros2_ws/` klasörü konteynerde `/ros2_ws` olarak görünüyor; bir tarafta oluşturulan dosya diğer tarafta da görünüyor
- [ ] `make turtlesim` ile turtlesim penceresi host ekranında açılıyor

## Kart 2: turtle_patrol paketi (kare devriye)

**Kullanıcı hikâyesi:** Bir öğrenci olarak, kaplumbağanın konum geri beslemesiyle kare çizerek
devriye gezdiği bir örnek paket görmek istiyorum, böylece publisher/subscriber, parametre ve
launch kavramlarını çalışan bir kod üzerinde inceleyebilirim.

**Kapsam:**
- `ament_python` tipinde `turtle_patrol` paketi
- `/turtle1/pose` dinleyip `/turtle1/cmd_vel` yayınlayan `patrol` düğümü
- `side_length`, `linear_speed`, `angular_speed`, `laps` parametreleri
- turtlesim ve devriye düğümünü birlikte başlatan launch dosyası
- ROS'tan bağımsız birim testleri ve stil testleri

**Kabul kriterleri:**
- [ ] `make test` çalıştırıldığında tüm testler geçiyor
- [ ] `make patrol` ile kaplumbağa ekranda kare çiziyor ve tur bitince duruyor
- [ ] `side_length` parametresi değiştirildiğinde kare boyutu değişiyor

## Kart 3: GitHub Actions ile sürekli entegrasyon

**Kullanıcı hikâyesi:** Bir geliştirici olarak, her PR'da Docker imajının derlenip testlerin
otomatik çalışmasını istiyorum, böylece bozuk kod main'e girmesin.

**Kabul kriterleri:**
- [ ] `.github/workflows/ci.yml` her push ve PR'da çalışıyor
- [ ] İş akışı Docker imajını derleyip `make test` ile aynı testleri koşuyor
- [ ] Test başarısız olursa PR'da kırmızı durum görünüyor
- [ ] README'ye CI durum rozeti ekleniyor

## Kart 4: Farklı devriye şekilleri

**Kullanıcı hikâyesi:** Bir öğrenci olarak, kaplumbağanın kare dışında başka düzgün çokgenler de
çizebilmesini istiyorum, böylece geometri ile kontrol kodu arasındaki ilişkiyi deneyebilirim.

**Kabul kriterleri:**
- [ ] `sides` parametresi eklendi (varsayılan 4); 3 ile üçgen, 6 ile altıgen çiziliyor
- [ ] Yeni ara nokta hesabı için birim testleri yazıldı ve geçiyor
- [ ] README'de farklı şekillerin nasıl çizdirileceği anlatılıyor

## Kart 5: Docker imajını GitHub Container Registry'de yayınlama

**Kullanıcı hikâyesi:** Bir öğrenci olarak, imajı kendim derlemek yerine hazır imajı indirmek
istiyorum, böylece yavaş bilgisayarda dakikalarca derleme beklemem.

**Kabul kriterleri:**
- [ ] main'e her merge'de imaj `ghcr.io/soykuvvetberat34/ros2-dockerlab` adresine gönderiliyor
- [ ] İmaj public ve `docker pull` ile giriş yapmadan indirilebiliyor
- [ ] docker-compose.yml hazır imajı kullanacak şekilde güncellendi ve README'de anlatıldı
