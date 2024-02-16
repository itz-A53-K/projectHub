## gunicorn.service file content

```bash
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/hosted_porjects
ExecStart=/root/hosted_porjects/python_virtual_envs/bin/gunicorn \
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
    server_name IP_ADDRESS;

    access_log off;

    location /static/ {
        alias /var/www/projectcodes/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
    }
}
```
