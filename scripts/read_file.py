# code for testing decorator chaining 
def decor1(func): 
	def inner(): 
		x = func() 
		return x * x 
	return inner 

def jeff(func): 
	def inner(): 
		x = func() 
		return 2 * x 
	return inner

class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)
	
class woman:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

@woman
class Student(Person, a_func):
  def __init__(self, fname, lname, year):
    super().__init__(fname, lname)
    self.graduationyear = year
	

def tim():
	print('yo')


@jeff
@decor1
def num2():
	return 10


@decor1
@jeff
def num(func):
    num2()
    func()
    return 10

print(num(tim)) 
print(num2())
