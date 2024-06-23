import json
import pandas as pd


def extract_face_data(predictions_json_path, model_type='face'):

    with open(predictions_json_path, 'r') as f:
        data = json.load(f)
    
    all_files_data = {}

    for file_data in data:
        file_name = file_data['source']['filename']
        try:
            predictions = file_data['results']['predictions'][0]['models'][model_type]['grouped_predictions'][0]['predictions']
        except (IndexError, KeyError):
            # Handle the case where predictions are empty or the structure is not as expected
            all_files_data[file_name] = {}
            continue
        
        face_data = pd.DataFrame(predictions)
        
        if not face_data.empty:
            emotions = [d['name'] for d in face_data['emotions'][0]]
            emotions_data = pd.DataFrame(face_data['emotions'].to_list(), columns=emotions)

            for emotion in emotions:
                emotions_data[emotion] = pd.json_normalize(emotions_data[emotion])['score']
            
            face_data = face_data.join(emotions_data)
            
            # Calculate the average score for each emotion
            average_emotions = emotions_data.mean().to_dict()

            # Determine the top emotion
            top_emotion = max(average_emotions, key=average_emotions.get)
            average_emotions['top_emotion'] = top_emotion
            
            # Store the average emotions data in the dictionary
            all_files_data[file_name] = average_emotions
        else:
            all_files_data[file_name] = {}

    return all_files_data


def save_results_to_json(data, output_json_path):
    with open(output_json_path, 'w') as f:
        json.dump(data, f, indent=4)


def main():
    try:
        models = ["face", "burst", "prosody"]

        for model in models:
            predictions_json_path = f"raw_predictions/{model}_predictions.json"
            output_json_path = f"final_predictions/final_{model}_predictions.json"
            average_predictions = extract_face_data(predictions_json_path, model)
            save_results_to_json(average_predictions, output_json_path)
            print(average_predictions)
            
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()