# OrthancTeam/Orthanc

## Introduction

**Orthanc** is an open-source, lightweight DICOM server designed to manage medical images and associated data. Developed by the Orthanc Team, it aims to provide a simple, yet powerful solution for handling DICOM files, making it ideal for medical imaging research and clinical settings. Orthanc can be easily integrated into existing healthcare systems and provides a range of functionalities to manage, query, and retrieve medical images.

## Features

- **DICOM Store**: Efficiently store and manage DICOM files.
- **Web Interface**: User-friendly web interface for managing images and server configurations.
- **REST API**: Powerful RESTful API for integration with other software and automation of tasks.
- **Plugins**: Support for plugins to extend functionality.
- **Lightweight**: Minimal dependencies and easy to set up.
- **Cross-Platform**: Available for Windows, Linux, and macOS.
- **Open Source**: Licensed under the GPL, ensuring transparency and community-driven development.

## Installation

### Prerequisites

- Ensure you have a compatible operating system (Windows, Linux, macOS).
- Install dependencies:
  - For Linux: `sudo apt-get install orthanc`
  - For Windows/macOS: Download binaries from the [official Orthanc website](https://www.orthanc-server.com/).

### Quick Start

1. **Download and Extract**:

   - Download the latest version of Orthanc from the [official website](https://www.orthanc-server.com/).
   - Extract the downloaded files to your preferred location.

2. **Configuration**:

   - Navigate to the extracted folder.
   - Edit the `Configuration.json` file to suit your needs.

3. **Run Orthanc**:

   - Open a terminal or command prompt.
   - Navigate to the Orthanc directory.
   - Execute the command:
     ```sh
     ./Orthanc Configuration.json
     ```

4. **Access Web Interface**:
   - Open a web browser and go to `http://localhost:8042`.
   - You should see the Orthanc web interface where you can start managing your DICOM files.

## Usage

### Web Interface

The web interface provides an intuitive way to interact with Orthanc. You can:

- Upload and download DICOM files.
- View patient information, studies, and series.
- Manage server settings and plugins.

### REST API

Orthanc's REST API allows for advanced integrations and automations. Common endpoints include:

- **Retrieve Instances**: `GET /instances`
- **Upload Instances**: `POST /instances`
- **Query Patients**: `GET /patients`
- **Retrieve Studies**: `GET /studies`

Refer to the [API documentation](https://book.orthanc-server.com/users/rest.html) for detailed information on available endpoints and their usage.

## Plugins

Orthanc supports various plugins to extend its functionality. Popular plugins include:

- **Orthanc-PostgreSQL**: Store metadata in a PostgreSQL database.
- **Orthanc-WebViewer**: Integrate a web-based DICOM viewer.
- **Orthanc-WSI**: Handle whole slide images for digital pathology.

## Community and Support

Orthanc has a vibrant community of developers and users. You can find support and contribute in several ways:

- **Official Documentation**: Comprehensive guides and API documentation.
- **Community Forums**: Join discussions, ask questions, and share experiences.
- **GitHub Issues**: Report bugs or request features on the [GitHub repository](https://github.com/orthanc-team/orthanc).
- **Contribute**: Submit pull requests, improve documentation, or develop plugins.

## License

Orthanc is licensed under the GNU General Public License (GPL), ensuring it remains free and open-source. You are free to use, modify, and distribute Orthanc under the terms of the GPL.

## Conclusion

Orthanc is a robust and versatile DICOM server, perfect for managing medical imaging data in research and clinical environments. With its user-friendly interface, powerful API, and active community, Orthanc makes it easy to handle and integrate DICOM files into your workflows.

For more information, visit the [Orthanc official website](https://www.orthanc-server.com/) and explore the extensive [documentation](https://book.orthanc-server.com/).
