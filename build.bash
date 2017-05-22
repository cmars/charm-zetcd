#!/bin/bash
set -e

rm -rf builds deps
charm build
rm -rf builds/zetcd/{builds, deps}
