name: Auto YouTube Shorts (Pipeline)

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Upgrade pip
        run: python -m pip install --upgrade pip

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y ffmpeg
          pip install --upgrade setuptools wheel
          pip install openai google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client Pillow requests moviepy

      - name: Run AI Shorts Pipeline
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
        run: python run_pipeline.py
