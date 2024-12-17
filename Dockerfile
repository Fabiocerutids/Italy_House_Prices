FROM python:3.11.9

WORKDIR /predict_app

COPY ./requirements_docker.txt /predict_app/requirements.txt 
RUN pip install --no-cache-dir -r requirements.txt 

COPY ./3_modelling/artifacts/refitted_lightgbm/model_05.pkl /predict_app/artifacts/
COPY ./3_modelling/artifacts/refitted_lightgbm/model_50.pkl /predict_app/artifacts/
COPY ./3_modelling/artifacts/refitted_lightgbm/model_95.pkl /predict_app/artifacts/
COPY ./3_modelling/artifacts/categorical_encoder.pkl /predict_app/artifacts/
COPY ./4_deploy_app/predict.py /predict_app/predict.py
COPY ./4_deploy_app/container_app.py /predict_app/container_app.py
COPY ./data/feature_data/abitanti.csv /predict_app/feature_data/
COPY ./data/feature_data/reddito_by_regione.csv /predict_app/feature_data/

ENTRYPOINT ["python"]

CMD ["container_app.py"]