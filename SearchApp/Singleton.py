__author__ = 'I302581'


# Singleton Class Helper
#
# Usage:
# Method 1
# class MyClass(BaseClass):
# 	__metaclass__ = Singleton
#
# Method 2
# class MyClass(BaseClass, metaclass=Singleton):
# 	pass

class Singleton(type):
	def __init__(cls, name, bases, dict):
		super(Singleton, cls).__init__(name, bases, dict)
		cls._instance = None

	def __call__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instance