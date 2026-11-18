"""turtle_patrol.geometry için birim testleri."""

import math

import pytest

from turtle_patrol.geometry import compute_command, normalize_angle, square_waypoints


def close(a, b, tol=1e-9):
    return abs(a - b) < tol


def test_normalize_angle_range():
    for angle in (0.0, 3.5, -3.5, 7.0, -10.0, 100.0):
        result = normalize_angle(angle)
        assert -math.pi <= result < math.pi
        assert close(math.sin(result), math.sin(angle), 1e-9)
        assert close(math.cos(result), math.cos(angle), 1e-9)


def test_square_has_four_corners_and_closes():
    pts = square_waypoints(5.0, 5.0, 0.0, 2.0)
    assert len(pts) == 4
    expected = [(7.0, 5.0), (7.0, 7.0), (5.0, 7.0), (5.0, 5.0)]
    for (x, y), (ex, ey) in zip(pts, expected):
        assert close(x, ex, 1e-9) and close(y, ey, 1e-9)


def test_square_sides_equal_side_length():
    side = 3.0
    pts = [(1.0, 1.0)] + square_waypoints(1.0, 1.0, 0.7, side)
    for a, b in zip(pts, pts[1:]):
        assert close(math.dist(a, b), side, 1e-9)


def test_square_rejects_non_positive_side():
    with pytest.raises(ValueError):
        square_waypoints(0.0, 0.0, 0.0, 0.0)


def test_command_turns_in_place_when_facing_wrong_way():
    linear, angular, reached = compute_command(0.0, 0.0, 0.0, (0.0, 1.0), 1.0, 1.0)
    assert not reached
    assert linear == 0.0
    assert angular > 0.0


def test_command_moves_forward_when_aligned():
    linear, angular, reached = compute_command(0.0, 0.0, 0.0, (2.0, 0.0), 1.0, 1.0)
    assert not reached
    assert close(linear, 1.0)
    assert close(angular, 0.0)


def test_command_reports_reached_at_target():
    assert compute_command(1.0, 1.0, 0.0, (1.0, 1.005), 1.0, 1.0) == (0.0, 0.0, True)


def test_simulated_patrol_draws_square():
    """Basit kinematik modelle tüm devriyeyi simüle et, köşelere varıldığını doğrula."""
    x, y, theta, dt = 5.5, 5.5, 0.0, 0.01
    waypoints = square_waypoints(x, y, theta, 3.0)
    visited = []
    for target in waypoints:
        for _ in range(10000):
            v, w, reached = compute_command(x, y, theta, target, 1.5, 1.5)
            if reached:
                visited.append((x, y))
                break
            theta += w * dt
            x += v * math.cos(theta) * dt
            y += v * math.sin(theta) * dt
        else:
            pytest.fail(f'{target} hedefine ulaşılamadı')
    for (vx, vy), (tx, ty) in zip(visited, waypoints):
        assert math.hypot(vx - tx, vy - ty) < 0.05
