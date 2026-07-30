import argparse

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
    print(host)