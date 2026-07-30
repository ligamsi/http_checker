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

    for i in range(args.count):
        start = time.perf_counter()
        response = requests.get(host)
        finish = time.perf_counter()
        elapsed = finish - start

        print(f"Запрос {i + 1}: {response.status_code} ({elapsed:.3f} сек)")