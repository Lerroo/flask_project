import psutil
import cpuinfo
import requests
import json
import click


def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    info.pop('flags')
    return info


def post_json_metric(token, url):
    j_dict = {'data':get_cpu_info()}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    return requests.post(url, data=json.dumps(j_dict), headers=headers, auth=(token, 'mybasicpass'))


# python3 metrics_requests\(1\).py http://localhost:5000/api/machine/1/metric -t f65b9d7f527e4ea78a33021b987d7c3e
@click.command()
@click.argument('url')
@click.option('--auth-token', '-t')
def main(auth_token, url):
    answer = post_json_metric(auth_token, url)
    print(answer.text)
    print(answer.ok)


if __name__ == "__main__":
    main()