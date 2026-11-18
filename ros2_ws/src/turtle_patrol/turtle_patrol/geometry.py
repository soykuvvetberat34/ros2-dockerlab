"""ROS'tan bağımsız geometri ve kontrol yardımcıları (birim test edilebilir)."""

import math


def normalize_angle(angle):
    """Açıyı [-pi, pi) aralığına getir."""
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


def square_waypoints(x0, y0, theta0, side):
    """
    Başlangıç pozundan sola dönerek çizilen karenin 4 köşesini döndür.

    Son köşe başlangıç noktasıdır; böylece kare kapanır.
    """
    if side <= 0:
        raise ValueError('side pozitif olmalı')
    points = []
    x, y, heading = x0, y0, theta0
    for _ in range(4):
        x += side * math.cos(heading)
        y += side * math.sin(heading)
        points.append((x, y))
        heading += math.pi / 2.0
    return points


def compute_command(x, y, theta, target, linear_speed, angular_speed,
                    angle_tolerance=0.02, distance_tolerance=0.02):
    """
    Hedefe gitmek için (doğrusal, açısal) hız ve hedefe varıldı mı bilgisini döndür.

    Önce yerinde döner, yön doğruysa düz ilerler. Böylece köşeler keskin olur.
    """
    dx = target[0] - x
    dy = target[1] - y
    distance = math.hypot(dx, dy)
    if distance < distance_tolerance:
        return 0.0, 0.0, True

    error = normalize_angle(math.atan2(dy, dx) - theta)
    if abs(error) > angle_tolerance:
        angular = math.copysign(min(angular_speed, 4.0 * abs(error)), error)
        return 0.0, angular, False

    linear = min(linear_speed, 2.0 * distance)
    return linear, 2.0 * error, False
