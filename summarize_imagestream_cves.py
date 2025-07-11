import argparse
import csv
import json
import os 
import subprocess 


def scan_images(args): 

	command_template = 'trivy image "{}" --scanners vuln --format json --output "{}"'
	with open(args.images_file, 'r') as file: 
		for idx, line in enumerate(file):
			line = line.strip()
			output_file = os.path.join(args.json_output_dir, f'result_{idx}.json')
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
				artifact_name = data.get("ArtifactName", None)				
				for result in data.get("Results", []):
					for vuln in result.get("Vulnerabilities", []):
						severity = vuln.get("Severity", "").upper()
						if severity in included_severities:
							critical_vulns.append({ 
								"ArtifactName": artifact_name,
								"VulnerabilityID": vuln.get("VulnerabilityID"),
								"PkgName": vuln.get("PkgName"),
								"InstalledVersion": vuln.get("InstalledVersion"),
								"FixedVersion": vuln.get("FixedVersion"),
								"Status": vuln.get("Status"),
								"Severity": severity,
								"Title": vuln.get("Title"),
								"PrimaryURL": vuln.get("PrimaryURL")
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
		"PkgName",
		"InstalledVersion",
		"FixedVersion",
		"Status",
		"Severity",
		"Title",
		"PrimaryURL",
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

	scan_images(args)
	vulns = extract_vulnerabilities(args)
	vulns = remove_duplicates(vulns) # function doesn't work
	write_summary(args, vulns)

if __name__ == "__main__":
	main()
