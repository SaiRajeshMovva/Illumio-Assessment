import csv
import sys

# Mapping from protocol numbers to protocol names.
PROTOCOL_MAP = {
    "1": "icmp",
    "6": "tcp",
    "17": "udp"
}


def load_lookup(lookup_filename):
    """
    Reads the lookup CSV file and returns a dictionary with keys as
    (dstport, protocol) tuples and values as tags.
    """
    lookup = {}
    with open(lookup_filename, "r", encoding="ascii") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=["dstport", "protocol", "tag"])
        first_row = next(reader)
        if first_row["tag"].lower() == "tag":
            pass  
        else:
            port = first_row["dstport"].strip()
            proto = first_row["protocol"].strip().lower()
            tag = first_row["tag"].strip()
            lookup[(port, proto)] = tag
        for row in reader:
            port = row["dstport"].strip()
            proto = row["protocol"].strip().lower()
            tag = row["tag"].strip()
            lookup[(port, proto)] = tag
    return lookup

def parse_flow_logs(flow_filename, lookup):
    """
    Processes the flow log file and computes:
      - tag_counts: counts of how many times each tag is applied
      - port_proto_counts: counts of each (dstport, protocol) combinations seen
    fields are - version,account-id,interface-id,srcaddr,dstaddr,srcport,dstport,protocol,packets,bytes,start,end,action,log_status
    """
    tag_counts = {}
    port_proto_counts = {}

    with open(flow_filename, "r", encoding="ascii") as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue  # skips blank lines

            fields = line.split()
            dstport = fields[6].strip()
            proto_num = fields[7].strip()
            protocol = PROTOCOL_MAP.get(proto_num, "others").lower()

            # Count this port/protocol combination
            pp_key = (dstport, protocol)
            port_proto_counts[pp_key] = port_proto_counts.get(pp_key, 0) + 1

            # Look up tag (case-insensitive match on protocol, and exact string match for port)
            tag = lookup.get(pp_key, "Untagged")
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    return tag_counts, port_proto_counts


def output_results(tag_counts, port_proto_counts):
    print("Tag Counts:")
    print("Tag,Count")
    # Sorting tags alphabetically
    for tag in sorted(tag_counts.keys()):
        print(f"{tag},{tag_counts[tag]}")
    print("\nPort/Protocol Combination Counts:")
    print("Port,Protocol,Count")
    # Sort by port (numerically when possible) then protocol
    def sort_key(item):
        port, proto = item[0]
        try:
            return (int(port), proto)
        except ValueError:
            return (port, proto)
    for (port, proto), count in sorted(port_proto_counts.items(), key=sort_key):
        print(f"{port},{proto},{count}")


def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: python3 main.py <lookup_file.csv> <flow_log_file.txt>\n")
        sys.exit(1)

    lookup_filename = sys.argv[1]
    flow_filename = sys.argv[2]

    lookup = load_lookup(lookup_filename)
    tag_counts, port_proto_counts = parse_flow_logs(flow_filename, lookup)
    output_results(tag_counts, port_proto_counts)



if __name__ == "__main__":
    main()
