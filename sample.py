"""
Ref.
    * https://codelabs.developers.google.com/vertex-pipelines-intro
    * https://zenn.dev/cloud_ace/articles/mlops-bigframes-vertex-ai-pipelines
    * https://future-architect.github.io/articles/20230213a/
    * https://tech.layerx.co.jp/entry/2023/11/16/185944#%E8%BE%9B%E3%81%84%E3%83%9D%E3%82%A4%E3%83%B3%E3%83%88
"""

# Step 2: Set your project ID and bucket
import os
PROJECT_ID = ""

# Get your Google Cloud project ID from gcloud
if not os.getenv("IS_TESTING"):
    shell_output=!gcloud config list --format 'value(core.project)' 2>/dev/null
    PROJECT_ID = shell_output[0]
    print("Project ID: ", PROJECT_ID)

#  create a variable to store your bucket name.
BUCKET_NAME="gs://" + PROJECT_ID + "-bucket"

# Step 3: Import libraries
import kfp

from kfp.v2 import compiler, dsl
from kfp.v2.dsl import component, pipeline, Artifact, ClassificationMetrics, Input, Output, Model, Metrics

from google.cloud import aiplatform
from google_cloud_pipeline_components import aiplatform as gcc_aip
from typing import NamedTuple

# Step 4: Define constants
## パイプラインを構築する前に行う必要がある最後の作業は、いくつかの定数を定義することです。
## PIPELINE_ROOT は、パイプラインによって作成されたアーティファクトが書き込まれる Cloud Storage パスです。
## ここではリージョンとして us-central1 を使用しますが、バケットの作成時に別のリージョンを使用した場合は、次のコードの REGION 変数を更新します。
PATH=%env PATH
%env PATH={PATH}:/home/jupyter/.local/bin
REGION="us-central1"

PIPELINE_ROOT = f"{BUCKET_NAME}/pipeline_root/"
print(PIPELINE_ROOT)

# Note:
## After running the code above, you should see the root directory for your pipeline printed. 
## This is the Cloud Storage location where the artifacts from your pipeline will be written. 
## It will be in the format of gs://YOUR-BUCKET-NAME/pipeline_root/

# 5. Creating your first pipeline
# * How to create custom components in the KFP SDK
# * How to run and monitor a pipeline in Vertex Pipelines

# Step 1: Create Python notebook and install libraries
@component(base_image="python:3.9", output_component_file="first-component.yaml")
def product_name(text: str) -> str:
    return text

@component(packages_to_install=["emoji"])
def emoji(
    text: str,
) -> NamedTuple(
    "Outputs",
    [
        ("emoji_text", str),  # Return parameters
        ("emoji", str),
    ],
):
    import emoji

    emoji_text = text
    emoji_str = emoji.emojize(':' + emoji_text + ':', language='alias')
    print("output one: {}; output_two: {}".format(emoji_text, emoji_str))
    return (emoji_text, emoji_str)

@component
def build_sentence(
    product: str,
    emoji: str,
    emojitext: str
) -> str:
    print("We completed the pipeline, hooray!")
    end_str = product + " is "
    if len(emoji) > 0:
        end_str += emoji
    else:
        end_str += emojitext
    return(end_str)


# ステップ 3: コンポーネントをパイプラインへとまとめる
@pipeline(
    name="hello-world",
    description="An intro pipeline",
    pipeline_root=PIPELINE_ROOT,
)

# You can change the `text` and `emoji_str` parameters here to update the pipeline output
def intro_pipeline(text: str = "Vertex Pipelines", emoji_str: str = "sparkles"):
    product_task = product_name(text)
    emoji_task = emoji(emoji_str)
    consumer_task = build_sentence(
        product_task.output,
        emoji_task.outputs["emoji"],
        emoji_task.outputs["emoji_text"],
    )

# ステップ 4: パイプラインをコンパイルして実行する
compiler.Compiler().compile(
    pipeline_func=intro_pipeline, package_path="intro_pipeline_job.json"
)

## 次に、TIMESTAMP 変数を作成します。これをジョブ ID に使用します。
from datetime import datetime

TIMESTAMP = datetime.now().strftime("%Y%m%d%H%M%S")

## パイプライン ジョブを定義します。
job = aiplatform.PipelineJob(
    display_name="hello-world-pipeline",
    template_path="intro_pipeline_job.json",
    job_id="hello-world-pipeline-{0}".format(TIMESTAMP),
    enable_caching=True
)

# ジョブを実行して新しいパイプライン実行を作成します。
job.submit()
















