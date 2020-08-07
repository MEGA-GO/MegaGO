# See https://github.com/phusion/passenger-docker for more information
FROM phusion/passenger-customizable:1.0.11
# Set correct environment variables.
ENV HOME /root

# Use baseimage-docker's init process.
CMD ["/sbin/my_init"]

RUN /pd_build/python.sh
RUN /pd_build/nodejs.sh

#### Start of our own build instructions
# Add configuration for nginx and our flask app
RUN rm /etc/nginx/sites-enabled/default
ADD nginx.conf /etc/nginx/sites-enabled/webapp.conf

# Copy the flask files to the correct directory
RUN apt -y install python3-pip
RUN pip3 install flask flask_cors
RUN git clone https://github.com/MEGA-GO/Mega-GO

# Install MegaGO as a PiP package from local source
RUN cd Mega-GO && pip3 install -U .
RUN mkdir -p /home/app/webapp/api && cd Mega-GO && mv api/* /home/app/webapp/api

# Build frontend and move newly generated files
RUN cd Mega-GO/web && npm install && npm run build && mv dist/* /home/app/webapp

RUN chown -R app:app /home/app/webapp

# Generate a self-signed certificate for the image that acts as a placeholder for a real SSL certificate that can
# optionally be provided.
RUN openssl req -x509 -newkey rsa:4096 -keyout private_key.pem -out certificate.pem -days 1825 -nodes -subj "/C=BE/ST=East-Flanders/L=Ghent/O=MegaGO/OU=NA/CN=localhost"
RUN mkdir -p /home/app/certificates && mv *.pem /home/app/certificates

# Remove this file to indicate that nginx can be started
RUN rm -f /etc/service/nginx/down
#### End of our own build instructions

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
