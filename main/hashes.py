# -*- coding: utf-8 -*-
import hashlib
import uuid


def gen_hashstr(value):
    salt = uuid.uuid4().hex
    return hashlib.sha1(salt.encode() + value.encode()).hexdigest() + ':' + salt
