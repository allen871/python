#!/usr/bin/python
#coding:utf-8

import os
path = "/tmp"

def enumeratepaths(path=path):
    """目录遍历"""
    path_collection = []
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            fullpath = os.path.join(dirpath, file)
            path_collection.append(fullpath)

    return path_collection

def enumeratefiles(path=path):
    """目录遍历"""
    file_collection = []
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            file_collection.append(file)

    return file_collection

if __name__ == '__main__':
    print enumeratepaths()