import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from kfp.v2 import compiler, dsl
from kfp.v2.dsl import Dataset, Model, Input, Output


@dsl.component(
    base_image="python:3.9",
    target_image="asia-northeast1-docker.pkg.dev/vertex-pipelines-20241020/repositry/training_pipeline:v1.0.0",
)
def train_and_evaluate_model(
    X_train_data: Input[Dataset],
    X_test_data: Input[Dataset],
    y_train_data: Input[Dataset],
    y_test_data: Input[Dataset],
    output_model: Output[Model],
):
    # 入力データの読み込み
    X_train = np.load(X_train_data.path)
    X_test = np.load(X_test_data.path)
    y_train = np.load(y_train_data.path)
    y_test = np.load(y_test_data.path)

    # モデルのトレーニング
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 評価
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")

    # モデルの保存
    model_path = f"{output_model.path}.pkl"
    pd.to_pickle(model, model_path)
    output_model.uri = model_path


if __name__ == "__main__":
    pass
