#!/usr/bin/env python3
"""convex_hull - Convex hull algorithms (Graham scan, Jarvis march, Andrew's monotone chain).

Usage: python convex_hull.py [--algo graham|jarvis|monotone] [--random N]
"""
import sys, math, random

def cross(O, A, B):
    return (A[0]-O[0])*(B[1]-O[1]) - (A[1]-O[1])*(B[0]-O[0])

def graham_scan(points):
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts
    pivot = min(pts, key=lambda p: (p[1], p[0]))
    pts.remove(pivot)
    def angle_key(p):
        return (math.atan2(p[1]-pivot[1], p[0]-pivot[0]),
                (p[0]-pivot[0])**2 + (p[1]-pivot[1])**2)
    pts.sort(key=angle_key)
    hull = [pivot]
    for p in pts:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)
    return hull

def jarvis_march(points):
    pts = list(set(points))
    if len(pts) <= 1:
        return pts
    start = min(pts, key=lambda p: (p[1], p[0]))
    hull = []
    current = start
    while True:
        hull.append(current)
        candidate = pts[0]
        for p in pts[1:]:
            if candidate == current:
                candidate = p
                continue
            c = cross(current, candidate, p)
            if c < 0 or (c == 0 and
                ((p[0]-current[0])**2+(p[1]-current[1])**2) >
                ((candidate[0]-current[0])**2+(candidate[1]-current[1])**2)):
                candidate = p
        current = candidate
        if current == start:
            break
    return hull

def monotone_chain(points):
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts
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

def hull_area(hull):
    n = len(hull)
    if n < 3: return 0.0
    area = 0.0
    for i in range(n):
        j = (i+1) % n
        area += hull[i][0]*hull[j][1] - hull[j][0]*hull[i][1]
    return abs(area) / 2.0

def main():
    algo = "monotone"
    n = 20
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--algo" and i+1 < len(args):
            algo = args[i+1]; i += 2
        elif args[i] == "--random" and i+1 < len(args):
            n = int(args[i+1]); i += 2
        else:
            i += 1
    points = [(random.randint(-100,100), random.randint(-100,100)) for _ in range(n)]
    print(f"Points ({n}): {points[:10]}{'...' if n>10 else ''}")
    algos = {"graham": graham_scan, "jarvis": jarvis_march, "monotone": monotone_chain}
    fn = algos.get(algo, monotone_chain)
    hull = fn(points)
    print(f"Algorithm: {algo}")
    print(f"Hull ({len(hull)} vertices): {hull}")
    print(f"Area: {hull_area(hull):.2f}")

if __name__ == "__main__":
    main()
