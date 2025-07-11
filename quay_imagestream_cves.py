import argparse
import csv
import cvss
import json
import os 
import re
import subprocess 


def scan_images(args): 

	command_template = './clair/cmd/clairctl/clairctl report --out json "{}" > "{}"'
	with open(args.images_file, 'r') as file: 
		for idx, line in enumerate(file):
			line = line.strip()
			name = line.split('/')[2]
			output_file = os.path.join(args.json_output_dir, f'{name}.json')
			command = command_template.format(line, output_file)
			print(f'Running: {command}')
			command = subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	return None

def extract_vulnerabilities(args): 
	critical_vulns = [] 
	
	severities = {'crit,high': {"CRITICAL", "HIGH"}, 
				'crit': {"CRITICAL"}}
	included_severities = severities.get(args.severity, None)

	for filename in os.listdir(args.json_output_dir):
		if filename.endswith('.json'):
			with open(os.path.join(args.json_output_dir, filename), 'r') as f: 
				data = json.load(f)
				artifact_name = filename.split('.')[0]
				vulns = data.get("vulnerabilities", [])
				for v, vuln in vulns.items():
					severity = vuln.get("normalized_severity", "").upper()
					if severity in included_severities:
						try:
							score = max(cvss.CVSS3(vuln.get("severity")).scores())
						except:
							score = None

						try:
							conv_cve_name = re.findall(r'CVE-\d{4}-\d{4,7}', vuln.get("links"))[0]
						except:
							conv_cve_name = None
						cve_name = conv_cve_name if conv_cve_name else vuln.get("name")
						critical_vulns.append({ 
							"ArtifactName": artifact_name,
							"VulnerabilityID": vuln.get("name"),
							"ConvID": cve_name,
							"PkgName": vuln.get("package").get("name"),
							"InstalledVersion": vuln.get("InstalledVersion"),
							"FixedVersion": vuln.get("fixed_in_version"),
							"Severity": severity,
							"CalcSeverity": score,
						})
	return critical_vulns

def remove_duplicates(dict_list): 
	seen = set() 
	unique_dicts = [] 

	for d in dict_list: 
		dict_tuple = tuple(sorted(d.items()))
		if dict_tuple not in seen: 
			seen.add(dict_tuple) 
			unique_dicts.append(d) 

	return unique_dicts 

def write_summary(args, critical_vulns):
	fieldnames = [
		"ArtifactName",
		"VulnerabilityID",
		"ConvID",
		"PkgName",
		"InstalledVersion",
		"FixedVersion",
		"Severity",
		"CalcSeverity",
		]

	with open(args.output_summary_file, "w", encoding="utf-8") as csvfile: 
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(critical_vulns)

def main():
	parser = argparse.ArgumentParser(description="")

	parser.add_argument("--images-file", default="images.txt", help="text file of images to scan (default: images.txt)")
	parser.add_argument("--json-output-dir", default="json_outputs", help="folder for json output (default: json_outputs)") 
	parser.add_argument("--output-summary-file", default="summary.csv", help="summary file, path must exist (default: summary.csv)") 
	parser.add_argument("--severity", default="crit", help="levels to filter - i.e. crit,high (default: crit)") 

	args = parser.parse_args() 


	os.makedirs(args.json_output_dir, exist_ok=True)

	# scan_images(args)
	vulns = extract_vulnerabilities(args)
	# vulns = remove_duplicates(vulns) # function doesn't work
	write_summary(args, vulns)

if __name__ == "__main__":
	main()
