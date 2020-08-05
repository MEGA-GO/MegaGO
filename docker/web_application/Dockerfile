# See https://github.com/phusion/passenger-docker for more information
FROM phusion/passenger-customizable:1.0.11
# Set correct environment variables.
ENV HOME /root

# Use baseimage-docker's init process.
CMD ["/sbin/my_init"]

RUN /pd_build/python.sh

#### Start of our own build instructions
# Add configuration for nginx and our flask app
RUN rm /etc/nginx/sites-enabled/default
ADD nginx.conf /etc/nginx/sites-enabled/webapp.conf

# Copy the flask files to the correct directory
RUN apt -y install python3-pip
RUN pip3 install flask
RUN git clone https://github.com/MEGA-GO/Mega-GO
RUN cd Mega-GO && git checkout feature/docker-container && pip3 install -U .
RUN mkdir -p /home/app/webapp && cd Mega-GO && mv api/* /home/app/webapp/
RUN chown -R app:app /home/app/webapp

# Remove this file to indicate that nginx can be started
RUN rm -f /etc/service/nginx/down
#### End of our own build instructions

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
