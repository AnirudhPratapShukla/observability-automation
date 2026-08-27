#!/bin/bash

HOSTS=(
    "host1|10.0.1.10|80|httpd"
    "host2|10.0.1.11|5672|rabbitMQ"
    "host3|10.0.1.12|5432|postgreSQL"
)

overall_status=0

printf "\n%-10s %-15s %-15s %-15s\n" "HOST" "SSH" "PORT" "SERVICE"
printf "%-10s %-15s %-15s %-15s\n" "----------" "---------------" "---------------" "---------------"

for entry in "${HOSTS[@]}"; do
    IFS='|' read -r host ip port service <<< "$entry"

    if ssh -o BatchMode=yes -o ConnectTimeout=3 "$ip" "exit" >/dev/null 2>&1; then
        ssh_status="REACHABLE"
    else
        ssh_status="UNREACHABLE"
        overall_status=1
    fi

    if nc -z -w 3 "$ip" "$port" >/dev/null 2>&1; then
        port_status="OPEN"
    else
        port_status="CLOSED"
    fi

    printf "%-10s %-15s %-15s %-15s\n" \
        "$host" "$ssh_status" "$port_status" "$service"
done

echo

if [ "$overall_status" -eq 0 ]; then
    echo "Pre-flight check PASSED."
else
    echo "Pre-flight check FAILED: one or more hosts are unreachable."
fi

exit "$overall_status"
