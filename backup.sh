#!/bin/bash
# 定期备份脚本
# 备份了：php程序，数据库，配置文件，重要日志

#用这个密码加密之后再上传
CRYPT_PSWD="back_it_UP"

MYSQL_PSWD="baby,your password"

#备份下面这些目录，文件
#每周全量备份一次，每天增量备份一次
DATA_DIR="/etc/nginx /etc/php /usr/share/nginx/html"


BACKUP_LOCAL_DIR="/tmp/data/"
SNAP_FILE="${BACKUP_LOCAL_DIR}/tar.snap"
UPLOAD="./kp.py upload "
LOG="./log.log"

now=$(date +%Y-%m-%d-%k_%M_%S |tr -d ' ')
BACKUP_LOCAL_DIR=$BACKUP_LOCAL_DIR$now
REMOTE_DIR="backup/"$now

function encrypt(){
## encrypt file ##
openssl aes-256-cbc -k $CRYPT_PSWD -salt -in $1   -out $2
}

function decrypt(){
## decrypt file ##
openssl aes-256-cbc -k $CRYPT_PSWD -d -in $1  -out $2
}


echo "begin backup at ${now}" >> ${LOG} 


mkdir -p $BACKUP_LOCAL_DIR

if [ "5" = $(date +%u) ]
then
    rm -f ${SNAP_FILE}
    echo "rm -f ${SNAP_FILE}" >> ${LOG} 
fi

#文件备份
(   tar --ignore-failed-read  --listed-incremental=${SNAP_FILE} -cvvvpf - $DATA_DIR | 
    openssl aes-256-cbc -k $CRYPT_PSWD |
    split -a 4 -b 64m - $BACKUP_LOCAL_DIR/data.${now}.tar.aes. 
)  >> ${LOG} 2>&1 
echo "end files backup at ${now}" >> ${LOG}

#mysql
sql=$BACKUP_LOCAL_DIR/db.${now}.sql
>$sql
mysqldump -A --single-transaction -u root $MYSQL_PSWD> $sql
gzip $sql
encrypt $sql.gz $sql.gz.aes
rm $sql.gz
echo "end mysql backup at ${now}" >> ${LOG}


${UPLOAD} $BACKUP_LOCAL_DIR/ $REMOTE_DIR >> ${LOG} 2>&1 
echo "end upload at ${now}" >> ${LOG} 
rm -rf $BACKUP_LOCAL_DIR/ 


echo "end all backup at ${now}" >> ${LOG}
