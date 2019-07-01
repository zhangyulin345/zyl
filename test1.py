#!/usr/bin/env python
# -*- coding:UTF-8 -*-
from jpype import *
import os.path
#jarpath='/home/zyl/eclipse-workspace/JavaPyTest/src/JavaPyTest/'
jarpath = os.path.join(os.path.abspath('.'), '/home/zyl/eclipse-workspace/')
#jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.ext.dirs=%s" % jarpath)
startJVM("/usr/local/jdk1.8/jre/lib/amd64/server/libjvm.so", "-ea","-Djava.class.path=%s" % (jarpath + 'JavaPyTest.jar'))
javaClass = JClass("JavaPyTest.JavaPyTest")
#javaClass = jpype.JClass('JavaPyTest.JavaPyTest')
javaInstance = javaClass()
sum1= javaInstance.getSum(10, 20)
print (sum1)
str1 = javaInstance.getString("getString")
print(str1)
shutdownJVM()
