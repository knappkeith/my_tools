#! /usr/bin/env python

from selenium.webdriver import PhantomJS as JS
import time
import datetime
import json
import sys as _sys
import numpy


WAIT_TIME_IN_SEC = 60 * 5
URL_TO_SPEED_TEST = "http://www.bandwidthplace.com/"

def loop_tester(num_runs):
    records = []
    try:
        record = speed_tester()
        records.append(record)
        print "Up: %s, Down: %s, Time: %s" % (
            record['upSpeed'], record['dwSpeed'], record['time'])
        for i in range(0, num_runs - 1):
            time.sleep(WAIT_TIME_IN_SEC)
            record = speed_tester()
            records.append(record)
            print "Up: %s, Down: %s, Time: %s" % (
                record['upSpeed'], record['dwSpeed'], record['time'])
    except KeyboardInterrupt:
        print ""
        print "Stopping execution, Results:"
        print_results(records)
        return
    print ""
    print "Results:"
    print_results(records)

def speed_tester():
    speed_driver = JS()
    speed_driver.get(URL_TO_SPEED_TEST)
    start_button = speed_driver.find_element_by_id("speedo-start")
    up_speed = speed_driver.find_element_by_id("speedo-up")
    down_speed = speed_driver.find_element_by_id("speedo-down")
    ping_time = speed_driver.find_element_by_id("speedo-ping")
    ip_address = speed_driver.find_element_by_id("speedo-ip")
    provider = speed_driver.find_element_by_id("speedo-provider")
    selected_server = speed_driver.find_element_by_id("speedo-server")

    start_button.click()

    while start_button.get_attribute("class") == "testing":
        time.sleep(1)
    while up_speed.text == "--.--":
        time.sleep(1)
    while down_speed.text == "--.--":
        time.sleep(1)

    record = {
        "upSpeed": up_speed.text,
        "dwSpeed": down_speed.text,
        "pingTime": ping_time.text,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ipAddress": ip_address.text,
        "provider": provider.text,
        "selectServer": selected_server.text
    }
    speed_driver.quit()
    return record

def print_results(records):
    if len(records) > 0:
        answer = raw_input("Print JSON Blob(Y/N)? ")
        if answer.upper() in ["YES", "Y"]:
            print ""
            print "JSON Blob:"
            print json.dumps(records, indent=2)
        print ""
        process_results(records)
    else:
        print "No Records to process!!"

def process_results(records):
    total_up = [float(i['upSpeed']) for i in records]
    total_dw = [float(i['dwSpeed']) for i in records]

    print "    Standard deviation(UP): %0.2f" % numpy.std(total_up)
    print "    Standard deviation(DOWN): %0.2f" % numpy.std(total_dw)

    print "    Average(UP): %0.2f" % numpy.average(total_up)
    print "    Average(DOWN): %0.2f" % numpy.average(total_dw)

    print "    Lowest(UP): %0.2f, Highest(UP): %0.2f" % (min(total_up), max(total_up))
    print "    Lowest(DOWN): %0.2f, Highest(DOWN): %0.2f" % (min(total_dw), max(total_dw))

if __name__ == "__main__":
    if len(_sys.argv) > 1:
        times = int(_sys.argv[1])
        if times > 0:
            print "Running the test %d time(s) every %d seconds!" % (times, WAIT_TIME_IN_SEC)
            loop_tester(times)
        else:
            print "Must pass a value > 0: %d" % times
            _sys.exit(0)
    else:
        print "Running every %d seconds FOR-EV-ER!!!!! Ctrl+C to Stop" % WAIT_TIME_IN_SEC
        loop_tester(100000000)
