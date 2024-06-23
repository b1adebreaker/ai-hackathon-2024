"""
Run batch inference jobs using face, burst, and prosody models on all YouTube videos.
Saves the unformatted predictions to raw_predictions folder.
"""

import os
import json
import numpy as np
import pandas as pd

from hume import HumeBatchClient
from hume.models.config import FaceConfig, BurstConfig, ProsodyConfig

from dotenv import load_dotenv
load_dotenv()
HUME_API_KEY = os.environ['HUME_API_KEY']


def get_video_paths(video_path='video_paths.json'):
    with open(video_path, 'r') as file:
        data = json.load(file)
        filepaths = [item['video_path'] for item in data]
    return filepaths


def get_model_configs():
    configs = {
        "face": FaceConfig(fps_pred=1),
        "burst": BurstConfig(),
        "prosody": ProsodyConfig()
    }
    return configs


def run_all_batches(filepaths):
    configs = get_model_configs()
    json_results = {}

    for config_name, config in configs.items():
        batch_result = run_single_batch(config_name, config, filepaths)
        json_results[config_name] = batch_result

    return json_results


def run_single_batch(config_name, config, filepaths):
    client = HumeBatchClient(HUME_API_KEY)
    job = client.submit_job(None, [config], files=filepaths)

    print(job)
    print("Running...")

    details = job.await_complete()
    job.download_predictions(f"raw_predictions/{config_name}_predictions.json")
    print(f"Predictions downloaded to raw_predictions/{config_name}_predictions.json")
    result = job.get_predictions()
    
    return result


def main():
    try:
        filepaths = get_video_paths()
        run_all_batches(filepaths)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()