import uuid
import json
import requests
import os 
from time import sleep
from tqdm import tqdm
import threading
from random import choice

api_key = os.getenv("S2_API_KEY")
headers = {"x-api-key": api_key}
base_dir = '/mnt/ssd/data/s2'
colours = ['red', 'green', 'blue']
datasets = ['papers', 'abstracts', 'tldrs']

def get_latest_release() -> str | None:
    url = 'https://api.semanticscholar.org/datasets/v1/release'
    r = requests.get(url, headers=headers)
    if r.ok:
        body = r.json()
        return body[-1]
    else:
        raise Exception("Failed to fetch latest release")
    
def download_file(file_url, dataset_name) -> None:
    try:
        r = requests.get(file_url, stream=True)
        r.raise_for_status()
    except Exception as e:
        print(f"Failed to download {file_url}: {e}")
        return

    # Save the file
    metadata = {
        'file_url': file_url,
        'filename': f"{str(uuid.uuid4())}.gz"
    }
    file_path = os.path.join(base_dir, dataset_name, metadata['filename'])
    pbar = tqdm(
        total=int(r.headers.get('content-length', 0)),
        ascii=True, 
        desc=metadata['filename'], 
        unit_scale=True,
        unit='B',
        colour=choice(colours),
    )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar.update(len(chunk))

    # save metadata
    with open(f'{file_path}.metadata.json', 'w') as f:
        json.dump(metadata, f)

def download_dataset(dataset_name, release) -> None:
    url = f'https://api.semanticscholar.org/datasets/v1/release/{release}/dataset/{dataset_name}'
    r = requests.get(url, headers=headers)
    try:
        r.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch dataset info for {dataset_name} release {release}: {e}")
        return
    
    threads = []
    file_list = r.json()['files']
    threads = [threading.Thread(target=download_file, args=(file_url, dataset_name,)) for file_url in file_list]
    
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f"Finished downloading dataset: {dataset_name} for release: {release}")

for dataset in datasets:
    latest_release = get_latest_release()
    if latest_release:
        print(f"Downloading dataset: {dataset} for release: {latest_release}")
        download_dataset(dataset, latest_release)
        sleep(2) # rate limiting
