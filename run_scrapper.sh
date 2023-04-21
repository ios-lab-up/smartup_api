#!/bin/bash

echo "Running scrapper script..."

python -c "from App.school.scrapper.utils import extractUPSiteSchedule; from school.config import Config; extractUPSiteSchedule(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)"

echo "Scrapper script completed."
