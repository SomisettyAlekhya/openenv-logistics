
---
title: OpenEnv Logistics Delivery Environment
emoji: 🚚
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "1.0"
python_version: "3.10"
app_file: server/app.py
pinned: false
---

# Logistics Delivery Optimization OpenEnv

This OpenEnv simulates a simple **delivery logistics optimization problem**.

An AI agent must choose actions to reduce pending orders while considering vehicle capacity and traffic conditions.

## Observation Space
- pending_orders (int)
- vehicle_capacity (int)
- traffic_level (0=low,1=medium,2=high)

## Action Space
- dispatch
- reroute
- delay

## Reward Logic
- Completing deliveries increases reward
- High traffic penalizes dispatch
- Efficient routing gives partial rewards

Reward range is always between **0.0 – 1.0**.

## Tasks
- easy_task → clear deliveries
- medium_task → manage traffic
- hard_task → optimize dispatch + rerouting

## Run locally

docker build -t openenv-env .
docker run -p 7860:7860 openenv-env

