import os
import sys
from django.test import TestCase

from synthesize import text2speech


# Create your tests here.
def split(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            text = line.strip()
            file_path = text.lower().replace(' ', '_')
            print(text)
            text2speech(file_path, text)


split("text.txt")
