# brew install libportaudio2
import asyncio
from hume import HumeStreamClient
from hume.models.config import LanguageConfig

text = "tomato"

import numpy as np

async def detect_greenwashing_likelihood(text, weights):
    """
    Calculates the likelihood of greenwashing (0-100) based on emotion scores and weights.

    Args:
        emotion_scores: List of dictionaries with 'name' and 'score' keys.
        weights: Dictionary with weights for each emotion cluster (0-1).

    Returns:
        Integer representing the likelihood of greenwashing (0-100).
    """
    client = HumeStreamClient("fOMYuyoKp0MLMGMHCCfycSydi1A1T4SikmXJauWWTcStW56j")
    config = LanguageConfig()
    async with client.connect([config]) as socket:
        result = await socket.send_text(text)
        emotion_scores = result["language"]["predictions"][0]["emotions"]

    cluster_scores = {
        'positive_spin': 0,
        'negative_defensive': 0,
    }

    for emotion in emotion_scores:
      print(emotion)
      name = emotion['name']
      score = emotion['score']

      if name in ['Admiration', 'Adoration', 'Aesthetic Appreciation', 'Enthusiasm', 'Joy', 'Pride', 'Satisfaction', 'Surprise (positive)']:
          cluster_scores['positive_spin'] += score
      elif name in ['Annoyance', 'Anxiety', 'Awkwardness', 'Confusion', 'Contempt', 'Disappointment', 'Disgust', 'Distress', 'Fear', 'Guilt', 'Shame']:
          cluster_scores['negative_defensive'] += score

    # Calculate weighted scores and normalize to 0-100
    weighted_positive = cluster_scores['positive_spin'] * weights['positive_spin']
    weighted_negative = cluster_scores['negative_defensive'] * weights['negative_defensive']
    total_weighted_score = weighted_positive + weighted_negative

    likelihood = int(100 * total_weighted_score / (weights['positive_spin'] + weights['negative_defensive']))
    return min(likelihood, 100)  # Cap likelihood at 100%

# Example Usage (Adjust weights based on your analysis)
weights = {
    'positive_spin': 0.6,  # Example weight, emphasizing positive spin
    'negative_defensive': 0.4,  # Example weight
}

"""What kind of green personality do you have?"""

import numpy as np

async def detect_greenwashing_profile(text):
    """
    Detects a psychological profile (1-10) indicative of greenwashing or greenhushing tendencies,
    based on emotion scores tailored to these specific deceptive behaviors.

    Args:
        emotion_scores: List of dictionaries with 'name' and 'score' keys.

    Returns:
        Integer representing the psychological profile (1-10).
    """
    client = HumeStreamClient("fOMYuyoKp0MLMGMHCCfycSydi1A1T4SikmXJauWWTcStW56j")
    config = LanguageConfig()
    async with client.connect([config]) as socket:
      result = await socket.send_text(text)
      emotion_scores = result["language"]["predictions"][0]["emotions"]

    cluster_scores = {
        'greenwasher': 0,            # Exaggerated positivity, deflecting criticism, avoiding responsibility
        'greenhushing_defensive': 0, # Discomfort, guilt, defensiveness about lack of action
        'genuinely_sustainable': 0,  # Genuine pride, satisfaction, openness about sustainability efforts
        'apathetic': 0,             # Boredom, indifference, lack of concern about environmental issues
        'skeptical': 0,             # Confusion, doubt, uncertainty about green claims
        'eco-anxious': 0,           # Anxiety, fear, distress about environmental problems
        'critical': 0,              # Contempt, disapproval, disgust towards unsustainable practices
        'aspiring_sustainable': 0,  # Desire, craving, envy for sustainable products/practices
        'idealistic': 0,            # Romance, adoration, overly optimistic about sustainability
        'eco-sad': 0,               # Sadness, disappointment, pain about environmental harm
    }

    for emotion in emotion_scores:
        name = emotion['name']
        score = emotion['score']

        if name in ['Admiration', 'Adoration', 'Enthusiasm', 'Ecstasy', 'Triumph']:
            cluster_scores['greenwasher'] += score
        elif name in ['Annoyance', 'Awkwardness', 'Confusion', 'Contempt', 'Disgust', 'Fear', 'Guilt', 'Shame', 'Pain']:
            cluster_scores['greenhushing_defensive'] += score
        elif name in ['Joy', 'Contentment', 'Love', 'Pride', 'Satisfaction', 'Gratitude']:
            cluster_scores['genuinely_sustainable'] += score
        elif name in ['Boredom', 'Calmness', 'Concentration', 'Contemplation', 'Tiredness']:
            cluster_scores['apathetic'] += score
        elif name in ['Confusion', 'Doubt', 'Surprise (negative)']:
            cluster_scores['skeptical'] += score
        elif name in ['Anxiety', 'Distress', 'Fear']:
            cluster_scores['eco-anxious'] += score
        elif name in ['Contempt', 'Disapproval', 'Disgust']:
            cluster_scores['critical'] += score
        elif name in ['Desire', 'Craving', 'Envy']:
            cluster_scores['aspiring_sustainable'] += score
        elif name in ['Romance', 'Adoration', 'Love']:
            cluster_scores['idealistic'] += score
        elif name in ['Sadness', 'Disappointment', 'Pain', 'Empathic Pain', 'Sympathy']:
            cluster_scores['eco-sad'] += score

    # Determine the dominant psychological profile
    max_cluster = max(cluster_scores, key=cluster_scores.get)
    profile = list(cluster_scores.keys()).index(max_cluster) + 1

    if profile == 1:
      print("This individual may be engaged in greenwashing.")
    elif profile == 2:
        print("This individual may be greenhushing.")
    else:
        print(f"The detected green profile is: {list(cluster_scores.keys())[profile - 1]}")

    return  profile

async def main():
    likelihood = await detect_greenwashing_likelihood(text, weights)
    print(likelihood);
    # Example Usage
    profile = await detect_greenwashing_profile(text)
    print(profile)

if __name__ == "__main__":
    asyncio.run(main())