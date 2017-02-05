Monitor WiFi

Monitor the WiFi connection and if the connection fails, restart it up to 5 times. If it's still down, restart the RPi

Schedule this by adding to root crontab: sudo crontab -e

@reboot /home/???/thermostat-monitorwifi.py

