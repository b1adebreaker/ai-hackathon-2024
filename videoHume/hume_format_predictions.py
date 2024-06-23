import json
import pandas as pd


# def extract_face_data(predictions_json):
#     data = pd.read_json(predictions_json)
#     face_data = pd.DataFrame(data['results'][0]['predictions'][0]['models']['face']['grouped_predictions'][0]['predictions'])

#     emotions = [d['name'] for d in face_data['emotions'][0]]
#     emotions_data = pd.DataFrame(face_data['emotions'].to_list(),columns=emotions)

#     for emotion in emotions:
#         emotions_data[emotion] = pd.json_normalize(emotions_data[emotion])['score']

#     face_data = face_data.join(emotions_data)
#     face_data['top_emotion'] = face_data[emotions].idxmax(axis=1)
#     face_data.to_json()
#     return face_data