# login-app-automation
A basic login app and its automation test code
This repository is a login test automation project targeting [The Internet - Login Page](https://the-internet.herokuapp.com/login) using **pytest** and **Playwright**.  
It covers multiple authentication scenarios (both successful and unsuccessful) by utilizing **data-driven tests (DDT)** with test data stored in CSV files.
Additionally, the tests are executed across multiple browsers—Chromium, Firefox, and WebKit—to ensure comprehensive cross-browser compatibility.



## Features

- **Data-Driven Testing**
  - Test data is stored in `testdata/login_data.csv` and is loaded by functions defined in `test_data.py`.
  - For each test case, the expected message is dynamically determined based on the input values.

- **Browser Operations using Playwright**
  - Uses the synchronous API to access the target page, fill out forms, perform click actions, and validate the results.

- **Screenshot Capture**
  - During test execution, screenshots are taken at various steps (after form fill-out, after login) and embedded into the HTML report using the `screenshot_helper` fixture.

- **HTML Report Generation**
  - The execution results are output as a self-contained HTML report using the `pytest-html` plugin.

## Directory Structure

```plaintext
login-app-automation/
├── testdata/
│   └── login_data.csv         # Test data (CSV)
├── tests/
│   ├── test_login.py          # Test code
│   └── conftest.py            # Common fixtures and settings (for screenshots, HTML report configuration, etc.)
├── test_data.py               # Utility for CSV loading & expected result determination
└── README.md                  # This documentation
```

## Environment Setup

1. **Install Python**  
   Ensure that Python 3.12 or later is installed.

2. **Create and Activate a Virtual Environment**

   python -m venv venv
   .\venv\Scripts\activate

3. **Install the Required Packages**

    pip install pytest playwright pytest-html
    playwright install

4. **Running the Tests**
    Execute the tests using the following command to generate a self-contained HTML report:

    pytest --html=report.html --self-contained-html
