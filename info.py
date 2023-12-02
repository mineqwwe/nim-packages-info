import json
import requests
import datetime
import time
import os

def get_github_repo_info(repo_url):
    # 提取仓库名称和作者
    print("repo_url: ",repo_url)
    repo_url = repo_url.rstrip("/")
    parts = repo_url.split('/')
    username = parts[-2]
    repo_name = parts[-1].split('.')[0]

    # 构建API请求URL
    api_url = f"https://api.github.com/repos/{username}/{repo_name}"

    # 发起GET请求
    print("api_url: ",api_url)
    api_key = os.environ["GET_NIM"]
    
    response = requests.get(api_url,headers={'Authorization': f'token {api_key}'})
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        # 提取更新时间和star数
        last_updated = data['updated_at']
        stars = data['stargazers_count']
        # 转换为datetime对象并返回
        update_time = datetime.datetime.strptime(
            last_updated, "%Y-%m-%dT%H:%M:%SZ")
        return update_time, stars
    else:
        # 请求失败时返回空值
        return None, None


def get_repo_info(file_path):
    repo_array = []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for repo in data:
            url = repo.get('url')
            web = repo.get('web')
            name = repo.get('name')
            description = repo.get('description')
            if url is None:
                urls = web
            else:
                urls = url
            repo_dict = {
                "name": name,
                "urls": urls,
                "description" : description
            }
            repo_array.append(repo_dict)
    return repo_array


repo_array = get_repo_info("packages.json")


import csv

# 假设repo_array是你的数据列表

# 打开一个CSV文件进行写入
with open('repo_info.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # 写入表头
    writer.writerow(["name", "stars", "update_time", "description", "urls"])
    index = 0
    # 遍历repo_array，并写入每个repo的信息
    for repo in repo_array:
        name = repo.get("name")
        # print(name)
        urls = repo.get("urls")
        description = repo.get("description")
        print("index: ",index)
        index = index + 1
        if urls is not None:
            update_time, stars = get_github_repo_info(urls)
            time.sleep(1)
        else:
            update_time = "not_get"
            stars = "not_get"      
        # 将每个repo的信息写入CSV文件
        writer.writerow([name, stars, update_time, description, urls])
