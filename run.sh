#!/usr/bin/env bash

cd scripts
python3 create_info_json_for_new_article.py
python3 generate_readme.py
cd ..
cp ./README.md public
cp -r ./markdown_new public
cp -r ./markdown_cleaned public
cp -r ./assets public
