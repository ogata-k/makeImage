# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 14:13:34 2017

@author: Owner
"""


from cx_Freeze import setup, Executable

base = None
includefiles = ["readme.txt"]

setup(name="sample",
      version="1.0",
      description="converter",
      options={"build_exe": {"include_files": includefiles}},
      executables=[Executable("make_img.py", base=base)])
