"""Collision helpers for player movement and interaction."""


def rects_overlap(ax, ay, aw, ah, bx, by, bw, bh):
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def can_move(px, py, pw, ph, dx, dy, obstacles, map_w, map_h):
    nx, ny = px + dx, py + dy
    if nx < 0 or ny < 0 or nx + pw > map_w or ny + ph > map_h:
        return False, px, py
    for obs in obstacles:
        if rects_overlap(nx, ny, pw, ph, obs["x"], obs["y"], obs["w"], obs["h"]):
            return False, px, py
    return True, nx, ny


def nearest_interactable(px, py, pw, ph, interactables, radius):
    cx, cy = px + pw / 2, py + ph / 2
    best, best_dist = None, radius + 1
    for obj in interactables:
        if obj.get("triggered"):
            continue
        ox = obj["x"] + obj["w"] / 2
        oy = obj["y"] + obj["h"] / 2
        dist = ((cx - ox) ** 2 + (cy - oy) ** 2) ** 0.5
        if dist <= radius and dist < best_dist:
            best, best_dist = obj, dist
    return best


def player_center(px, py, pw, ph):
    return px + pw / 2, py + ph / 2
