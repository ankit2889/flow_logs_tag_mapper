# Problem statement
This tool can parse a file containing flow log data and will count the frequency of matching tags and combination of dstport and protocol

# Requirement details(from the question)

1. Input file as well as the file containing tag mappings are plain text (ascii) files  
2. The flow log file size can be up to 10 MB 
3. The lookup file can have up to 10000 mappings 
4. The tags can map to more than one port, protocol combinations.  for e.g. sv_P1 and sv_P2 in the sample above. 
5. The matches should be case insensitive

# Assumptions

1. Only VPC flow logs version 2 supported
2. Only supports ports-protocol mapping specified in custom port_protocol_mapping.py created from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
3. Invalid flow log records will be logged and skipped
4. Validation is done on the number of fields in each log record and not the validity of individual fields (checks for length 14)
5. Tags lookup will contain dstport, protocol and tag and if not then it will log and skip it
6. Outputs will be stored for tag and dstport_protocol seperately under output/<tag/dstport_protocol>_timestamp.txt

# Files
1. flow_logs_parser.py : Script to load flow log records, tag from lookup file and count number of tags and dstport_protocol
2. port_protocol_mapping.py: created from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
3. tests/flow_logs_parser_test.py - Test with valid and invalid config
 
# Build and deploy instructions
1. Install python 3.x (tested with v3.9.6)
2. Navigate to root dir and run scripts/flow_logs_parser.py and pass appropriate command-line args to run the tool
```
    python scripts/flow_logs_parser.py --logs_file tests/resources/flow_logs.txt --tags_file tests/resources/tags.csv
```
Arguments list: 

- logs_file: Path to vpc flow logs file (eg: tests/resources/flow_logs.txt)
- tag_file: Path to tag lookup file (eg: tests/resources/tags.csv)

3. Navigate to root dir and run unit test from root dir to validate with input log files and tags.csv and one test case for invalid path
```
   python -m unittest -v tests/flow_logs_parser_test.py
```
Note: Tool is tested to work with flow_logs file of max size 10mb and 10k tags with execution time of 0.07 and 0.06 sec

4. To fetch counts for other fields, update the log_fields to add that additional field:
```
log_fields = {
   'dstport': record[6], 
   'protocol': record[7]
   '<additional-field>': record[<field-index>]
}
```

# Future Enhancements
1. Support version 3 additional fields (only update the log pattern regex)
3. Updated to read log files and tag lookup files from remote sources like s3 or any servers by using requests library
4. Updated to read log files asynchronously by using python's asyncio library
5. Can be containerized by adding dockerfile with base python-alpine image and copying the src scripts and log files
  

 