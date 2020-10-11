#!/bin/bash

echo '---' > vars.yml
for v in dev test qa prod 
	do
		echo "${v}-secret-pass" > ${v}_pass_file
		echo "This is the super secret data for ${v}" | ansible-vault encrypt_string --vault-id ${v}@${v}_pass_file --stdin-name env_${v}_pass >> vars.yml
	done
