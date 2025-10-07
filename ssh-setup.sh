#!/bin/sh
# Configures a host ready to accept SSH connections to be centrallaly controlled via Ansible and Semaphore.
sudo bash -c 'apt-get update -y && apt-get install -y openssh-server && mkdir -p /root/.ssh && echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINSIKybfdS9Io3xfLaVjH5ERwU14KLCGdYINm7ADOSnS" >> /root/.ssh/authorized_keys && chmod 700 /root/.ssh && chmod 600 /root/.ssh/authorized_keys && systemctl enable --now ssh || systemctl enable --now sshd'
echo "Host ready for Semaphore!"
