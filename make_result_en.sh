#!/bin/bash

python ./src/missing_values_analysis.py
python ./src/missing_values_visualize.py --lang en
python ./src/model_emotion_analysis.py
python ./src/model_emotion_statistics.py
python ./src/model_emotion_visualize.py --lang en
python ./src/model_emotion_similarity.py --lang en
python ./src/model_reason_analysis.py
python ./src/model_reason_statistics.py
python ./src/model_reason_visualize.py --lang en
python ./src/model_reason_similarity.py --lang en
python ./src/text_emotion_analysis.py
python ./src/text_emotion_statistics.py
python ./src/text_emotion_visualize.py --lang en
python ./src/text_emotion_similarity.py --lang en
python ./src/text_reason_analysis.py
python ./src/text_reason_statistics.py
python ./src/text_reason_visualize.py --lang en
python ./src/text_reason_similarity.py --lang en
python ./src/persona_emotion_analysis.py
python ./src/persona_emotion_statistics.py
python ./src/persona_emotion_visualize.py --lang en
python ./src/persona_emotion_similarity.py --lang en
python ./src/persona_reason_analysis.py
python ./src/persona_reason_statistics.py
python ./src/persona_reason_visualize.py --lang en
python ./src/persona_reason_similarity.py --lang en
python ./src/temperature_emotion_analysis.py
python ./src/temperature_emotion_statistics.py
python ./src/temperature_emotion_visualize.py --lang en
python ./src/temperature_reason_analysis.py
python ./src/temperature_reason_visualize.py --lang en