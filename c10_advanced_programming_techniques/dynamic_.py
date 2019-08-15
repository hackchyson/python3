import math

code = '''
def area_of_sphere(r):
    return 4 * math.pi * r ** 2
'''
context = {}
context["math"] = math
exec(code, context)

# If exec() is called with some code as its only argument there is no way to
# access any functions or variables that are created as a result of the code being
# executed. Furthermore, exec() cannot access any imported modules or any of
# the variables, functions, or other objects that are in scope at the point of the
# call. Both of these problems can be solved by passing a dictionary as the second
# argument. The dictionary provides a place where object references can be kept
# for accessing after the exec() call has finished. For example, the use of the
# context dictionary means that after the exec() call, the dictionary has an object
# reference to the area_of_sphere() function that was created by exec() . In this
# example we needed exec() to be able to access the math module, so we inserted
# an item into the context dictionary whose key is the module’s name and whose
# value is an object reference to the corresponding module object. This ensures
# that inside the exec() call, math.pi is accessible.


# In some cases it is convenient to provide the entire global context to exec() .
# This can be done by passing the dictionary returned by the globals() function.
# One disadvantage of this approach is that any objects created in the exec() call
# would be added to the global dictionary. A solution is to copy the global context
# into a dictionary, for example, context = globals().copy() . This still gives exec()
# access to imported modules and the variables and other objects that are in
# scope, and because we have copied, any changes to the context made inside the
# exec() call are kept in the context dictionary and are not propagated to the glob-
# al environment. (It would appear to be more secure to use copy.deepcopy() , but
# if security is a concern it is best to avoid exec() altogether.) We can also pass
# the local context, for example, by passing locals() as a third argument—this
# makes objects in the local scope accessible to the code executed by exec() .

area_of_sphere = context["area_of_sphere"]
area = area_of_sphere(5)
print(area)
