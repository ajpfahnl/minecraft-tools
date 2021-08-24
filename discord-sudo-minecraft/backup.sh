#!/bin/bash

server_dir=$(sed -n 's/^SERVER-DIRECTORY=//p' .env)
server_dir="${server_dir/#\~/$HOME}"
backup_dir=$(sed -n 's/^BACKUP-DIRECTORY=//p' .env)
backup_dir="${backup_dir/#\~/$HOME}"
backup_partial_path="${backup_dir}my_minecraft_server-V"
[ ! -d "${server_dir}" ] && { echo "Server directory \"${server_dir}\" does not exist."; exit 1; }
[ ! -d "${backup_dir}" ] && { echo "Backup directory \"${backup_dir}\" does not exist."; exit 1; }
i=0
while [ -d "${backup_partial_path}${i}" ]
do
	let i++
done
echo "${backup_partial_path}${i}"
cp -r "${server_dir}" "${backup_partial_path}${i}"
