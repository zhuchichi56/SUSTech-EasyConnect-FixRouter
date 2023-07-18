import subprocess
from concurrent.futures import ThreadPoolExecutor

def delete_gateway_route(subnet):
    subprocess.run(['sudo', 'route', 'delete', subnet])

def delete_gateway_routes(gateways, num_processes=10):
    process = subprocess.Popen(['netstat', '-rn'], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    routes = output.decode('utf-8').splitlines()
    cut_gateway_routes = [route for route in routes if len(route.split()) >= 4]
    gateway_routes = [route for route in cut_gateway_routes if route.split()[1] in gateways]

    # 使用多线程删除路由表项
    with ThreadPoolExecutor(max_workers=num_processes) as executor:
        executor.map(delete_gateway_route, [route.split()[0] for route in gateway_routes])

    # 增加对应vpn的路由，本人要访问的机器是10.xxx.xxx.xxx，所以能访问了
    subprocess.run(['sudo', 'route', '-n', 'add', '-net', '10.0.0.0/8', '10.21.144.10'])

if __name__ == "__main__":
    gateway_to_delete = ['10.21.144.10', '10.21.144.11']
    delete_gateway_routes(gateway_to_delete)
