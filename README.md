# cf_at_bq_dials
## Overview

`cf_at_bq_dials` is a Python-based tool designed to facilitate the integration and analysis of data from Cloud Functions (CF) and BigQuery (BQ) using DIALS (Data Integration and Analysis Library Suite). This tool aims to streamline the process of data ingestion, transformation, and analysis, providing a seamless experience for data engineers and analysts.

## Features

- **Data Ingestion**: Easily ingest data from various sources into BigQuery.
- **Data Transformation**: Perform complex data transformations using DIALS.
- **Automation**: Automate data workflows with Cloud Functions.
- **Scalability**: Handle large datasets efficiently with BigQuery.
- **Integration**: Seamlessly integrate with other Google Cloud services.

## Installation

To install `cf_at_bq_dials`, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/cf_at_bq_dials.git
cd cf_at_bq_dials
pip install -r requirements.txt
```

## Usage (Locally)

1. **Configure your environment**: Set up your Google Cloud credentials and BigQuery dataset and your Python virtual-env.
2. **Run the tool**: Execute the main script to start the data integration process by using functions-framework.

```bash
functions-framework --target post_to_bigquery_with_timestamp --debug
```

## Debugging with VS Code

To debug the `cf_at_bq_dials` project in VS Code, you need to set up the `launch.json` file. This file allows you to configure the debugging environment and specify how the debugger should run your application.

1. **Open the Command Palette**: Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac) and type `Debug: Open launch.json`.

2. **Select Environment**: Choose `Python` as the environment.

3. **Configure `launch.json`**: Add the following configuration to your `launch.json` file:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Functions Framework",
            "type": "debugpy",
            "request": "launch",
            "module": "functions_framework",
            "console": "integratedTerminal",
            "args": [
                "--target",
                "post_to_bigquery_with_timestamp",
                "--debug",
            ],
            "cwd": "${workspaceFolder}/code_dir",
        }
    ]
}
```

4. **Start Debugging**: Set breakpoints in your code, then press `F5` to start debugging. The debugger will launch the Functions Framework and attach to it, allowing you to step through your code and inspect variables.

By following these steps, you can effectively debug your `cf_at_bq_dials` project using VS Code.

## Contributing

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact

For any questions or feedback, please open an issue on GitHub :D