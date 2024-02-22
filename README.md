# DOSA: A Dataset of Social Artifacts from Different Indian Geographical Subcultures

This repo hosts the code to run experiments on the **DOSA** dataset.


## Create Environment

Create the `culture` conda environment by running the `create_env.py`

Activate the environment by running `conda activate culture`


## Environment Variables

Set the below environment variables in the .env file

* `OPENAI_API_KEY`
* `HF_TOKEN`

Also, export the `PYTHONPATH` variable so that all the packages can work correctly. To add `PYTHONPATH`, write this command on your terminal: `export PYTHONPATH=$PYTHONPATH:<path to cultural_artifacts>`

*Note*
Make sure that you apply for an access to Llama 2 model. Also, we use HuggingFace to download the llama2 model. Ensure that you use the same email id as the one that you used to apply for the access to the llama 2 model. Generate the `HF_TOKEN` and then store it in the `.env` file

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
