set -a
. "$(dirname "$0")/dev.env"
set +a

echo "/opt/netbox/netbox" > /opt/netbox/venv/lib/python3.12/site-packages/netbox.pth
echo "alias manage='python /opt/netbox/netbox/manage.py'" >> /etc/bash.bashrc
alias manage='python /opt/netbox/netbox/manage.py'

echo "--- installing pip ---"
curl -sS https://bootstrap.pypa.io/get-pip.py | /opt/netbox/venv/bin/python
python -m pip install -e .
if [ $? -eq 0 ]; then
    echo "--- finished ---"
else
    echo "--- failed to download pip ---"
    exit 1
fi

echo "--- copying Database Backup ---"
echo "host: $DB_BACKUP_HOST"
scp $DB_BACKUP_USER@$DB_BACKUP_HOST:$DB_BACKUP_DIRECTORY/$(ssh ''"$DB_BACKUP_USER@$DB_BACKUP_HOST"' ls -t '"$DB_BACKUP_DIRECTORY"'' | head -1) .devcontainer/db_backup.sql.gz
if [ $? -eq 0 ]; then
    echo "--- finished ---"
else
    echo "--- failed to copy Database Backup ---"
fi

if [ -f ".devcontainer/db_backup.sql.gz" ]; then
    echo "--- droping Database ---"
    echo "DROP DATABASE IF EXISTS $DB_NAME WITH (FORCE); CREATE DATABASE $DB_NAME" | docker compose -p store-data-plugin_devcontainer exec -T postgres sh -c 'psql -U '"$DB_USER"' template1' &
    docker_pid=$!
    wait $docker_pid
    exit_code=$?
    if [ $exit_code -eq 0 ]; then
        echo "--- finished ---"
    else
        echo "--- failed to drop database ---"
        exit 1
    fi

    echo "--- migrating Database Backup ---"
    gunzip -c .devcontainer/db_backup.sql.gz | docker compose -p store-data-plugin_devcontainer exec -T postgres sh -c 'psql -U '"$DB_USER $DB_NAME"'' &
    docker_pid=$!
    echo "--- Waiting for docker compose process (PID: $docker_pid) to complete ---"
    wait $docker_pid
    exit_code=$?
    if [ $exit_code -eq 0 ]; then
        echo "--- Database backup restored successfully ---"
    else
        echo "--- failed to migrate Database Backup (exit code: $exit_code) ---"
        exit 1
    fi
fi

echo "--- starting Database Migration ---"
manage migrate
if [ $? -ne 0 ]; then
    echo "--- migrate failed ---"
    exit 1
fi
manage makemigrations
if [ $? -ne 0 ]; then
    echo "--- makemigrations failed ---"
    exit 1
fi
manage collectstatic --no-input
if [ $? -ne 0 ]; then
    echo "--- collectstatic failed ---"
    exit 1
fi
echo "--- finished ---"

echo "--- creating Superuser ---"
DJANGO_SUPERUSER_PASSWORD=12345 manage createsuperuser --no-input --username super --email super@example.com
if [ $? -eq 0 ]; then
    echo "--- Superuser created successfully ---"
else
    echo "--- Note: Superuser creation failed (may already exist) ---"
fi

echo "--- starting Netbox ---"
manage runserver &
manage rqworker
echo "--- finished ---"

echo "--- waiting ---"
wait