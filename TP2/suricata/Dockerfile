FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y suricata curl iproute2 tcpdump && \
    apt-get clean

COPY suricata.yaml /etc/suricata/suricata.yaml
COPY rules/ /etc/suricata/rules/

CMD ["suricata", "-i", "eth0", "-c", "/etc/suricata/suricata.yaml"]
