import argparse
import requests
import time
import re
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    "-H",
    "--hosts",
    help="Список хостов"
)

group.add_argument(
    "-F",
    "--file",
    help="Путь к файлу со списком хостов"
)

parser.add_argument(
    "-C",
    "--count",
    type=int,
    default=1,
    help="Количество запросов"
)

parser.add_argument(
    "-O",
    "--output",
    help="Файл с результатом"
)

output_file = None

def output(text):
    if output_file:
        print(text, file=output_file)
    else:
        print(text)

def check_host(host, count):
    output(f"\nПроверяем {host}")

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

            output(f"Запрос {i + 1}: {response.status_code} ({elapsed:.3f} сек)")

        except requests.RequestException as e:
            errors += 1
            output(f"Запрос {i + 1}: Ошибка ({e})")

    output(f"\nСтатистика для {host}:")
    output(f"Success: {success}")
    output(f"Failed: {failed}")
    output(f"Errors: {errors}")

    if times:
        output(f"Min: {min(times):.3f} сек")
        output(f"Max: {max(times):.3f} сек")
        output(f"Avg: {sum(times) / len(times):.3f} сек")

args = parser.parse_args()

if args.output:
    try:
        output_file = open(args.output, "w", encoding="utf-8")
    except OSError:
        parser.error(f"Не удалось открыть файл '{args.output}'")

if args.count <= 0:
    parser.error("Количество запросов должно быть больше нуля")

if args.hosts:
    hosts = args.hosts.split(",")
else:
    try:
        with open(args.file, "r") as file:
            hosts = []
            for line in file:
                host = line.strip()
                if host:
                    hosts.append(host)
    except FileNotFoundError:
        parser.error(f"Файл '{args.file}' не найден")


for host in hosts:
    if not re.fullmatch(r"https://[A-Za-z0-9.-]+\.[A-Za-z]{2,}", host):
        parser.error(f"Некорректный адрес: {host}")

with ThreadPoolExecutor() as executor:
    futures = []

    for host in hosts:
        future = executor.submit(check_host, host, args.count)
        futures.append(future)

    for future in futures:
        future.result()