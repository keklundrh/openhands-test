# Container Image CVE Scanner

A Python toolkit for scanning container images for Common Vulnerabilities and Exposures (CVEs) using multiple security scanners. This repository provides scripts to scan images listed in a file and generate comprehensive vulnerability reports.

## Features

- **Multiple Scanner Support**: Supports both Clair and Trivy vulnerability scanners
- **Batch Processing**: Scan multiple container images from a list file
- **Severity Filtering**: Filter vulnerabilities by severity levels (Critical, High)
- **CSV Output**: Generate structured CSV reports for easy analysis
- **Duplicate Removal**: Remove duplicate vulnerability entries
- **CVSS Scoring**: Calculate CVSS scores for vulnerabilities (Clair scanner)

## Requirements

### Dependencies

- Python 3.6+
- Required Python packages:
  - `cvss` (for CVSS score calculation)
  - Standard library modules: `argparse`, `csv`, `json`, `os`, `re`, `subprocess`

### External Tools

- **For Clair scanning**: [Clair](https://github.com/quay/clair) with `clairctl` command-line tool
- **For Trivy scanning**: [Trivy](https://github.com/aquasecurity/trivy) scanner

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install Python dependencies:
   ```bash
   pip install cvss
   ```

3. Install external scanners:
   - **Clair**: Follow the [Clair installation guide](https://github.com/quay/clair)
   - **Trivy**: Follow the [Trivy installation guide](https://aquasecurity.github.io/trivy/latest/getting-started/installation/)

## Usage

### Clair Scanner (`quay_imagestream_cves.py`)

Scan container images using Clair and generate a vulnerability report:

```bash
python quay_imagestream_cves.py [OPTIONS]
```

**Options:**
- `--images-file`: Text file containing list of images to scan (default: `images.txt`)
- `--json-output-dir`: Directory for JSON output files (default: `json_outputs`)
- `--output-summary-file`: Path for CSV summary file (default: `summary.csv`)
- `--severity`: Severity levels to include - `crit` or `crit,high` (default: `crit`)

**Example:**
```bash
python quay_imagestream_cves.py --images-file my_images.txt --severity crit,high --output-summary-file vulnerabilities.csv
```

### Trivy Scanner (`summarize_imagestream_cves.py`)

Scan container images using Trivy and generate a vulnerability report:

```bash
python summarize_imagestream_cves.py [OPTIONS]
```

**Options:**
- `--images-file`: Text file containing list of images to scan (default: `images.txt`)
- `--json-output-dir`: Directory for JSON output files (default: `json_outputs`)
- `--output-summary-file`: Path for CSV summary file (default: `summary.csv`)
- `--severity`: Severity levels to include - `crit` or `crit,high` (default: `crit`)

**Example:**
```bash
python summarize_imagestream_cves.py --images-file my_images.txt --severity crit,high --output-summary-file trivy_report.csv
```

## Input Format

Create a text file (e.g., `images.txt`) with one container image per line:

```
registry.redhat.io/ubi8/ubi:latest
quay.io/organization/image:tag
docker.io/library/nginx:alpine
```

## Output Format

Both scripts generate CSV files with vulnerability information:

### Clair Output Fields
- `ArtifactName`: Container image name
- `VulnerabilityID`: CVE or vulnerability identifier
- `ConvID`: Conventional CVE name (if available)
- `PkgName`: Affected package name
- `InstalledVersion`: Currently installed version
- `FixedVersion`: Version that fixes the vulnerability
- `Severity`: Vulnerability severity level
- `CalcSeverity`: Calculated CVSS score

### Trivy Output Fields
- `ArtifactName`: Container image name
- `VulnerabilityID`: CVE identifier
- `PkgName`: Affected package name
- `InstalledVersion`: Currently installed version
- `FixedVersion`: Version that fixes the vulnerability
- `Status`: Vulnerability status
- `Severity`: Vulnerability severity level
- `Title`: Vulnerability title/description
- `PrimaryURL`: Link to vulnerability details

## Examples

### Basic Usage

1. Create an `images.txt` file:
   ```
   registry.redhat.io/ubi8/ubi:latest
   quay.io/myorg/myapp:v1.0
   ```

2. Run Trivy scanner:
   ```bash
   python summarize_imagestream_cves.py --images-file images.txt --severity crit,high
   ```

3. View results in `summary.csv`

### Advanced Usage

Scan with custom output directory and filename:

```bash
python summarize_imagestream_cves.py \
  --images-file production_images.txt \
  --json-output-dir ./scan_results \
  --output-summary-file ./reports/production_vulnerabilities.csv \
  --severity crit,high
```

## Notes

- The Clair scanner script has the `scan_images()` function commented out by default
- The duplicate removal function is noted as not working properly in both scripts
- Ensure the output directory exists before running the scripts
- Large image scans may take considerable time to complete

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
1. Check existing issues in the repository
2. Create a new issue with detailed information about your problem
3. Include relevant error messages and system information
