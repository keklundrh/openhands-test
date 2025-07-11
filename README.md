# Container Image CVE Scanner

A Python-based tool for scanning container images for Common Vulnerabilities and Exposures (CVEs) using multiple vulnerability scanners. This repository provides scripts to scan images listed in a file and generate comprehensive vulnerability reports.

## Features

- **Multiple Scanner Support**: Choose between Clair and Trivy vulnerability scanners
- **Severity Filtering**: Filter vulnerabilities by severity levels (Critical, High, etc.)
- **Batch Processing**: Scan multiple images from a text file input
- **CSV Output**: Generate structured CSV reports for easy analysis
- **JSON Intermediate Storage**: Store detailed scan results in JSON format
- **Duplicate Detection**: Built-in functionality to identify and handle duplicate vulnerabilities

## Scripts

### `quay_imagestream_cves.py`
Uses Clair (clairctl) to scan container images for vulnerabilities. Provides detailed vulnerability information including CVSS scores.

### `summarize_imagestream_cves.py`
Uses Trivy to scan container images for vulnerabilities. Offers comprehensive vulnerability details with status information.

## Prerequisites

### For Clair Scanner (`quay_imagestream_cves.py`)
- [Clair](https://github.com/quay/clair) vulnerability scanner
- `clairctl` command-line tool installed and accessible in `./clair/cmd/clairctl/`

### For Trivy Scanner (`summarize_imagestream_cves.py`)
- [Trivy](https://github.com/aquasecurity/trivy) vulnerability scanner
- `trivy` command available in PATH

### Python Dependencies
```bash
pip install cvss
```

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

3. Install your preferred vulnerability scanner:
   - **For Clair**: Follow the [Clair installation guide](https://github.com/quay/clair)
   - **For Trivy**: Follow the [Trivy installation guide](https://aquasecurity.github.io/trivy/latest/getting-started/installation/)

## Usage

### Input File Format

Create a text file (default: `images.txt`) with one container image per line:
```
registry.example.com/namespace/image:tag
quay.io/organization/app:latest
docker.io/library/nginx:alpine
```

### Using Clair Scanner

```bash
python quay_imagestream_cves.py [OPTIONS]
```

**Options:**
- `--images-file`: Text file containing images to scan (default: `images.txt`)
- `--json-output-dir`: Directory for JSON output files (default: `json_outputs`)
- `--output-summary-file`: Path for CSV summary file (default: `summary.csv`)
- `--severity`: Severity levels to include - `crit` or `crit,high` (default: `crit`)

**Example:**
```bash
python quay_imagestream_cves.py --images-file my_images.txt --severity crit,high --output-summary-file vulnerabilities.csv
```

### Using Trivy Scanner

```bash
python summarize_imagestream_cves.py [OPTIONS]
```

**Options:**
- `--images-file`: Text file containing images to scan (default: `images.txt`)
- `--json-output-dir`: Directory for JSON output files (default: `json_outputs`)
- `--output-summary-file`: Path for CSV summary file (default: `summary.csv`)
- `--severity`: Severity levels to include - `crit` or `crit,high` (default: `crit`)

**Example:**
```bash
python summarize_imagestream_cves.py --images-file containers.txt --json-output-dir scan_results --output-summary-file report.csv
```

## Output Format

### CSV Report Fields

**Clair Scanner Output:**
- `ArtifactName`: Name of the scanned image
- `VulnerabilityID`: Unique vulnerability identifier
- `ConvID`: Conventional CVE identifier (if available)
- `PkgName`: Affected package name
- `InstalledVersion`: Currently installed package version
- `FixedVersion`: Version that fixes the vulnerability
- `Severity`: Vulnerability severity level
- `CalcSeverity`: Calculated CVSS score

**Trivy Scanner Output:**
- `ArtifactName`: Name of the scanned image
- `VulnerabilityID`: Unique vulnerability identifier
- `PkgName`: Affected package name
- `InstalledVersion`: Currently installed package version
- `FixedVersion`: Version that fixes the vulnerability
- `Status`: Vulnerability status
- `Severity`: Vulnerability severity level
- `Title`: Vulnerability title/description
- `PrimaryURL`: Link to vulnerability details

## Directory Structure

```
.
├── README.md
├── LICENSE
├── quay_imagestream_cves.py      # Clair-based scanner
├── summarize_imagestream_cves.py # Trivy-based scanner
├── images.txt                    # Input file (create this)
├── json_outputs/                 # JSON scan results (auto-created)
└── summary.csv                   # CSV report output
```

## Severity Levels

- `crit`: Include only CRITICAL vulnerabilities
- `crit,high`: Include both CRITICAL and HIGH severity vulnerabilities

## Known Issues

- The duplicate removal function in `quay_imagestream_cves.py` is currently disabled due to functionality issues
- Ensure proper permissions and network access for container image scanning

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
1. Check existing issues in the repository
2. Create a new issue with detailed information about your problem
3. Include sample input files and error messages when applicable
