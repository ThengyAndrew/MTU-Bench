import os
import sys
import tqdm
import requests

import MTU_processor

DOWNLOADED_DIR = os.path.join(os.path.dirname(__file__), "downloaded")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "processed")

urls = {
    "MTU-Bench":"https://raw.githubusercontent.com/MTU-Bench-Team/MTU-Bench/refs/heads/main/MTU-Eval/benchmark/",
}

download_files = {
    "MTU-Bench":[
        "M-M_eval.jsonl",
        "M-S_eval.jsonl",
        "S-M_eval.jsonl",
        "S-S_eval.jsonl",
        "OOD_eval.jsonl",
    ]
}

process_method = {
    "MTU-Bench": MTU_processor.processor,
}

def download_file(url, file_path):
    # 如果文件已存在，提示用户是否覆盖
    if os.path.exists(file_path):
        print(f"文件 {file_path[len(DOWNLOADED_DIR):]} 已存在，跳过。")
        return
    # 发起 GET 请求，打开流式下载模式
    with requests.get(url, stream=True) as response:
        response.raise_for_status()  # 若响应出错，会抛出异常

        # 根据响应头获取文件大小（字节数）
        total_size = int(response.headers.get("content-length", 0))
        block_size = 8192  # 每次读取的块大小，可根据需要调整

        # 使用 tqdm 包裹文件下载，显示进度条
        with open(file_path, "wb") as file:
            # 使用 tqdm 显示进度条，total_size 是文件总大小，block_size 是每次读取的块大小
            with tqdm.tqdm(total=total_size, unit='B', unit_scale=True, desc="开始下载 "+file_path[len(DOWNLOADED_DIR):]) as pbar:
                for data in response.iter_content(chunk_size=block_size):
                    file.write(data)
                    pbar.update(len(data))  # 更新进度条

    print("下载完成！")

def download_one_dataset(dataset_name):
    folder_path = os.path.join(DOWNLOADED_DIR, dataset_name)
    os.makedirs(folder_path, exist_ok=True)
    if isinstance(download_files[dataset_name], list):
        for name in download_files[dataset_name]:
            download_file(urls[dataset_name]+name, os.path.join(folder_path, name))
    else:
        for path, name_list in download_files[dataset_name].items():
            os.makedirs(os.path.join(folder_path, path), exist_ok=True)
            for name in name_list:
                download_file(urls[dataset_name]+path+"/"+name, os.path.join(folder_path, path, name))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "download":
        if sys.argv[2] in urls:
            download_one_dataset(sys.argv[2])
        else:
            print("你可以下载以下数据集: \n{}".format("\n".join(list(urls.keys()))))
    elif len(sys.argv) > 2 and sys.argv[1] == "process":
        if sys.argv[2] in process_method:
            os.makedirs(os.path.join(PROCESSED_DIR, sys.argv[2]), exist_ok=True)
            process_method[sys.argv[2]]()
        else:
            print("你可以处理以下数据集: \n{}".format("\n".join(list(process_method.keys()))))
    else:
        print("你可以使用以下命令: \npython {} download <DATASET_NAME>\npython {} process <DATASET_NAME>".format(
            sys.argv[0], sys.argv[0]
        ))
