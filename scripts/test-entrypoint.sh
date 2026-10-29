#!/bin/sh
set -eu

pytest --create-db "$@"
