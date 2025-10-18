name: Auto Shorts

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repo
      uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11

    - name: Install dependencies
      run: |
        pip install --upgrade pip
        pip install moviepy google-api-python-client google-auth google-auth-oauthlib

    - name: Install ffmpeg
      run: |
        sudo apt-get update
        sudo apt-get install -y ffmpeg

    - name: Run Auto Shorts
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        GOOGLE_CREDENTIALS_JSON: ${{ secrets.GOOGLE_CREDENTIALS_JSON }}
      run: |
        python auto_shorts.py

