#!/bin/bash

mkdir -p day$1/src
cp template.rs "day${1}/src/main.rs"
cp template.toml "day${1}/Cargo.toml"

# Download input
# Put this in .cookie.txt
# cookie: session=<token-copied-from-browser-devtools>
curl -o day$1/input.txt -H @.cookie.txt https://adventofcode.com/2022/day/$1/input
