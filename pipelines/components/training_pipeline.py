from datetime import datetime
import os
import sys

from kfp.v2 import compiler, dsl
# from kfp.v2.google.client import AIPlatformClient
from google.cloud import aiplatform

# from google_cloud_pipeline_components import aiplatform as gcc_aip

current_dir_path = os.path.abspath("./")
sys.path.append(current_dir_path)
from pipelines.components.preprocess.preprocess import preprocessing
from pipelines.components.train.train import train_and_evaluate_model


PROJECT_ID = None
REGION = None


@dsl.pipeline(
    name="training-pipeline",
    description="Vertex AI Piplines sample",
    pipeline_root=f"gs://vertex-pipelines-20241020-bucket/",
)
def pipeline(
    project_id: str = "project-id",
    location: str = "us-central1",
    dataset_path: str = "project-id.dataset",
):
    prepro_comp = preprocessing()
    train_comp = train_and_evaluate_model(
        X_train_data=prepro_comp.outputs["X_train_output"],
        X_test_data=prepro_comp.outputs["X_test_output"],
        y_train_data=prepro_comp.outputs["y_train_output"],
        y_test_data=prepro_comp.outputs["y_test_output"],
    )


# if __name__ == "__main__":
pipeline_filename = "training_pipeline.json"
compiler.Compiler().compile(
    pipeline_func=pipeline,
    package_path=pipeline_filename,
)

PROJECT_ID = "vertex-pipelines-20241020" if PROJECT_ID is None else PROJECT_ID
REGION = "asia-northeast1" if REGION is None else REGION

import vertexai
vertexai.init(
    project=PROJECT_ID, 
    location=REGION,
)
# Run
## パイプライン ジョブを定義します。
TIMESTAMP = datetime.now().strftime("%Y%m%d%H%M%S")
job = aiplatform.PipelineJob(
    display_name="hello-world-pipeline",
    template_path="training_pipeline.json",
    job_id="hello-world-pipeline-{0}".format(TIMESTAMP),
    enable_caching=True,
)

# ジョブを実行して新しいパイプライン実行を作成します。
job.submit()
