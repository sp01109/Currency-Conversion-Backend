# Currency Conversion Backend

This is a Currency Conversion backend service that uses the FastAPI framework.

## Installation

1. Make sure you have Python 3.9 installed. It is suggested to use `conda` to create a dedicated environment on your computer.
2. Clone or download the repository to your local machine.
3. Open a terminal or command prompt and navigate to the project directory.
4. Create a new conda environment: `conda create --name CurrencyConversion python=3.9`.
5. Activate the environment: `conda activate CurrencyConversion`.
6. Install the required dependencies: `pip install -r requirements.txt`.

## Usage

To run the program, make sure the conda environment is activated by running `conda activate CurrencyConversion`, 

Run the following command to start the program for development:
```bash
uvicorn main:app --reload
```

## Testing

Unit testing code is included in `test_main.py`. It is built based on **PyTest** framework with **HTTPX** to start the emulator as an *AsyncClient*.

Run the following command to execute testing:

```bash
pytest
```

## License

This project is licensed under the MIT License.