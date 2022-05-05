# Credit Card Fraud Detection - Backend

Running serverless on GCP

Flask application which can predict if a given credit card transaction string is a fraud or not with 97% recall. Utilizes a pickeled Neural Network `storedModel.pckl` develped and described [here](https://www.kaggle.com/code/jdelamorena/recall-97-by-using-undersampling-neural-network).

```
git clone https://github.com/Alirvah/GCP_frontend.git
cd GCP_frontend
gcloud run deploy
```

Please use automatically generated Cloud Run URL from this project as an API source URL for [Frontend part](https://github.com/Alirvah/GCP_frontend).

![image](https://user-images.githubusercontent.com/37639059/166879038-6cc0e23c-d88a-4cfd-a09c-c9bdf32b2c16.png)

