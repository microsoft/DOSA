<div style="display: flex; align-items: center; justify-content: center;">
  <img src="dosa_image.jpeg" alt="Image description" style="width: 50px; height: 50px; margin-right: 10px;">
  <h2>
    DOSA: A Dataset of Social Artifacts from Different Indian Geographical Subcultures
  </h2>
</div>

<p align="center">
  <a href="https://lrec-coling-2024.org/"><img src="https://img.shields.io/badge/LREC_COLING-2024-blue?style=flat"></a>
  <a href="https://arxiv.org/abs/2403.14651"><img src="https://img.shields.io/badge/arxiv-2403.14651-red"></a>
  <a href="https://github.com/microsoft/DOSA/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green">
  </a>
</p>

This repo hosts the code to run experiments on the **DOSA** dataset.


## Create Environment

Create the `dosa` conda environment by running the `create_env.py`

Activate the environment by running `conda activate dosa`


## Environment Variables

Set the below environment variables in the .env file

* `OPENAI_API_KEY`
* `HF_TOKEN`

Also, export the `PYTHONPATH` variable so that all the packages can work correctly. To add `PYTHONPATH`, write this command on your terminal: `export PYTHONPATH=$PYTHONPATH:<path to cultural_artifacts>`

*Note*
Make sure that you apply for an access to Llama 2 model. Also, we use HuggingFace to download the llama2 model. Ensure that you use the same email id as the one that you used to apply for the access to the llama 2 model. Generate the `HF_TOKEN` and then store it in the `.env` file

## Citation
If you're using the dataset, or the code, then please cite it using:
```
@misc{seth2024dosa,
      title={DOSA: A Dataset of Social Artifacts from Different Indian Geographical Subcultures}, 
      author={Agrima Seth and Sanchit Ahuja and Kalika Bali and Sunayana Sitaram},
      year={2024},
      eprint={2403.14651},
      archivePrefix={arXiv},
      primaryClass={cs.CY}
}

``` 

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

## Data License

Please refer to our data license [here](DATA_LICENSE.md).

## Privacy

You can read more about Microsoft's privacy statement [here](https://privacy.microsoft.com/en-us/privacystatement).
