import re
import json
import csv

def parse_markdown(md_text):
    data = {}

    # Extract Executive Summary
    exec_summary_match = re.search(r'## Executive Summary(.*?)##', md_text, re.DOTALL)
    if exec_summary_match:
        data['Executive Summary'] = exec_summary_match.group(1).strip()

    # Extract Fund Overview
    fund_overview_match = re.search(r'## Fund Overview(.*?)##', md_text, re.DOTALL)
    if fund_overview_match:
        data['Fund Overview'] = fund_overview_match.group(1).strip()

    # Extract Investment Strategy
    invest_strategy_match = re.search(r'## Investment Strategy(.*?)##', md_text, re.DOTALL)
    if invest_strategy_match:
        data['Investment Strategy'] = invest_strategy_match.group(1).strip()

    # Extract Team Structure
    team_structure_match = re.search(r'## Team Structure(.*?)##', md_text, re.DOTALL)
    if team_structure_match:
        data['Team Structure'] = team_structure_match.group(1).strip()

    # Extract Total Assets Under Management (AUM)
    aum_match = re.search(r'## Total Assets Under Management \(AUM\)(.*?)##', md_text, re.DOTALL)
    if aum_match:
        data['AUM'] = aum_match.group(1).strip()

    # Extract Risk Assessment
    risk_assessment_match = re.search(r'## Risk Assessment(.*)', md_text, re.DOTALL)
    if risk_assessment_match:
        data['Risk Assessment'] = risk_assessment_match.group(1).strip()

    return data

def save_json(data, filename='corporate_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Saved JSON data to {filename}")

def save_csv_from_table(md_text, filename):
    # Extract markdown table
    table_match = re.search(r'(\|.*\|[\r\n]+(\|[-: ]+\|)+[\r\n]+(\|.*\|[\r\n]*)+)', md_text)
    if not table_match:
        print(f"No table found in markdown for {filename}")
        return
    table_text = table_match.group(1).strip()
    lines = table_text.split('\n')
    headers = [h.strip() for h in lines[0].strip('|').split('|')]
    rows = []
    for line in lines[2:]:
        if line.strip() == '':
            continue
        row = [c.strip() for c in line.strip('|').split('|')]
        rows.append(row)
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Saved CSV table to {filename}")

def main():
    with open('Capetain-Cetriva/corporate_breakdown.md', 'r', encoding='utf-8') as f:
        md_text = f.read()

    data = parse_markdown(md_text)
    save_json(data)

    # Save AUM tables separately
    if 'AUM' in data:
        save_csv_from_table(data['AUM'], 'aum_data.csv')

if __name__ == '__main__':
    main()
