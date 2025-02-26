# Illumio Assessment

## Overview
This assessment is a Python-based solution designed to parse AWS VPC flow log data and map each log entry to a specific tag based on a lookup table provided as a CSV file. The lookup table associates a combination of destination port (`dstport`) and protocol (`protocol`) with a tag. The program processes the flow log data, applies the mapping, and produces two outputs:
- A count of matches for each tag.
- A count of matches for each (port, protocol) combination.

## Components
- **Flow Log Parsing:** Processes AWS VPC flow log records (Version 2 format).
- **Lookup Table Mapping:** Reads a CSV file with header `dstport,protocol,tag` and maps flow log entries.
- **Protocol Conversion:** Converts protocol numbers (e.g., `6`, `17`, `1`) to their names (`tcp`, `udp`, `icmp`).
- **Case-Insensitive Matching:** Performs case-insensitive comparisons for protocols.
- **Comprehensive Output:** Generates two CSV outputs:
  - Tag Counts.
  - Port/Protocol Combination Counts.
- **Unit Testing:** Includes unit tests to verify core functionality.

## Getting Started

### Prerequisites
- **Python Version:** Python 3.6 or higher is recommended.
- **Dependencies:** The project uses Python’s standard library modules (`csv`, `sys`, etc.), so no external packages are required.

### Installation
**Clone the Repository:**
   ```bash
   git clone https://github.com/SaiRajeshMovva/Illumio-Assessment.git
   cd Illumio-Assessment
   ```

### Running the Program
The program requires two arguments:
- The lookup CSV file.
- The flow log file.

Run the program with below command (sample lookup file and log file is in `/data` directory)
```python
python3 main.py <data/lookup_file.csv> <data/flow_log_file.txt>
```

### Running Unit Tests
Unit tests are provided to ensure the integrity of core functions. To run the tests:
```python
python3 -m unittest discover
```

This command automatically discovers and executes all tests located in the `tests/` directory.

## Approach & Assumptions

### Flow Log File Assumptions
- **Format:** The flow log file is assumed to follow the AWS VPC Flow Log Version 2 format based on given sample.
- **Field Order:** The expected order of fields is: `version, account-id, interface-id, srcaddr, dstaddr, srcport, dstport, protocol, packets, bytes, start, end, action, log_status`
- **Field Usage:** The program uses `dstport` (field index 6) and `protocol` (field index 7) for tagging. 

### Lookup CSV File Assumptions
- **Header:** The CSV file must include a header row with exactly `dstport,protocol,tag`. If the header is missing or misformatted (e.g., extra spaces or different casing), a `KeyError` might occur.
- **Content:** Each row must contain:
- A destination port (`dstport`)
- A protocol (as a string, e.g., `tcp`)
- The corresponding tag (`tag`)
- **Case Sensitivity:** Protocol matching is done in a case-insensitive manner to handle given requirement, while destination ports are matched exactly.

### Protocol Conversion
- **Mapping:** AWS flow logs represent the protocol as a number. A predefined mapping converts (taken from [here](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml))
- `6` → `tcp`
- `17` → `udp`
- `1` → `icmp`
- **Fallback:** If a protocol number is not in the mapping, the program uses `other` protocol.

### Error Handling
- **CSV Header Issues:** A missing or misformatted CSV header (e.g., missing `"tag"`) will result in a `KeyError`. Ensure that the CSV file is correctly formatted or modify the code to handle header variations.

---


