FROM continuumio/miniconda3:4.8.2

RUN apt-get update -y; apt-get upgrade -y; apt-get install -y vim-tiny vim-athena



# Always save your environments in a conda env file. 
# This makes it so much easier to fix your environment when you inadvertantly clobber it
#COPY (Relative to project) (/root)
COPY environment.yml environment.yml
RUN conda env create -f environment.yml
RUN echo "alias l='ls -lah'" >> ~/.bashrc

# This is the conda magic. If you are running through a shell just activating the environment in your profile is peachy
RUN echo "source activate proto_app" >> ~/.bashrc

# This is the equivalent of running `source activate`
# Its handy to have in case you want to run additional commands in the Dockerfile
# env > before_activate.txt
# source activate proto_app
# env > after_activate.txt
# diff before_activate.txt after_activate.txt
ENV CONDA_EXE /opt/conda/bin/conda
ENV CONDA_PREFIX /opt/conda/envs/proto_app
ENV CONDA_PYTHON_EXE /opt/conda/bin/python
ENV CONDA_PROMPT_MODIFIER (proto_app)
ENV CONDA_DEFAULT_ENV proto_appapp
ENV PATH /opt/conda/envs/proto_app/bin:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin