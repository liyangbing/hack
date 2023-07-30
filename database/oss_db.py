import oss2
from typing import Optional

import config.config as config

class OSSDB:
    def __init__(self, access_key_id: str, access_key_secret: str, endpoint: str, bucket_name: str, file_prefix: str = ''):
        self.bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
        self.endpoint = endpoint
        self.bucket_name = bucket_name
        self.file_prefix = file_prefix

    def upload_file(self, local_file_path: str, oss_file_name: Optional[str] = None):
        if not oss_file_name:
            oss_file_name = local_file_path.split('/')[-1]
        oss_file_name = self.file_prefix + oss_file_name

        # 使用阿里云OSS的put_object_from_file方法，上传本地文件
        self.bucket.put_object_from_file(oss_file_name, local_file_path)
        
        # 修改文件权限为公共读
        self.bucket.put_object_acl(oss_file_name, oss2.OBJECT_ACL_PUBLIC_READ)

        # 返回文件的访问链接
        return f"https://{self.bucket_name}.{self.endpoint}/{oss_file_name}"