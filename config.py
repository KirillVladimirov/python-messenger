# coding=utf-8

import os

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# environment (production, development, test)
environment = 'test'

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2
