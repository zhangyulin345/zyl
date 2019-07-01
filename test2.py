from jpype import *
import os.path

startJVM("/usr/local/jdk1.8/jre/lib/amd64/server/libjvm.so", "-ea")
java.lang.System.out.println("hello World")
shutdownJVM()