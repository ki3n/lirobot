# lirobot
A robot for scraping job titles, job descriptions, and job links from LinkedIn.com job search results. The robot visits LinkedIn.com,  signs in using your (faked) credentials, visits the jobs page, searches for a result, scrapes all the links on the 1-40 pages, and visits each link. The job title, job decription, and job links from each posting are stored in a .csv file.

### Installing Dependencies
To begin using this robot, you must install a few necessary python packages, a web client, and a corresponding web driver. 

1. You must install [Selenium](https://pypi.python.org/pypi/selenium) and [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4/4.3.2). This can be done easily by using ``pip``:

```bash
sudo pip install bs4 selenium
```
2. You must install a web browser which supports the use of Selenium. I suggest a non-mobile browser because that's the only browser I ran code tests upon. Typically people will use [Firefox](https://www.mozilla.org/en-US/firefox/new/) or [Chrome](https://www.google.com/chrome/browser/desktop/index.html).

3. You must install a corresponding web driver for your browser: [geckodriver](https://github.com/mozilla/geckodriver/releases) for Firefox and [chrome driver](https://sites.google.com/a/chromium.org/chromedriver/) for Chrome. I would recommend installing the driver in your browser's installation directory and making a symbolic link to the file within ``/usr/bin``:

```bash
sudo mv /path/to/driver/file /path/to/browser/installation/directory
sudo ln -s /new/path/to/driver/file /usr/bin
```

### Running the script
Before running the script, there are a few things to understand:
1. Do not run two instances of this script at the same time from the same account OR two instances of this script at the same time with the request headers. I left the script very basic so that others could use the script for their own needs. It seems that LinkedIn.com has a way to detect robots by their frequency of requests, but not by using a web driver directly. I leave the user to sort out the process of changing request headers, changing JavaScript document object names, etc...

2. You need to change the browser instance opened by ``driver = webdriver.Firefox()`` on line 35 to match your browser.

3. You will need to enter in your own information into the *Parameters* section of the script at the top. The section is commented well to help the user understand what they need to supply.
