# Reverse Mortgage Simulator Project

## Made By:

Tomás Cordoba Urquijo

Emmanuel Calad Correa

## Purpose

Its purpose is to provide an accessible and easy-to-use tool that allows users to thoroughly and accurately evaluate the options available in the reverse mortgage market. This software is designed to help older homeowners understand how this type of financial product works, estimate the potential amount of funds they could receive, and visualize the impact a reverse mortgage would have on their financial situation over time. The simulator offers an interactive simulation based on custom data, allowing users to adjust key variables such as property value, interest rate, and loan duration.

## How does it work?

The user must enter certain personal data (age, gender, marital status, age of their spouse (optional), and gender of their spouse (optional)). Additionally, you must enter information related to your home and the financing (value and interest rate).

Subsequently, the system will be in charge of carrying out the necessary calculations and will return the value of each monthly installment of the reverse mortgage.

## How is it done?

The project is divided into two main folders, an `src` folder and a `tests` folder. The `src` folder contains a module in which there is a file with the distribution of the classes and methods, and another is the module in which the execution of the program by console is found. On the other hand, the `tests` folder contains each of the unit `tests` (normal cases, extraordinary cases, and error cases). In addition, there are 3 files of the general structure of a project (.gitignore, README.md, and License).

## Installation and Use

### 1. Clone the Repository:
  
Open your command prompt and run the following command:

    git clone "https://github.com/emmanuelcalad0615/ReverseMortgageSimulator"
  
### 2. Navigate to the Project Directory:

Change your directory to the `ReverseMortgageSimulator` folder:

    cd path\to\ReverseMortgageSimulator

**Example:** If you cloned the repository to `C:\Projects`, you would run:

    cd C:\Projects\ReverseMortgageSimulator

### 3. Create a Virtual Environment

Before installing the required packages, it's recommended to create a virtual environment. Run the following commands:

#### Windows:

    py -m venv .venv
    .venv\Scripts\activate

#### macOS/Linux:

    python3 -m venv venv
    source venv/bin/activate

### 4. Install Requirements

Once the virtual environment is activated, install the required packages using the `requirements.txt` file:

    pip install -r requirements.txt

### 5. Execute the Program

#### Console Execution:

Run the `console.py` file:

    py src\Console\console.py

#### GUI Execution:

If a graphical user interface (GUI) is available, navigate to the `GUI` folder and run the `gui.py` file:

    py src\GUI\gui.py