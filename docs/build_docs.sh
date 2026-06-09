#!/bin/sh

LANG_CODE=$1

if [ -n "$LANG_CODE" ]; then
  echo "Building docs for language: $LANG_CODE..."
  sphinx-build -b html source/ "build/html_$LANG_CODE/" -D language="$LANG_CODE"
else
  echo "Building docs in default language..."
  sphinx-build -b html source build/html
fi
