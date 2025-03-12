"""
Module Name: readXml2Enc.py
Author: Zhongxiao Cao
Date: 2025-3-9
Version: 1.0
Description: 
1、基于SM2非对称算法，读取xml中算法配置信息；
2、构造、加密并发送ESP数据包（传输模式）；
3、测试语音模块功能。
"""

import sys
import binascii
from base64 import b64encode, b64decode
from gmssl import sm2               # 加解密模块 - 国密SM2算法
from scapy.all import *             # 发包模块
import pyttsx3                      # 语音模块
import xml.etree.ElementTree as ET  # 读取xml配置文件模块


# 语音播报
def text_to_speech(text):
    # 初始化语音引擎
    engine = pyttsx3.init()
    
    # 设置参数（可选）
    engine.setProperty("rate", 150)    # 语速（默认约200）
    engine.setProperty("volume", 1.0)  # 音量（0.0~1.0）
    
    # 朗读文字
    engine.say(text)
    engine.runAndWait()


# 读取 XML 配置文件
def read_sm2_config(file_path):
    # file_path = "/Users/czx/Documents/Developer/1-PythonTest"
    tree = ET.parse(file_path)
    root = tree.getroot()

    config = {
        "private_key": root.find("private_key").text,
        "public_key": root.find("public_key").text,
        "plaintext": root.find("plaintext").text,
        "source_ip": root.find("ipsec/source_ip").text,
        "destination_ip": root.find("ipsec/destination_ip").text,
        "spi": int(root.find("ipsec/spi").text, 16),  # 转换为十六进制整数
        "seq": int(root.find("ipsec/seq").text),
    }
    return config


# SM2 加密
def sm2_encrypt(public_key, plaintext):
    sm2_crypt = sm2.CryptSM2(private_key=None, public_key=public_key)
    encrypted_data = sm2_crypt.encrypt(plaintext.encode('utf-8'))
    return encrypted_data


# 构造并发送 ESP 数据包
def send_esp_packet(source_ip, destination_ip, spi, seq, encrypted_data):
    ip = IP(src=source_ip, dst=destination_ip)
    esp = ESP(spi=spi, seq=seq, data=encrypted_data)
    packet = ip / esp
    send(packet)
    print("IPsec ESP packet sent!")



if __name__ == "__main__":
    # 读取配置文件
    config = read_sm2_config("sm2_config.xml")

    # 获取配置值
    private_key = config["private_key"]
    public_key = config["public_key"]
    plaintext = config["plaintext"]
    source_ip = config["source_ip"]
    destination_ip = config["destination_ip"]
    spi = config["spi"]
    seq = config["seq"]

    # 打印配置信息
    print("Private Key:", private_key)
    print("Public Key:", public_key)
    print("Plaintext:", plaintext)
    print("Source IP:", source_ip)
    print("Destination IP:", destination_ip)
    print("SPI:", hex(spi))
    print("Sequence Number:", seq)

    # 语音提示
    text2speech_read_plaintext = "您要加密的内容是:"
    text_to_speech(text2speech_read_plaintext)
    print("您要加密的内容是:", plaintext)

    print(" *** 开始加密 *** ")
    text2speech_start = "开始加密！"
    text_to_speech(text2speech_start)

    # SM2 加密
    encrypted_data = sm2_encrypt(public_key, plaintext)
    print(" === 加密结果 === ")
    print("Encrypted Data (Hex):", binascii.hexlify(encrypted_data).decode())

    # 发送 ESP 数据包（传输模式）
    print(" *** 开始发包 *** ")
    text2speech_send_packet = "开始发包！"
    text_to_speech(text2speech_send_packet)
    send_esp_packet(source_ip, destination_ip, spi, seq, encrypted_data)
    print(" === 发包结束 === ")