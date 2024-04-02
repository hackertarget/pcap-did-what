# Use the official Zeek image as a base
FROM zeek/zeek

# Install necessary tools for zkg (if needed) and the ja3 package
RUN zkg refresh && \
    zkg autoconfig --force

RUN zkg install ja3 --force && \
    zkg install zeek/foxio/ja4 --force && \
    zkg install geoip-conn --force

# Copy Maxmind GeoLite2 files (download from Maxmind with Free account)
COPY GeoLite2-City.mmdb /usr/share/GeoIP/
COPY GeoLite2-ASN.mmdb /usr/share/GeoIP/

COPY local_asn.zeek /usr/local/zeek/share/zeek/site/local_asn.zeek

# Python script to convert zeek logs to sqlite db
COPY zeek-to-sqlite.py /usr/local/bin/
RUN chmod +x /usr/local/bin/zeek-to-sqlite.py

# Add packages and local_asn script to local.zeek config
RUN echo "@load ja3" >> /usr/local/zeek/share/zeek/site/local.zeek
RUN echo "@load ja4" >> /usr/local/zeek/share/zeek/site/local.zeek
RUN echo "@load geoip-conn" >> /usr/local/zeek/share/zeek/site/local.zeek
RUN echo "@load local_asn" >> /usr/local/zeek/share/zeek/site/local.zeek

ENTRYPOINT ["/bin/bash"]
