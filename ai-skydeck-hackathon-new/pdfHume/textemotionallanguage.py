# brew install libportaudio2
import asyncio
from hume import HumeStreamClient
from hume.models.config import LanguageConfig

profile_details = {
    'greenwasher': {
        'description': "This profile suggests a tendency to exaggerate positive environmental actions and deflect criticism. There may be a focus on appearing sustainable without substantial backing. Watch out for vague language, cherry-picked data, and a lack of measurable goals.",
        'towards_genuine': "Focus on transparently communicating actual environmental impact, setting realistic goals, and engaging in continuous improvement. Back up claims with data, prioritize actions over words, and seek third-party verification."
    },
    'greenhushing_defensive': {
        'description': "This profile indicates discomfort or defensiveness regarding sustainability efforts. There might be a lack of action due to fear of scrutiny or a reluctance to admit shortcomings.",
        'towards_genuine': "Acknowledge areas for improvement, openly communicate challenges, and engage stakeholders in finding solutions. Be proactive in addressing concerns, demonstrate a willingness to learn, and celebrate small victories along the way."
    },
    'genuinely_sustainable': {
        'description': "This profile reflects genuine commitment to sustainability. There's a sense of pride and openness about environmental actions, along with a willingness to share both successes and challenges.",
        'towards_genuine': "Continue setting ambitious goals, transparently report progress, and inspire others through leadership. Share best practices, collaborate with others in the industry, and advocate for systemic change."
    },
    'apathetic': {
        'description': "This profile suggests a lack of concern or interest in environmental issues. There might be indifference towards sustainability efforts or a belief that it's not a priority.",
        'towards_genuine': "Educate yourself about the environmental impact of your operations and the benefits of sustainability. Explore how sustainable practices can align with your business goals, and consider partnering with organizations that can provide guidance and support."
    },
    'skeptical': {
        'description': "This profile indicates doubt or uncertainty about green claims. There might be skepticism about the effectiveness of sustainability measures or concerns about greenwashing.",
        'towards_genuine': "Seek out credible sources of information about sustainability, look for case studies and research that demonstrate the impact of sustainable practices, and engage in dialogue with experts and stakeholders to address your concerns."
    },
    'eco-anxious': {
        'description': "This profile reflects anxiety, fear, or distress about environmental problems. There might be a sense of overwhelm or helplessness in the face of climate change and other environmental challenges.",
        'towards_genuine': "Focus on actionable steps that you can take to make a positive impact. Channel your anxiety into constructive action, join forces with others who share your concerns, and celebrate your achievements along the way."
    },
    'critical': {
        'description': "This profile suggests a critical stance towards unsustainable practices. There might be disapproval or disgust towards companies that are not taking sufficient action on environmental issues.",
        'towards_genuine': "Use your critical eye to identify areas where improvement is needed. Hold companies accountable for their environmental impact, advocate for stronger regulations and policies, and support businesses that are truly committed to sustainability."
    },
    'aspiring_sustainable': {
        'description': "This profile indicates a desire to become more sustainable, but with some uncertainty or hesitation. There might be a feeling of envy towards companies that are already further along in their sustainability journey.",
        'towards_genuine': "Set realistic goals, start with small steps, and gradually build momentum. Seek out resources and mentorship from those who have already made progress, and don't be afraid to ask for help."
    },
    'idealistic': {
        'description': "This profile reflects an overly optimistic or idealistic view of sustainability. There might be a tendency to romanticize or oversimplify the challenges involved.",
        'towards_genuine': "Ground your idealism in practical realities. Acknowledge the complexity of environmental issues, set realistic expectations, and be prepared to adapt your approach as needed."
    },
    'eco-sad': {
        'description': "This profile suggests sadness, disappointment, or pain about environmental harm. There might be a sense of grief or loss over the damage already done to the planet.",
        'towards_genuine': "Allow yourself to feel your sadness, but don't let it paralyze you. Channel your grief into action, connect with others who share your concerns, and focus on solutions and hope for the future."
    }
}

async def emotion_scores_from(text):
    client = HumeStreamClient("fOMYuyoKp0MLMGMHCCfycSydi1A1T4SikmXJauWWTcStW56j")
    config = LanguageConfig()

    chunk_size = 500
    text_chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    emotion_totals = {}  # Track total scores per emotion
    num_chunks = 0       # Count the number of processed chunks

    async with client.connect([config]) as socket:
        for chunk in text_chunks:
            result = await socket.send_text(chunk)
            for emotion_dict in result["language"]["predictions"][0]["emotions"]:
                emotion_name = emotion_dict['name']
                score = emotion_dict['score']
                emotion_totals[emotion_name] = emotion_totals.get(emotion_name, 0) + score
            num_chunks += 1  # Increment chunk counter

    # Calculate averages
    average_emotions = []
    for emotion_name, total_score in emotion_totals.items():
        average_score = total_score / num_chunks
        average_emotions.append({"name": emotion_name, "score": average_score})

    return average_emotions



async def sustainability_score_and_profile(emotion_scores, weights):
    """
    Calculates the likelihood of greenwashing (0-100) based on emotion scores and weights.

    Args:
        emotion_scores: List of dictionaries with 'name' and 'score' keys.
        weights: Dictionary with weights for each emotion cluster (0-1).

    Returns:
        Integer representing the likelihood of greenwashing (0-100).
    """
    cluster_scores = {
        'positive_spin': 0,
        'negative_defensive': 0,
    }
    score_and_profile = {}

    for emotion in emotion_scores:
      print (emotion)
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
    score_and_profile["genuinely_sustainable_score"] = min(likelihood, 100)  # Cap likelihood at 100%

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
# Determine the dominant profile and add details
    max_cluster = max(cluster_scores, key=cluster_scores.get)
    profile = max_cluster
    
    #change these to save a JSON with the text and scores
    result = {
        'profile': profile,
        'description': profile_details[profile]['description'],
        'towards_genuine': profile_details[profile]['towards_genuine']
    }
    score_and_profile["profile"] = result

    return score_and_profile

import json
import os
from pathlib import Path

# Example Usage (Adjust weights based on your analysis)
weights = {
    'positive_spin': 0.6,  # Example weight, emphasizing positive spin
    'negative_defensive': 0.4,  # Example weight
}

def convert_emotion_scores(emotion_list):
    """Converts a list of emotion dictionaries into the desired format.

    Args:
        emotion_list: A list of dictionaries, each with 'name' and 'score' keys.

    Returns:
        A list of strings, each a formatted dictionary representation.
    """
    ret = {}
    for emotion in emotion_list:
        ret[emotion['name']] = emotion['score']
    return ret


async def main():
    text_files_dir = Path("../textFiles/companies/")
    max_chars = 10000  # Limit for characters to read

    for company_dir in text_files_dir.iterdir():
        if not company_dir.is_dir():
            continue
        for report_file in company_dir.iterdir():
            if not report_file.is_file() or not report_file.suffix == ".txt":
                continue
            report_name = report_file.stem
            year = report_name.split("_")[-1]

            try:
                with open(report_file, "r") as file:
                    text = file.read(max_chars)  # Read up to max_chars

                emotion_scores = await emotion_scores_from(text)
                score_profile = await sustainability_score_and_profile(
                    emotion_scores, weights 
                )

                output_dirs = [
                    Path(f"../media/companies/{company_dir.name}"),
                    #Path(f"../score_and_profile/companies/{company_dir.name}"),
                ]
                for out_dir in output_dirs:
                    os.makedirs(out_dir, exist_ok=True)  # Create if doesn't exist
                    output_file = out_dir / f"{year}.json"

                    with open(output_file, "w") as outfile:
                        json.dump(
                            convert_emotion_scores(emotion_scores),
                            #if "emotion" in out_dir.name
                            #else score_profile,
                            outfile,
                            indent=2,
                        )
            except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
                print(
                    f"Error processing {report_file}: {e} - Skipping to the next file."
                )


if __name__ == "__main__":
    asyncio.run(main())