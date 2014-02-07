kuaipan_backup
==============

incremental backup linux server to KuaiPan,using openssl encryption



使用了 https://github.com/deren/python-kuaipan ,谨致谢意。




部署方法：
1.修改backup.sh，修改要备份的目录，mysql密码，数据加密密码
2.获取consumer_key , consumer_secret ,oauth_token, oauth_token_secret ，并填入kp.py
  获取方法：
  1)在 http://www.kuaipan.cn/developers/list.htm 创建一个应用，得到 consumer_key 和 consumer_secret
  2)使用 https://github.com/deren/python-kuaipan 之中的KuaiPan_OAuth.py ，修改其中的 consumer_key 和 consumer_secret ，
    获取 oauth_token 和 oauth_token_secret 
  3)consumer_key , consumer_secret ,oauth_token, oauth_token_secret  填入kp.py
