#!/usr/bin/env bash

BASEDIR=$(dirname $0)

mkdir -p ~/.babyslam/sets
cp -r "$BASEDIR/samples" "$HOME/.babyslam/sets"
