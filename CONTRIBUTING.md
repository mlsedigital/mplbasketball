# Contributing to mplbasketball

Contributions are made to this repo via Issues and Pull Requests (PRs)

## Quicklinks

- [Issues](#issues)
- [Pull Requests](#pull-requests)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Reviewing and Merging](#reviewing-and-merging)

## Issues

Issues should be used to report problems with the library, request a new feature, or to discuss potential changes before a PR is created.

If you find an Issue that addresses the problem you're having, please add your own reproduction information to the existing issue rather than creating a new one. Adding a [reaction](https://github.blog/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) can also help be indicating to our maintainers that a particular problem is affecting more than just the reporter.

## Pull Requests

Pull requests should address a single concern with the least number of changed lines possible, be well-described, and ensure that the code is thoroughly tested before submission. We typically follow the standard Git workflow of cloning or forking the repository and then creating pull requests. Additionally, **poetry** is used to manage package dependencies in the project. To make a pull request:

### 1. Clone the Repository

First, clone the repository from GitHub:

```bash
git clone https://github.com/mlsedigital/mplbasketball.git
```

Then navigate into the project directory:

```bash
cd mplbasketball
```

### 2. Set up a Virtual Environment

Create a Python virtual environment to isolate your dependencies:

```bash
# macOS/Linux
python3 -m venv .venv

# Windows
python -m venv .venv
```

Activate the virtual environment

```bash
source .venv/bin/activate #on macOS/Linux

source .venv\Scripts\activate #on WIndows
```

Verify the virtual environment is active (you should see `.venv` in your terminal prompt):

```bash
which python
```

### 3. Install Poetry

Install Poetry within the virtual environment:

```bash
pip install poetry
```

### 4. Install Dependencies

Inside the virtual environment, run the following to install all dependencies:

```bash
poetry install
```

## Making Changes

1. Make the necessary changes to the codebase.
2. Create a new branch for your changes:

```bash
git checkout -b <your-branch-name>
```

3. Commit your changes:

```bash
git add .
git commit -m "Describe your changes"
```

4. Push your branch to Github and create a pull request

```bash
git push origin <your-branch-name>
```

Open a pull request by visiting the [Pull Requests](https://github.com/mlsedigital/mplbasketball/pulls) page on GitHub.

## Testing

Before submitting your pull request, make sure to run the tests to ensure your changes don't break existing functionality.

### Running Tests

You can run the tests using pytest through Poetry:

```bash
# Run all tests
poetry run pytest

# Run tests with verbose output
poetry run pytest -v
```

### Checking Code Coverage

To check the code coverage of the tests, use the `pytest-cov` plugin:

```bash
# Run tests with coverage report
poetry run pytest --cov=mplbasketball

# Generate a detailed HTML coverage report
poetry run pytest --cov=mplbasketball --cov-report=html
```

The HTML coverage report will be generated in the `htmlcov` directory. Open `htmlcov/index.html` in your browser to view the detailed coverage report.

### Writing Tests

When adding new features or fixing bugs, please include tests that cover your changes. Tests should be placed in the `tests/` directory and follow the existing naming conventions:

- Test files should be named `test_*.py`
- Test functions should be named `test_*`
- Each test function should focus on testing a specific functionality

## Reviewing and Merging

To facilitate a smooth merge:

- **Be Responsive**: Address any feedback or requested changes promptly.
- **Follow Workflow**: We use the standard Git workflow, typically involving cloning or forking the repository and creating pull requests. Ensure your branch is up-to-date with the main branch before submission.
- **Dependency Management**: The project uses Poetry for package dependency management. Make sure to test your changes in a properly configured environment to avoid dependency conflicts.

Once you submit a pull request, it will be reviewed by maintainers. Please be patient and responsive to feedback to ensure a smooth merge.

---

Thank you for contributing!
