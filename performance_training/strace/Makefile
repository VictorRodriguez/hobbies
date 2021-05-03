all:image

image:
	docker build -t sqlstrace .

strace:
	docker run \
    --name 'sql19strace'  -it  \
    -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD='$PASSWORD \
    -p 1433:1433 \
     sqlstrace /bin/bash -c "/usr/bin/strace -f /opt/mssql/bin/sqlservr"
