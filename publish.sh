#!/usr/local/bin/bash
set -x

poetry version patch
poetry publish --build