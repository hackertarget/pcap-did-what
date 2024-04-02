# Zeek & Grafana Integration for Network Monitoring
                                                                                                                      This repository provides a quick way to get started using Zeek in with a practical use case. The focus is to analyse a
 network pcap and enable easy visual analysis using Grafana Charts.                                                                                                                                                                         
The mini project consists of three parts.                                                                             
                                                                                                                      
1. Custom Zeek Docker build that generates zeek log files with GeoIP, ASN and JA3 / JA4 fingerprints.                 
                                                                                                                      
2. Python Script to convert zeek log files to an SQLite database.
                                                                                                                      
3. Custom Grafana Docker build with a pre-configured dashboard for analysing Zeek Data.                               
                                                                                                                      
Keeping this project simple and broken up into three parts should help both Zeek newcomers and those with more experience get up and running quickly. Working from these base images it would be an easy task to add other packages, and ext
end the dashboard to suit your own environment or use case. 

A two part article is available that goes into more detail about the project and getting started.

[Zeek with GeoIP, ASN & JA4 in 5 minutes](https://hackertarget.com/zeek-geoip-asn-ja4/)
[Zeek Dashboard using Grafana](https://hackertarget.com/zeek-dashboard-grafana/)


## Overview

The project is structured to use Docker containers for easy setup and scalability. It includes a customized Zeek conta
iner for log generation and a Grafana container for data visualization.


### File Structure

- **Dockerfile**: Located at `./pcap-did-what/zeek-docker/Dockerfile`, this file creates a Docker container based on the 
official Zeek image. It includes the installation of necessary packages for JA3 / JA4 fingerprinting and GeoIP, with a
 custom script for ASN enrichment.
- **local_asn.zeek**: `./pcap-did-what/zeek-docker/local_asn.zeek`, a small zeek script to add ASN information to the con
n.log. The script uses the builtin zeek function (lookup_autonomous_system).
- **docker-compose.yml**: Found in `./pcap-did-what/grafana-docker/docker-compose.yml`, this Docker Compose file sets up 
the Grafana container, configuring it to use a custom SQLite datasource and including volumes for persistent storage a
nd configuration.
- **dashboard.yml**: Located at `./pcap-did-what/grafana-docker/dashboards/dashboard.yml`, this configuration file specif
ies the dashboard provider settings for Grafana.
- **datasource.yml**: Found in `./pcap-did-what/grafana-docker/datasources/datasource.yml`, this file configures Grafana 
to use an SQLite database as the data source, pointing to the Zeek logs stored in SQLite format.

## Usage

To get started with this setup, ensure you have Docker and Docker Compose installed on your system. 

You will also need the MaxMind GeoIP and ASN databases, this requires registration (free) and a download of the two fi
les.

Follow these steps to deploy the environment:

1. **Clone this repository**

```git clone https://github.com/yourusername/pcap-did-what.git```

2. **Build Zeek Docker Image**

From the ./pcap-did-what/ build zeek image.

```cd zeek-docker
sudo docker build -t zeek-custom .```

Running the docker will drop you into bash. From bash it is possible to generate the zeek logs and convert them to sql
ite db.

```# zeek -C -r /data/test.pcap local
   # zeek-to-sqlite.py```

3. **Start the Grafana Container**
    
Use docker-compose to start the Grafana container:

```cd ../grafana-docker
sudo docker-compose up -d```


4. **Accessing Grafana:**
Once the containers are up and running, access the Grafana dashboard through your web browser:

```http://localhost:3000```

Use the default Grafana credentials (admin/admin) unless changed in the configuration. The dashboard should be loaded 
but there will be likely no data unless the zeek_log.db file has been generated and is in place.

## Customization and Notes

- You can modify the `Dockerfile` to include additional Zeek scripts or alter the existing configuration to suit your 
network analysis requirements.
- The Grafana dashboard and data source configurations can be adjusted in `dashboard.yml` and `datasource.yml` respect
ively, allowing for further customization of how data is displayed.
- zeek-to-sqlite.py uses a hardcoded /data/ path to match the build. Modify this as required.
- The local_asn.zeek script could be used to learn more about zeek scripting or extend it to populate other log files.


## Credits

Thanks to Zeek and Grafana for making high quality open source software. 

Also, thanks to Christos @ [Threat Hunting Tails](https://threathuntingtails.com/zeek-asn-enrichment/) for the ASN inf
ormation and asn.zeek script. 

