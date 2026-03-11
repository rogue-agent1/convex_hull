#!/usr/bin/env python3
"""Convex hull — Graham scan and gift wrapping algorithms."""
import sys, math, random

def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def graham_scan(points):
    pts = sorted(set(points))
    if len(pts) <= 2: return pts
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

def gift_wrap(points):
    pts = list(set(points))
    if len(pts) <= 2: return pts
    start = min(pts)
    hull = [start]; current = start
    while True:
        next_pt = pts[0]
        for p in pts[1:]:
            c = cross(current, next_pt, p)
            if next_pt == current or c > 0 or (c == 0 and
                math.dist(current, p) > math.dist(current, next_pt)):
                next_pt = p
        if next_pt == start: break
        hull.append(next_pt); current = next_pt
    return hull

def hull_area(hull):
    n = len(hull)
    return abs(sum(hull[i][0]*hull[(i+1)%n][1] - hull[(i+1)%n][0]*hull[i][1] for i in range(n))) / 2

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    random.seed(42)
    points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]
    hull = graham_scan(points)
    print(f"Points: {n}, Hull vertices: {len(hull)}")
    print(f"Area: {hull_area(hull):.1f}")
    for i, (x, y) in enumerate(hull):
        print(f"  {i}: ({x:.1f}, {y:.1f})")
