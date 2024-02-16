## gunicorn.service file content

```bash
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/hosted_porjects/projectcodes
ExecStart=/root/hosted_porjects/projectcodes/python_virtual_envs/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          projectHub.wsgi:application

[Install]
WantedBy=multi-user.target
```

## nginx site config content

```bash
server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /root/hosted_porjects/projectcodes/static_cdn;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
