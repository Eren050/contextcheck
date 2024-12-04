![ContextCheck Logo](https://raw.githubusercontent.com/Addepto/contextcheck/main/docs/contextcheck_logo_violet.png)

# ContextCheck

A human-friendly framework for testing and evaluating LLMs, RAGs, and chatbots.

**ContextCheck** is an open-source framework designed to evaluate, test, and validate large language models (LLMs), Retrieval-Augmented Generation (RAG) systems, and chatbots. It provides tools to automatically generate queries, request completions, detect regressions, perform penetration tests, and assess hallucinations, ensuring the robustness and reliability of these systems. ContextCheck is configurable via YAML and can be integrated into continuous integration (CI) pipelines for automated testing.


## Table of Contents
- [Features](https://github.com/Addepto/contextcheck#features)
- [LLM Prompts Validation](https://github.com/Addepto/contextcheck#llm-validation-process)
     - [LLM Prompts Validation Process](https://github.com/Addepto/contextcheck#llm-prompts-validation-process)
- [Testing Prompts Across Different Models](https://github.com/Addepto/contextcheck#testing-prompts-across-different-models)
- [Installation](https://github.com/Addepto/contextcheck#installation)
  - [For Users](https://github.com/Addepto/contextcheck#for-users)
  - [For Developers](https://github.com/Addepto/contextcheck#for-developers)
- [Tutorial](https://github.com/Addepto/contextcheck#tutorial)
- [CLI Features](https://github.com/Addepto/contextcheck#cli-features)
  - [Output Test Results to Console](https://github.com/Addepto/contextcheck#output-test-results-to-console)
  - [Running in CI/CD](https://github.com/Addepto/contextcheck#running-in-cicd)
- [Contributing](https://github.com/Addepto/contextcheck#contributing)
  - [Running Tests](https://github.com/Addepto/contextcheck#running-tests)
- [Acknowledgments](https://github.com/Addepto/contextcheck#acknowledgments)
- [License](https://github.com/Addepto/contextcheck#license)


## Features

- **Simple test scenario definition** using human-readable `.yaml` files
- **Flexible endpoint configuration** for OpenAI, HTTP, and more
- **Customizable JSON request/response models**
- **Support for variables and Jinja2 templating** in YAML files
- **Response validation** options, including heuristics, LLM-based judgment, and human labeling
- **Enhanced output formatting** with the `rich` package for clear, readable displays

## LLM Prompts Validation
An LLM prompt is a specific input or query provided to a language model to generate a response based on the model's training data. ContextCheck provides an easy-to-use tool for fine-tuning and validating multiple prompts at once.

### LLM Prompts Validation Process
The prompts testing workflow consists of the following steps:

1. Choose an LLM: Select the provider and model version you want to test your prompts with.
2. Write test scenario(s).

Each test scenario requires you to:

1. Define LLM Prompts: Create the prompts you want to test.
2. Write Tests: Create test assertions that verify the effectiveness of your prompts. These tests check if the model's responses meet your expectations.
3. Execute Tests: Run your tests to see which prompts pass or fail.
4. Fine-Tune Prompts: If any tests fail, adjust your prompts and re-run the tests. Repeat this process until all tests pass or you’re satisfied with the results.

ContextCheck allows you to execute individual or batch test scenarios.

You can test your prompts using either deterministic (rule-based) metrics, LLM-based metrics, or a combination of both, depending on your needs. To better understand the available metrics and how to use them, refer to the [metrics](https://github.com/Addepto/contextcheck/blob/main/docs/docs/user_guide/metrics.md) documentation.

For technical details how to configure and write tests, refer to [How to configure test scenario](https://github.com/Addepto/contextcheck/blob/main/docs/docs/user_guide/test_scenarios.md).

## Testing Prompts Across Different Models
Based on your particular requirements, you might want check how your prompts will perform against various LLM models. Once scenario, or multiple scenarios, are ready you can switch LLM model and run tests against it.

The LLM landscape changes rapidly. When new models or model versions become available, and you want to test how they perform against your prompts, simply change test scenario configuration and execute you tests.

Note that in the case of prompt validation, not all LLM-based metrics are applicable. For example, the `hallucination/` metric requires reference documents to verify if the answer is based solely on the reference or if it is fabricated.

## Installation

### For Users

Install the package directly from PyPI using pip:

```sh
pip install ccheck
```

After installation, you can access the `ccheck` CLI command:

```sh
ccheck --help
```

This will display all available options and help you get started with using ContextCheck.

### For Developers

If you wish to contribute to the project or modify it for your own use, you can set up a development environment using Poetry.

1. Fork your own copy of Addepto/contextcheck on GitHub.
2. Clone the Repository:
  ```sh
  git clone https://github.com/<your_username>/contextcheck.git
  cd contextcheck
  ```
3. Ensure you have [Poetry](https://python-poetry.org/) installed.
4. Install Dependencies:
  ```sh
  poetry install
  ```
5. Activate the Virtual Environment:
  ```sh
  poetry shell
  ```
6. Activate the `ccheck` CLI command using:
  ```sh
  poetry run ccheck --help
  ```


## Tutorial

Please refer to `examples/` folder for the tutorial.


## CLI Features

### Output Test Results to Console

- **Run a single scenario and output results to the console:**
  ```sh
  ccheck --output-type console --filename path/to/file.yaml
  ```
- **Run multiple scenarios and output results to the console:**
  ```sh
  ccheck --output-type console --filename path/to/file.yaml path/to/another_file.yaml
  ```

### Running in CI/CD

To automatically stop the CI/CD process if any tests fail, add the `--exit-on-failure` flag. Failed test will cause the script to exit with code 1:

```sh
ccheck --exit-on-failure --output-type console --folder my_tests
```

Use env variable `OPENAI_API_KEY` to be able to run:
- `tests/scenario_openai.yaml`
- `tests/scenario_defaults.yaml`


## Contributing

Contributions are welcomed!

### Running Tests

To run tests:
```
poetry run pytest tests/
```

To include tests which require calling LLM APIs (currently OpenAI and Ollama), run one of:
```
poetry run pytest --openai          # includes tests that use OpenAI API
poetry run pytest --ollama          # includes tests that use Ollama API
poetry run pytest --openai --ollama # includes tests that use both OpenAI and Ollama API
```


## Acknowledgments

Made with ❤️ by the Addepto Team

ContextCheck is an extension of the [ContextClue](https://context-clue.com/) product, created by the [Addepto](https://addepto.com/) team. This project is the result of our team’s dedication, combining innovation and expertise.

Addepto Team:

* Radoslaw Bodus
* Bartlomiej Grasza
* Volodymyr Kepsha
* Vadym Mariiechko
* Michal Tarkowski

Like what we’re building? ⭐ Give it a star to support its development!


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
