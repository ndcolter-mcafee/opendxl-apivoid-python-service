# Base image from Python 2.7 (slim)
FROM python:2.7-slim

VOLUME ["/opt/dxlapivoidservice-config"]

# Copy application files
COPY . /tmp/build
WORKDIR /tmp/build

# Clean application
RUN python ./clean.py

# Install application package and its dependencies
RUN pip install .

# Cleanup build
RUN rm -rf /tmp/build

################### INSTALLATION END #######################
#
# Run the service.
#
# NOTE: The configuration files for the service must be
#       mapped to the path: /opt/dxlapivoidservice-config
#
# For example, specify a "-v" argument to the run command
# to mount a directory on the host as a data volume:
#
#   -v /host/dir/to/config:/opt/dxlapivoidservice-config
#
CMD ["python", "-m", "dxlapivoidservice", "/opt/dxlapivoidservice-config"]
