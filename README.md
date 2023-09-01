## Cultural Artifact Mapping

This repo hosts the code to run experiments to analyze how LLMs are able to understand and map cultural artifacts accurately.


### CREATE ENVIRONMENT
Create the `culture` conda environment by running the `create_env.py`

Activate the environment by running `conda activate culture`


### ENVIRONMENT VARIABLES
Set the below environment variables in the .env file

* `OPENAI_API_KEY`
* `HF_TOKEN`

Also, export the `PYTHONPATH` variable so that all the packages can work correctly. To add `PYTHONPATH`, write this command on your terminal: `export PYTHONPATH=$PYTHONPATH:<path to cultural_artifacts>`

*Note*
Make sure that you apply for an access to Llama 2 model. Also, we use HuggingFace to download the llama2 model. Ensure that you use the same email id as the one that you used to apply for the access to the llama 2 model. Generate the `HF_TOKEN` and then store it in the `.env` file