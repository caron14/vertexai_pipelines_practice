import os
import sys
from typing import NamedTuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from kfp.v2 import compiler, dsl
from kfp.v2.dsl import Output, Artifact

current_dir_path = os.path.abspath('./')
sys.path.append(current_dir_path)
from modules import generate_data


@dsl.component(
    base_image="python:3.9",
    target_image="asia-northeast1-docker.pkg.dev/vertex-pipelines-20241020/repositry/training_pipeline:v1.0.0",
)
def preprocessing(
    X_train_output: Output[Artifact],
    X_test_output: Output[Artifact],
    y_train_output: Output[Artifact],
    y_test_output: Output[Artifact],
):
    # データ生成
    X, y = generate_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 各出力ファイルを保存
    np.save(X_train_output.path + ".npy", X_train)
    np.save(X_test_output.path + ".npy", X_test)
    np.save(y_train_output.path + ".npy", y_train)
    np.save(y_test_output.path + ".npy", y_test)

    # スキーマ情報を設定
    X_train_output.metadata["schema_title"] = "system.Array"
    X_train_output.metadata["schema_version"] = "0.0.1"
    X_test_output.metadata["schema_title"] = "system.Array"
    X_test_output.metadata["schema_version"] = "0.0.1"
    y_train_output.metadata["schema_title"] = "system.Array"
    y_train_output.metadata["schema_version"] = "0.0.1"
    y_test_output.metadata["schema_title"] = "system.Array"
    y_test_output.metadata["schema_version"] = "0.0.1"

    return (X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    pass
