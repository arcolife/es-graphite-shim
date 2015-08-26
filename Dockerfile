# DEPLOYMENT INSTRUCTIONS

# To build the image, refer:
# docker build -t egs_shim .

# To run using the container, refer the following command:
# docker run --privileged -it -d \
#		-v /sys/fs/cgroup:/sys/fs/cgroup:ro \
#		-p 8000:8000 egs_shim

# this port should be same as one configured for the shim
###########################################################

FROM fedora:22
MAINTAINER arcolife <archit.py@gmail.com>

RUN dnf -y update && dnf clean all

# Install useful packages
RUN dnf install -y procps-ng tar wget vim gcc python3 python3-devel python3-gunicorn 
RUN dnf install -y mod_wsgi nginx && dnf clean all

RUN mkdir -p /opt/egs/egs/
ADD egs/ /opt/egs/egs/
RUN mkdir /opt/egs/logs/
COPY requirements.txt /opt/egs/
COPY conf/local_settings.py /opt/egs/egs/
RUN chmod a+x /opt/egs/egs/egs/wsgi.py

# for gunicorn socket
RUN mkdir /var/egs

WORKDIR /opt/egs
RUN pip3 install -r /opt/egs/requirements.txt
RUN easy_install-3.4 importlib

# add nginx configs
COPY conf/egs.conf.example /etc/nginx/conf.d/egs.conf
COPY conf/gunicorn.service /lib/systemd/system/gunicorn.service

# modify selinux policies and folder ownerships
RUN chown -R nginx:nginx /opt/egs/
RUN chown -R nginx:nginx /var/egs/

# add root password
RUN echo "root:egs_shim" | chpasswd

# add test page content
RUN echo "Shim test page" >> /var/www/html/index.html

# RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN echo "nginx on Fedora" > /usr/share/nginx/html/index.html

RUN systemctl enable nginx
RUN systemctl enable gunicorn

# Launch nginx
CMD [ "/usr/sbin/init" ]
