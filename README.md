# pygencase

Plugin for [pytest](https://docs.pytest.org/en/latest/) to generate 'use/test' case.

# How to use

- Mark method from your library/framework with `step` decorator.

```python
from pygencase import step

@step("""
    Test case take:
    {}
    and
    {}
    Do something.
""", "And return this str or object")
def foo(param_1, param_2):
  ...
````

- run `pytest` with `gencase` and `caseformat` parameters. 
Example:

```sh
pytest --gencase --caseformat rst test_case.py
```

- `rst` file will be generated.

Format should be like following:

> ## Test Cases
>
> ### [test_a]
>
> {test doc str}
>
> **Steps:**
>
> 1. Test case take:
>
> {param_1}
>
> and
>
> {param_2}
>
> Do something.
```
