from flask import Flask, render_template
from schedule_scraper import *

app = Flask(__name__)
driver = init_scraper_driver()


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/availability")
def scraper_availability():
    return get_scraped_availability(driver=driver)


if __name__ == "__main__":
    app.run()
    driver.quit()
