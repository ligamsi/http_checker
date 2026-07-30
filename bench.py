import argparse
import requests
import time

parser = argparse.ArgumentParser()

parser.add_argument(
    "-H",
    "--hosts",
    help="Список хостов"
)

parser.add_argument(
    "-C",
    "--count",
    type=int,
    default=1,
    help="Количество запросов"
)

args = parser.parse_args()
hosts = args.hosts.split(",")

for host in hosts:
    print(f"\nПроверяем {host}")
    times = []

    for i in range(args.count):
        start = time.perf_counter()
        response = requests.get(host)
        finish = time.perf_counter()
        elapsed = finish - start
        times.append(elapsed)

        print(f"Запрос {i + 1}: {response.status_code} ({elapsed:.3f} сек)")
        print(f"\nСтатистика для {host}")

        print(f"Min: {min(times):.3f}")
        print(f"Max: {max(times):.3f}")
        print(f"Avg: {sum(times) / len(times):.3f}")