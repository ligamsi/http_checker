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

def check_host(host, count):
    print(f"\nПроверяем {host}")

    times = []
    success = 0
    failed = 0
    errors = 0

    for i in range(count):
        try:
            start = time.perf_counter()
            response = requests.get(host, timeout=5)
            elapsed = time.perf_counter() - start
            times.append(elapsed)

            if response.status_code == 200:
                success += 1
            elif 400 <= response.status_code < 600:
                failed += 1

            print(f"Запрос {i + 1}: {response.status_code} ({elapsed:.3f} сек)")

        except requests.RequestException as e:
            errors += 1
            print(f"Запрос {i + 1}: {e}")

    print(f"\nСтатистика для {host}")
    print(f"Success: {success}")
    print(f"Failed: {failed}")
    print(f"Errors: {errors}")

    if times:
        print(f"Min: {min(times):.3f} сек")
        print(f"Max: {max(times):.3f} сек")
        print(f"Avg: {sum(times) / len(times):.3f} сек")