# Capture webscreen

This is a tool to capture full page pages with selenium in python.
You just have to prepare for a file of URL list and execute this tool.

## Requirements

- Google Chrome
- Chrome Driver
- Python 3+

## How to Use

- `--driver`: Selenium driver. Supporting `chromedriver` and `pahtomjs` now.
- `--input`: Path to a file of URL list
- `--output`: Path to a directory to store captured images

```
# Run on ChromeDriver
python capture_screens.py  \
  --driver chromedriver \
  --input test-urls.txt \
  --output ./capture-images/

# Run on Phantom JS
python capture_screens.py  \
  --driver phantomjs \
  --input test-urls.txt \
  --output ./capture-images/
```

## How Setup

### Install Python libraries

```
pip install -r requirements.txt
```

### Install Chrome Driver

If you are using mac, you should install

- [Homebrew](https://brew.sh/)
- [Homebrew/homebrew\-services](https://github.com/Homebrew/homebrew-services)

```
# Install chrome-driver
brew install chromedriver

# Start chrome-driver
brew services start chromedriver
```

## Install PhantomJS

```
brew install phantomjs
```

# See Also

- [Website screenshot generator with Python – Ronny Yabar – Medium](https://medium.com/@ronnyml/website-screenshot-generator-with-python-593d6ddb56cb)
