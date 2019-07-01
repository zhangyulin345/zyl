#-*-coding:utf-8-*-
import jpype
from jpype import *
#获得默认jvm路径，即jvm.dll文件路径
jvmPath = jpype.getDefaultJVMPath()
#java扩展包路径
ext_classpath = r'/home/zyl/eclipse-workspace/'
#jvmArg = '-Djava.class.path=%s'%ext_classpath
#print (jvmArg)
if not jpype.isJVMStarted():
    #启动Java虚拟机
    jpype.startJVM(jvmPath,'-ea',"-Djava.class.path=%s" % (ext_classpath + 'test.jar'))
    #startJVM(jvmPath, "-ea","-Djava.class.path=%s" % (ext_classpath + 'test.jar'))
#jpype.java.lang.System.out.println('Hello world!')
#获取相应的Java类
javaClass = JClass("com.javatest")
javaInstance = javaClass()
#调用Java方法
jprint = java.lang.System.out.println
jprint(javaInstance.run('123'))
jprint(javaInstance.testParam('zyl'))
#关闭jvm
jpype.shutdownJVM()