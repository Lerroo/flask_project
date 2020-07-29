#1 Определение полной информации о ЦП средствами Python
import psutil
import cpuinfo
import requests
import json

def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    info.pop('flags')
    return info


if __name__ == "__main__":
    metric_v = get_cpu_info()
    j_dict = {'data':metric_v}
    url = 'http://localhost:5000/api/machine/58/metric'
    token = '1646875ea2344fbb809adbcb32570b04'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(j_dict), headers=headers, auth=(token, 'mybasicpass'))
    print(r.text)
    print(r)
