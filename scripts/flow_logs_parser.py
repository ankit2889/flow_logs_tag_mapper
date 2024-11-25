#!/usr/bin/env python3
import argparse
import time
import os
from collections import Counter, defaultdict
import csv
from port_protocol_mapping import port_protocol_mapping

def load_flow_logs(log_file):
    """load vpc flow logs from input log file and extract ip, dstport and protocol from each entry
    Args:
        log_file: input log file

    Returns:
        [{ dstport: '', protocol: ''}]
    """
    flow_logs = []
    try:
        with open(log_file, 'r') as file:
            for line in file:
                record = line.strip().split()
                # validating number of fields in record and not content of each field
                if record and len(record) >= 14:
                    log_fields = {
                        'dstport': record[6], 
                        'protocol': record[7] 
                    }
                    flow_logs.append(log_fields)
                else:
                    print(f"Invalid record: {record}") # skip invalid records
    except Exception as e:
        print(f"Error occurred while loading flow logs: {e}")

    return flow_logs
    
def load_tags(csv_file):
    """
    Load dstposrt, protocol, tags from the input .csv file        
    Returns:
        tags -> {"dstport, protocol" : "tag"}
    """
    tags = defaultdict()
    try:
        with open(csv_file) as f:
            reader = csv.reader(f, delimiter=',')
            header = next(reader, None) # skip header row
            for row in reader:
                if len(row) >= 3 and all(row[i] for i in range(3)):
                    key = f"{row[0]},{row[1]}".strip()
                    tags[key] = row[2].strip()
                else:
                   print(f"Invalid tag lookup: {row}") # skip invalid tag lookup
    except Exception as e:
        print(f"Error occurred while loading the tags: {e}")

    return tags

def generate_counts(flow_log_file_path, tags_file_path):
    """
    Generate counts of flow log entries based on a given keyword (e.g., 'tag' or 'dstport_protocol').

    Args:
        flow_log_file_path (str): Path to the flow log file.
        tags_file_path (str): Path to the tags file.
        keyword (str): Count grouping criterion ('tag' or 'dstport_protocol'). Default is 'tag'.

    Returns:
        count_map -> { tag : <count> } 
    """
    try:
        # future updates: asyncio lib can be used to read flow logs and tags asynchronously
        flow_logs = load_flow_logs(flow_log_file_path)
        tags = load_tags(tags_file_path)
        if not flow_logs:
            raise Exception("No flow logs found")
        if not tags:
            raise Exception("No tags found")

        tag_counter = Counter()
        port_protocol_counter = Counter()

        for flow_log in flow_logs:
            protocol = flow_log.get('protocol')
            if protocol not in port_protocol_mapping:
                print(f"Protocol '{protocol}' not found in protocol-port mappings.")
                continue
            
            mapped_protocol = port_protocol_mapping[protocol]
            flow_log_tag = f"{flow_log['dstport']},{mapped_protocol}"

            if flow_log_tag in tags:
                tag_counter[tags[flow_log_tag]] += 1
            else:
                tag_counter['untagged']+= 1

            port_protocol_counter[flow_log_tag] += 1

        return tag_counter, port_protocol_counter
    
    except Exception as e:
        print(f"Error while generating count_map: {e}")
        # raise exception
        raise

def generate_reports(output_file, tag_counter, port_protocol_counter):
    """Generate output reports for tag count and p
    """
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as file:
            file.write("Tag Counts:\n")
            file.write("Tag,Count\n")  
            file.writelines(f"\n{tag},{count}" for tag,count in tag_counter.items())

            file.write("\n\n\nPort/Protocol Combination Counts:\n")
            file.write("Port,Protocol,Count\n")
            file.writelines(f"\n{port_protocol},{count}" for port_protocol,count in port_protocol_counter.items())
            print(f"Report generated successfully at {output_file}")
    except Exception as e:
        print(f"Error while generating report: {e} ")

def main():
    parser = argparse.ArgumentParser(description="Program to get the counts for tag and/or dst,protocol")
    parser.add_argument('--logs_file', default= '', type=str, help='Path to the vpc flow logs file')
    parser.add_argument('--tags_file', default= '', type=str, help='Path to the tags file')
    args = parser.parse_args()

    tag_counter, port_protocol_counter = generate_counts(args.logs_file, args.tags_file)

    if tag_counter and port_protocol_counter:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_file = f"output/counts_{timestamp}.txt"
        generate_reports(output_file, tag_counter, port_protocol_counter)

if __name__ == '__main__':
    main()

