import base64
import zlib
from typing import Union

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

IV = b"abcd134556abcedf"
def _decrypt(data: bytes, key: bytes, iv: bytes = IV) -> bytes:
    """pycryptodomex库解密"""
    cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    plaintext = cipher.decrypt(bytes.fromhex(data.decode()))
    result = unpad(plaintext, AES.block_size)
    return result

def unzip(base64data: Union[str, bytes]) -> bytes:
    """
    使用python中zlib模块使用window中的系统缓存区进行解压缩
    :param base64data: 字符
    :param -zlib.MAX_WBITS: window系统缓存区的大小
    :param bytearray(): 把变为二进制字节数组的序列
    :param decompress(): 解压缩
    :return:
    """
    return zlib.decompress(bytearray(ord(i) for i in base64.b64decode(base64data).decode()), -zlib.MAX_WBITS)


def decrypt_doc_id(doc_id: str, key: bytes) -> str:
    result = unzip(doc_id)
    for _ in range(2):
        result = _decrypt(result, key)

    return result.decode()










