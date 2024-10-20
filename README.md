# vertexai_pipelines_practice
Code tips for practice of Vertex Pipelines

# Environment setup
## Python environment setup
### Create an Virtual Environment
The procedure of setting up a virtual environment is the following, where name_of_venv is the name of the virtual environment.  
In general, we set name_of_venv as 'venv'.
```sh
$ python -m venv <venv name>
$ source <venv name>/bin/activate
```

Note that the command to deactivate the virtual environment is below.
```sh
$ deactivate
```
### Install the Necessary Libraries
```sh
$ pip install --upgrade pip
$ pip install -r requirements-dev.txt
$ pip install -r requirements-test.txt
$ pip install -r requirements.txt
```

## Cloud environment setup
Run the following command in Cloud Shell to confirm that the gcloud command knows about your project.
```sh
gcloud config list project
```

Set the PROJECT you will use with this command:
```sh
gcloud config set project <PROJECT_ID>
```

Set the compute region/zone with the following commands:
```sh
gcloud config set compute/region asia-northeast1
gcloud config set compute/zone asia-northeast1-a
```

**
```sh
gcloud auth application-default login
```

### Step 2: Enable APIs
Run this command to give your project access to the Compute Engine, Container Registry, and Vertex AI services:
```sh
gcloud services enable compute.googleapis.com         \
                       containerregistry.googleapis.com  \
                       aiplatform.googleapis.com  \
                       cloudbuild.googleapis.com \
                       cloudfunctions.googleapis.com
```

### Step 3: Create a Cloud Storage Bucket
To run a training job on Vertex AI, we'll need a storage bucket to store our saved model assets. The bucket needs to be regional. In this demo, we're using asia-northeast1. If you already have a bucket you can skip this step.

Run the following commands in your Cloud Shell terminal to create a bucket:
```sh
BUCKET_NAME=gs://$GOOGLE_CLOUD_PROJECT-bucket
gsutil mb -l asia-northeast1 $BUCKET_NAME
```

Next we'll give our compute service account access to this bucket. This will ensure that Vertex Pipelines has the necessary permissions to write files to this bucket. Run the following command to add this permission:
```sh
gcloud projects describe $GOOGLE_CLOUD_PROJECT > project-info.txt
PROJECT_NUM=$(cat project-info.txt | sed -nre 's:.*projectNumber\: (.*):\1:p')
SVC_ACCOUNT="${PROJECT_NUM//\'/}-compute@developer.gserviceaccount.com"
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member serviceAccount:$SVC_ACCOUNT --role roles/storage.objectAdmin
```

# Note
## Symbolic link

```sh
ln -s <original-file PATH> <symbolic file name>
```
Ex. The symbolic file "runtime-requirements.txt" linling to "requirements.txt" will be created in the current directory.
```sh
ln -s ~/vertexai_pipelines_practice/requirements.txt runtime-requirements.txt
```
