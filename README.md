# Container Image CVE Scanner

A Python toolkit for scanning container images for Common Vulnerabilities and Exposures (CVEs) using multiple security scanners. This repository provides scripts to scan images listed in a file and generate comprehensive vulnerability reports with support for both Clair and Trivy vulnerability scanners.

To see how it's done, jump straight to [installation](#install).

## Table of contents

- [Detailed description](#detailed-description)
- [See it in action](#see-it-in-action)
- [Architecture diagrams](#architecture-diagrams)
- [References](#references)
- [Requirements](#requirements)
  - [Minimum hardware requirements](#minimum-hardware-requirements)
  - [Required software](#required-software)
  - [Required permissions](#required-permissions)
- [Install](#install)
- [Uninstall](#uninstall)

## Detailed description

The Container Image CVE Scanner is a comprehensive Python toolkit designed to identify security vulnerabilities in container images. It provides automated scanning capabilities using industry-standard vulnerability scanners (Clair and Trivy) to help organizations maintain secure container deployments.

Key capabilities include:
- **Multiple Scanner Support**: Supports both Clair and Trivy vulnerability scanners for comprehensive coverage
- **Batch Processing**: Scan multiple container images from a list file for efficient bulk operations
- **Severity Filtering**: Filter vulnerabilities by severity levels (Critical, High) to focus on the most important issues
- **CSV Output**: Generate structured CSV reports for easy analysis and integration with other tools
- **CVSS Scoring**: Calculate CVSS scores for vulnerabilities when using the Clair scanner
- **Flexible Configuration**: Customizable output directories, file names, and scanning parameters

### See it in action

1. **Basic Scanning**: Create an `images.txt` file with container images and run the scanner:
   ```bash
   python summarize_imagestream_cves.py --images-file images.txt --severity crit,high
   ```

2. **Advanced Usage**: Scan with custom output directory and filename:
   ```bash
   python summarize_imagestream_cves.py \
     --images-file production_images.txt \
     --json-output-dir ./scan_results \
     --output-summary-file ./reports/production_vulnerabilities.csv \
     --severity crit,high
   ```

3. **Results Analysis**: View the generated CSV reports containing detailed vulnerability information including CVE IDs, affected packages, severity levels, and fix versions.

### Architecture diagrams

The Container Image CVE Scanner follows a simple pipeline architecture:

```
[Image List] → [Scanner (Clair/Trivy)] → [JSON Output] → [CSV Report]
```

*Note: Architecture diagrams will be added to the `assets/images` folder in future updates.*

### References

- [Clair Vulnerability Scanner](https://github.com/quay/clair) - Static analysis of vulnerabilities in application containers
- [Trivy Scanner](https://github.com/aquasecurity/trivy) - A Simple and Comprehensive Vulnerability Scanner for Containers
- [CVSS Scoring](https://www.first.org/cvss/) - Common Vulnerability Scoring System
- [Container Security Best Practices](https://kubernetes.io/docs/concepts/security/) - Kubernetes security documentation
- [NIST Container Security Guide](https://csrc.nist.gov/publications/detail/sp/800-190/final) - Application Container Security Guide

## Requirements

### Minimum hardware requirements

- **CPU**: 2 cores minimum, 4 cores recommended for large-scale scanning
- **Memory**: 4GB RAM minimum, 8GB recommended for processing large images
- **Storage**: 10GB free disk space for temporary files and scan results
- **Network**: Internet connectivity required for downloading vulnerability databases and accessing container registries

### Required software

- **Python**: Version 3.6 or higher
- **Python packages**:
  - `cvss` (for CVSS score calculation with Clair scanner)
  - Standard library modules: `argparse`, `csv`, `json`, `os`, `re`, `subprocess`
- **Container Scanners** (choose one or both):
  - **Clair**: [Installation guide](https://github.com/quay/clair) with `clairctl` command-line tool
  - **Trivy**: [Installation guide](https://aquasecurity.github.io/trivy/latest/getting-started/installation/)
- **Container Runtime**: Docker or Podman for accessing container images

### Required permissions

- **File System**: Read/write permissions to the working directory for creating output files and temporary data
- **Network Access**: Ability to pull container images from registries (may require registry authentication)
- **Container Registry Access**: Appropriate credentials for private registries if scanning private images
- **Scanner Permissions**: Execution permissions for Clair/Trivy binaries and their dependencies

## Install

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd container-image-cve-scanner
   ```

2. **Install Python dependencies**:
   ```bash
   pip install cvss
   ```

3. **Install vulnerability scanners**:

   **For Clair scanning**:
   - Follow the [Clair installation guide](https://github.com/quay/clair)
   - Ensure `clairctl` is available in your PATH

   **For Trivy scanning**:
   - Follow the [Trivy installation guide](https://aquasecurity.github.io/trivy/latest/getting-started/installation/)
   - Verify installation: `trivy --version`

4. **Prepare your image list**:
   Create a text file (e.g., `images.txt`) with one container image per line:
   ```
   registry.redhat.io/ubi8/ubi:latest
   quay.io/organization/image:tag
   docker.io/library/nginx:alpine
   ```

5. **Create output directory**:
   ```bash
   mkdir -p json_outputs
   ```

6. **Run your first scan**:
   ```bash
   python summarize_imagestream_cves.py --images-file images.txt --severity crit,high
   ```

## Uninstall

1. **Remove the repository**:
   ```bash
   rm -rf /path/to/container-image-cve-scanner
   ```

2. **Uninstall Python dependencies** (if not used by other projects):
   ```bash
   pip uninstall cvss
   ```

3. **Remove vulnerability scanners** (optional):
   - **Clair**: Follow the uninstallation steps from the Clair documentation
   - **Trivy**: Remove the Trivy binary from your system PATH

4. **Clean up output files**:
   ```bash
   rm -rf json_outputs/
   rm -f summary.csv
   rm -f *.json
   ```
