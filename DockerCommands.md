Jupyter Notebook

podman build -t pytorch-jupyter -f docker/Dockerfile .
podman run -p 8888:8888 -v $(pwd):/workspace:Z pytorch-jupyter

Navigate to:
http://localhost:8888/notebooks/Bot-Helper.ipynb#

If you installed toolkit and wish to use GPU:

podman run --hooks-dir=/usr/share/containers/oci/hooks.d --gpus all -p 8888:8888 -v $(pwd):/workspace:z pytorch-jupyter

Streamlit Interface

podman build -t pytorch-jupyter-app -f appDocker/Dockerfile .
podman run --user root -p 8501:8501 -p 5000:5000 -v $(pwd):/usr/src/app:Z -v $(pwd)/nltk_data:/root/nltk_data -v $(pwd)/data:/usr/src/app/data:Z pytorch-jupyter-app

Navigate to:
http://localhost:8501/
