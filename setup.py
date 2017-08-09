# -*- coding: utf-8 -*-

application_title = "Image Metadata" #what you want to application to be called
main_python_file = "combined.py" #the name of the python file you use to run the program

import sys

from cx_Freeze import setup, Executable

base = "Console"

packages = ["exifread","openpyxl","os","datetime"]

executables = [
    Executable(script = main_python_file, base = base),
    # Executable(script = 'excel.py', base = base),
    # Executable(script = 'metadata.py', base = base)
]

setup(
        name = application_title,
        version = "0.1",
        description = "Extract Image Metadata",
        options = {
            "build_exe" : {
                "includes" : [
                    "exifread","openpyxl","os","datetime","encodings"
                ],
                "packages" : packages,
                "path" : sys.path + ["image_processing"]
            }
        },
        executables = executables)
