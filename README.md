# FIE463: Numerical Methods in Macroeconomics and Finance using Python

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

Course material for spring term 2026 (V26) — Author: Richard Foltyn


## Course outline

`L` = Lecture, `W` = Workshop

### Part 1 — Introduction to Python

| Week | Date        | L/W | Topic | Notes & Exercises | Solutions |
|------|-------------|-----|-------|-------------------|-----------|
|  2   | Tue, Jan 15 | `L` | Introduction | [Slides](lectures/lecture00/lecture00.pdf) | — |
|  3   | Tue, Jan 20 | `L` | Language & NumPy basics | [Notebook](lectures/lecture01/lecture01.ipynb), [PDF](lectures/lecture01/lecture01.pdf) | — |
|      | Thu, Jan 22 | `W` | Language & NumPy basics | [Notebook](workshops/workshop01/workshop01.ipynb), [PDF](workshops/workshop01/workshop01.pdf) | [Notebook](workshops/workshop01/workshop01-solution.ipynb), [PDF](workshops/workshop01/workshop01-solution.pdf) |
|  4   | Tue, Jan 27 | `L` | Control flow & list comprehensions | [Notebook](lectures/lecture02/lecture02.ipynb), [PDF](lectures/lecture02/lecture02.pdf) | —  |
|      | Thu, Jan 29 | `W` | Control flow & list comprehensions | [Notebook](workshops/workshop02/workshop02.ipynb), [PDF](workshops/workshop02/workshop02.pdf) | [Notebook](workshops/workshop02/workshop02-solution.ipynb), [PDF](workshops/workshop02/workshop02-solution.pdf) |
|  5   | Tue, Feb 3  | `L` | Functions & modules | [Notebook](lectures/lecture03/lecture03.ipynb), [PDF](lectures/lecture03/lecture03.pdf) | —  |
|      | Thu, Feb 5  | `W` | Functions & modules | [Notebook](workshops/workshop03/workshop03.ipynb), [PDF](workshops/workshop03/workshop03.pdf) | [Notebook](workshops/workshop03/workshop03-solution.ipynb), [PDF](workshops/workshop03/workshop03-solution.pdf) |
|  6   | Tue, Feb 10 | `L` | Random numbers & plotting | [Notebook](lectures/lecture04/lecture04.ipynb), [PDF](lectures/lecture04/lecture04.pdf) | —  |
|      | Thu, Feb 12 | `W` | Random numbers & plotting | [Notebook](workshops/workshop04/workshop04.ipynb), [PDF](workshops/workshop04/workshop04.pdf) | [Notebook](workshops/workshop04/workshop04-solution.ipynb), [PDF](workshops/workshop04/workshop04-solution.pdf) |


### Part 2 — Applications to models in macroeconomics & finance

| Week | Date        | L/W | Topic | Notes & Exercises | Solutions |
|------|-------------|-----|-------|-------------------|-----------|
|  7   | Tue, Feb 17 | `L` | Numerical optimization | [Notebook](lectures/lecture05/lecture05.ipynb), [PDF](lectures/lecture05/lecture05.pdf) | —  |
|      | Thu, Feb 19 | `W` | Numerical optimization | [Notebook](workshops/workshop05/workshop05.ipynb), [PDF](workshops/workshop05/workshop05.pdf) | TBA |
|  8   | Tue, Feb 24 | `L` | General equilibrium | [Notebook](lectures/lecture06/lecture06.ipynb), [PDF](lectures/lecture06/lecture06.pdf) | —  |
|      | Thu, Feb 26 | `W` | General equilibrium | [Notebook](workshops/workshop06/workshop06.ipynb), [PDF](workshops/workshop06/workshop06.pdf) | TBA  |
|  9   | Tue, Mar 3  | `L` | Overlapping-generations models | [Notebook](lectures/lecture07/lecture07.ipynb), [PDF](lectures/lecture07/lecture07.pdf) | —  |
|      | Thu, Mar 5  | `W` | VS Code & GitHub Copilot integration | TBA | TBA |
|  10  | Tue, Mar 10 | `L` | Stochastic processes & wealth dynamics | [Notebook](lectures/lecture08/lecture08.ipynb), [PDF](lectures/lecture08/lecture08.pdf) | —  |
|      | Thu, Mar 12 | `W` | Stochastic processes & wealth dynamics | [Notebook](workshops/workshop08/workshop08.ipynb), [PDF](workshops/workshop08/workshop08.pdf) | TBA |


### Part 3 — Working with financial data

| Week | Date        | L/W | Topic | Notes & Exercises | Solutions |
|------|-------------|-----|-------|-------------------|-----------|
|  11  | Tue, Mar 17 | `L` | Data processing with Pandas | [Notebook](lectures/lecture09/lecture09.ipynb), [PDF](lectures/lecture09/lecture09.pdf) | —  |
|      | Thu, Mar 19 | `W` | Data processing with Pandas | [Notebook](workshops/workshop09/workshop09.ipynb), [PDF](workshops/workshop09/workshop09.pdf) | TBA |
|  12  | Tue, Mar 24 | `L` | Intro to scikit-learn | [Notebook](lectures/lecture10/lecture10.ipynb), [PDF](lectures/lecture10/lecture10.pdf) | —  |
|      | Thu, Mar 26 | `W` | Intro to scikit-learn | [Notebook](workshops/workshop10/workshop10.ipynb), [PDF](workshops/workshop10/workshop10.pdf) | TBA |
|  13  | Tue, Mar 31 | `L` | Regression models | [Notebook](lectures/lecture11/lecture11.ipynb), [PDF](lectures/lecture11/lecture11.pdf) | —  |
|      | Thu, Apr 2  | `W` | No workshop (Easter break) | — | — |
|  14  | Tue, Apr 7  | `L` | Classification models | [Notebook](lectures/lecture12/lecture12.ipynb), [PDF](lectures/lecture12/lecture12.pdf) | —  |
|      | Thu, Apr 9  | `W` | Regression & classification models | [Notebook](workshops/workshop12/workshop12.ipynb), [PDF](workshops/workshop12/workshop12.pdf) | TBA |



## Guides

See the [guides/](guides/README.md) folder for instructions on how to 
install Anaconda (Python), Visual Studio Code, and git version control.


## Forking & Cloning

### Forking

- Click on the `Fork` icon to fork this repository (create your own personal copy)
- In the future, you need to click on `Sync Fork` to get new commits made to this repository into your forked version.

### Cloning

1. Click on the green `Code` icon to clone the repository to your computer
2. Select HTTPS or SSH depending on your authentication method (SSH keys will only work if you have configured them) and copy the URL.
3. You can clone the repository directly in Visual Studio Code, or use the command line:

    _Using HTTPS (no SSH key configured):_
    ```bash
    git clone https://github.com/richardfoltyn/FIE463-V26.git
    ```
    _Using SSH keys:_
    ```bash
    git clone git@github.com:richardfoltyn/FIE463-V26.git
    ```


## Creating a Conda environment

Using the Anaconda Prompt (Windows) or Terminal (macOS), you can use 
the environment definition file ([environment.yml](environment.yml)) provided in this repository to create 
a conda environment called `FIE463`:
```bash
conda env create -f environment.yml
```
Note that you first need to change to the directory where `environment.yml` is located for this to work.

If you don't know how to locate the `environment.yml` file on your system,
you can also download it directly from GitHub and create the environment in one step:
```bash
curl -O https://raw.githubusercontent.com/richardfoltyn/FIE463-V26/main/environment.yml
conda env create -f environment.yml
```


## Additional resources

1. [Think Python](https://allendowney.github.io/ThinkPython/index.html) by Allen B. Downey:
   general intro to Python, chapters are available as Jupyter notebooks.
2. [Python for Everybody](https://www.py4e.com/book) by Charles R. Severance:
   general intro to Python with a focus on data analysis, available as PDF.
3. [QuantEcon](https://quantecon.org/lectures/): Python programming for economics & finance
    (beginners & advanced)
4. [Introduction to Programming and Numerical Analysis](https://sites.google.com/view/numeconcph-introprog/home): 
    Python for macroeconomics, taught at the University of Copenhagen

## License

This material is licensed under a 
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/),
except for the data files contained in the `data/` folder, which
fall under the terms imposed by the original content creators.
