import subprocess
from concurrent.futures import ThreadPoolExecutor
from collections import Counter

def delete_gateway_route(subnet):
    subprocess.run(['sudo', 'route', 'delete', subnet])


def find_most_common_element(lst):
    counter = Counter(lst)
    most_common_element, _ = counter.most_common(1)[0]
    return most_common_element


def delete_gateway_routes(num_processes=10):
    process = subprocess.Popen(['netstat', '-rn'], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    routes = output.decode('utf-8').splitlines()
    cut_gateway_routes = [route for route in routes if len(route.split()) >= 4]
    gateway_routes_name = [route.split()[1] for route in cut_gateway_routes]
    gateway =find_most_common_element(gateway_routes_name)
    gateway_routes = [route for route in cut_gateway_routes if route.split()[1] == gateway]


    # 使用多线程删除路由表项
    with ThreadPoolExecutor(max_workers=num_processes) as executor:
        executor.map(delete_gateway_route, [route.split()[0] for route in gateway_routes])

    # 增加对应vpn的路由，本人要访问的机器是10.xxx.xxx.xxx，所以能访问了
    subprocess.run(['sudo', 'route', '-n', 'add', '-net', '10.0.0.0/8', gateway])


    #运行'netstat', '-rn' 并在终端输出结果
    subprocess.run(['netstat', '-rn'])



if __name__ == "__main__":
    delete_gateway_routes()

