import os
import sys
import pytest
import inspect

import yaml

collection = {}

def step(step, return_param=None):
  def wrapped(func):
    def wrapped_f(*args, **kwargs):
      if _gencase:
        name, doc = get_caller_test()
        if name not in collection:
          collection[name] = {}
          collection[name]["doc"] = doc
          collection[name]["steps"] = []
        collection[name]["steps"].append({"args": args, "step": step})
        return return_param
      else:
        return func(*args, **kwargs)
    return wrapped_f
  return wrapped

def get_caller_test():
  f = sys._getframe(2)
  while f:
    name = f.f_code.co_name
    if name.startswith("test_"):
      return name, inspect.getdoc(f.f_globals[name])
    f = f.f_back

def pytest_addoption(parser):
    parser.addoption("--gencase", action="store_false", default=True)
    parser.addoption("--caseformat", action="store", default="rst")

def pytest_generate_tests(metafunc):
  global _gencase
  global _caseformat
  _gencase = not metafunc.config.option.gencase
  _caseformat = metafunc.config.option.caseformat

def pytest_sessionfinish(session, exitstatus):
  if _caseformat in case_types:
    case_types[_caseformat]()
  else:
    raise Exception(f"There in no {_caseformat} case formater supported.")
  
def get_lines(rst=True):
  lines = ["Test Cases\n",
           "==========\n"]
  for name, v in collection.items():
    doc = v["doc"]
    if rst:
      lines.append(f"\n[{name}]\n{'^'*(len(name) + 2)}\n\n{doc}\n\n**Steps:**\n\n")
    else:      
      lines.append(f"\n[{name}]\n\n{doc}\n\nSteps:\n")
    for step in v["steps"]:
      args = step["args"]    
      if rst:
        step = step["step"].replace("\n", "\n\n") 
        args = [yaml.dump(x, indent=4).replace('\n', '\n\n\t') if isinstance(x, dict) else x for x in args]
        lines.append("#. " + step.strip().format(*args) + "\n\n")
      else:
        step = step["step"]
        args = [yaml.dump(x, indent=4).replace('\n', '\n\t\t') if isinstance(x, dict) else x for x in args]
        lines.append(step.strip().format(*args) + "\n")
  return lines

def console():
  print()
  print(*get_lines(False))

def rst():
  if os.path.isfile('test_case.rst'):
    os.remove("test_case.rst")
  lines = get_lines()
  with open("test_case.rst", "w+") as f:
    f.writelines(lines)
    
case_types = {
  "rst": rst,
  "cmd": console,
  "console": console
}