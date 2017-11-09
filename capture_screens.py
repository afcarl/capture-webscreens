import os
import sys
import argparse
import time

from selenium import webdriver
from PIL import Image
from io import BytesIO


def read_lines(file_path):
    """
    Read lines in a file as a iterator.

    :param file_path: path to input file
    """
    # check wether it is a file or not
    if not os.path.isfile(file_path):
        print("%s is not file" % file_path)

    # read lines with yeild
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            yield line


def capture(driver, url, output, verbose=False):
    """
    Capture a full web page and then save it as a image.

    :param driver: browser driver for selenium
    :param url: captured URL
    :param output: path to output image
    :param verbose: verbose flag
    """

    driver.get(url)
    driver.maximize_window()
    # TODO adjust the time
    time.sleep(0.5)

    # SEE ALSO:
    # here http://stackoverflow.com/questions/1145850/how-to-get-height-of-entire-document-with-javascript
    js = """
    return Math.max(
      document.body.scrollHeight,
      document.body.offsetHeight,
      document.documentElement.clientHeight,
      document.documentElement.scrollHeight, 
      document.documentElement.offsetHeight);
    """
    scrollheight = driver.execute_script(js)
    viewport_height = int(driver.execute_script("return window.innerHeight"))
    if verbose:
        print("scroll height: %s" % (scrollheight))
    # capture screen scrolling down
    slices = []
    offset = 0
    while offset < scrollheight:
        if verbose:
            print("offset: %s"% (offset))
        driver.execute_script("window.scrollTo(0, %s);" % offset)
        img = Image.open(BytesIO(driver.get_screenshot_as_png()))
        slices.append(img)
        offset += viewport_height
        if verbose:
            driver.get_screenshot_as_file('%s/screen_%s.png' % ('/tmp', offset))
            print("scroll height: %s" % (scrollheight))

    ## merge parts of captures
    if verbose:
        print("# of slices: %d" % (len(slices)))

    offset = 0
    total_height = sum([img.size[1] for img in slices])
    screenshot = Image.new('RGB', (slices[0].size[0], total_height))
    for img in slices:
        screenshot.paste(img, (0, offset))
        offset += img.size[1]
    # save image
    screenshot.save(output)


def main(args):
    url_list = args.input
    output = args.output

    # make a directory to save images
    if not os.path.isdir(output):
        print("make a directory at %s" % (output))
        os.mkdir(output)

    # capture webscreens
    if args.driver == "chromedriver":
        num_line = 1
        driver = webdriver.Chrome()
        for url in read_lines(url_list):
            image_path = os.path.join(output, "%06d.png" % (num_line))
            capture(driver, url, image_path, verbose=args.verbose)
            num_line += 1
        driver.quit()
    elif args.driver == "phantomjs":
        num_line = 1
        driver = webdriver.PhantomJS()
        for url in read_lines(url_list):
            image_path = os.path.join(output, "%06d.png" % (num_line))
            driver.get(url)
            driver.save_screenshot(image_path)
            num_line += 1
        driver.quit()
    else:
        print("invalid selenium driver type: %s" % (args.driver))
        sys.exit(1)


if __name__ == "__main__":
    # parse options
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--driver", type=str, default="chromedriver", help="Selenium driver")
    parser.add_argument(
        "--input", type=str, default=None, help="Path to file which is a list of URLs")
    parser.add_argument(
        "--output", type=str, default=None, help="Path to directory to store captured images")
    parser.add_argument(
        "--verbose", action='store_true', default=False, help="Verbose flag")
    args = parser.parse_args()

    # validate arguments
    if args.input is None:
        print("invalid input: %s")
    if args.output is None:
        print("invalid output: %s")

    # run
    main(args)
