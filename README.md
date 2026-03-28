# MOAR Mini-Project

This repository contains reproduction and failure analysis of the MOAR optimizer within the DocETL.

Due to regional constraints in Mainland China, this project was adapted to run on my **local Windows laptop**. These constraints include strict billing policies that prohibit mainland credit card payments for the official OpenAI API, compounded by network access restrictions and the lack of a proxy-enabled Linux server. To bypass the payment and network hurdles, I utilized the **OpenRouter API** as a unified endpoint.

## Environment Reproduction

The environment was built using `Anaconda3` on Windows. Follow these steps to reproduce the setup:

### 1. Create the conda environment

```
conda create -n docetl_env python=3.10
conda activate docetl_env
```

### 2. Install DocETL

```
pip install docetl[parsing]
```

### 3.  Windows path compatibility fix

The DocETL source code contains a hard-coded Linux-style path separator for moar optimizer, which will cause a crush on Windows when generating Pareto frontier graph. 

In order to run MOAR optimizer on Windows, you should modify the source code in your local environment:

1. Locate `ParetoFrontier.py` in your site-packages (e.g., `anaconda3\envs\docetl_env\Lib\site-packages\docetl\moar\ParetoFrontier.py`)
2. Change **Line 321**(Original code):
    ```
    graph_dir = str(new_node.yaml_file_path).rsplit("/", 1)[0] + "/graph/"
    ```
3. To this:
   ```
   graph_dir = os.path.join(os.path.dirname(str(new_node.yaml_file_path)), "graph")
   ```

### 4. API key configuration

Since official OpenAI payments are restricted, this project route all OpenAI API calls through OpenRouter.

Every reproducible folder contains contains a `.env` file. To run the benchmarks, simply open the `.env` file in the respective folder and replace the placeholder with your own OpenRouter API key:

```
OPENAI_API_KEY=your_openrouter_api_key_here
OPENAI_API_BASE=https://openrouter.ai/api/v1
```

## Run the benchmarks

To run any of the benchmarks in this repository, navigate to the specific folder.

A custom Python runner `run_moar.py` is included to handle execution. Because MOAR internally defaults to Azure OpenAI credentials for certain operations, this script forcefully patches the LiteLLM configurations to route all Azure-bound requests through the OpenRouter API key instead.

### Example: Running the reproduce scenario 1

```
cd reproduce_moar/1
python run_moar.py
```

Check the generated `results/moar_optimization` to see the results.

For these two simple benchmark tasks in the `reproduce_moar` directory, MOAR successfully discovered optimal pipelines that only rely on synthesized Python code. By completely eliminating the need for downstream LLM inferences during execution, MOAR achieved a $0 execution cost for these scenarios.