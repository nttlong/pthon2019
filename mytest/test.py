from mytest import pkg1
from mytest import pkg2

pkg1.set_my_var("X")
print(pkg1.my_var)
print(pkg2.my_var)
pkg2.set_my_var("Y")
print(pkg1.my_var)
print(pkg2.my_var)