from pyo3_interior_mutability_experiment import PyOtherStruct, PyMyStruct

print("=== Basic PyOtherStruct mutation ===")
other_struct = PyOtherStruct(1)
print(f"Initial value: {other_struct.x}")
assert other_struct.x == 1, "Initial value should be 1"
other_struct.x = 2
print(f"After mutation: {other_struct.x}")
assert other_struct.x == 2, "Value should be updated to 2"
print(f"Representation: {repr(other_struct)}")

print("\n=== Mutation through reference sharing ===")
# Create a reference to the same object
ref1 = other_struct
ref2 = other_struct
print(f"ref1.x: {ref1.x}, ref2.x: {ref2.x}")
assert ref1.x == ref2.x == 2, "All references should have same value"
ref1.x = 3
print(f"After ref1.x = 3:")
print(f"ref1.x: {ref1.x}, ref2.x: {ref2.x}, other_struct.x: {other_struct.x}")
assert ref1.x == ref2.x == other_struct.x == 3, "All references should reflect the change"

print("\n=== PyMyStruct container test ===")
my_struct = PyMyStruct([other_struct])
items = my_struct.items_py
print(f"Container items: {items}")
print(f"First item x value: {items[0].x}")
assert items[0].x == other_struct.x, "Container item should reference the same object"

print("\n=== Mutation of object in container ===")
container_item = items[0]
container_item.x = 4
print(f"After container item mutation:")
print(f"container_item.x: {container_item.x}")
print(f"original object: {other_struct.x}")
print(f"from container: {my_struct.items_py[0].x}")
assert container_item.x == other_struct.x == my_struct.items_py[0].x == 4, "All references should reflect the change"

print("\n=== Multiple containers sharing objects ===")
struct1 = PyOtherStruct(10)
struct2 = PyOtherStruct(20)
container1 = PyMyStruct([struct1, struct2])
container2 = PyMyStruct([struct2])  # container2 shares struct2 with container1

print(f"Initial values:")
print(f"container1.items_py: {container1.items_py}")
print(f"container2.items_py: {container2.items_py}")
assert container1.items_py[1].x == container2.items_py[0].x == 20, "Shared object should have same value in both containers"

struct2.x = 25
print(f"\nAfter struct2.x = 25:")
print(f"container1.items_py: {container1.items_py}")
print(f"container2.items_py: {container2.items_py}")
assert container1.items_py[1].x == container2.items_py[0].x == 25, "Change should be visible in both containers"

print("\n=== Testing container representation ===")
print(f"Container repr: {repr(my_struct)}")

print("\n=== Iterating and modifying in-place ===")
# Create a collection of objects to iterate through
objects = [PyOtherStruct(i) for i in range(1, 6)]
print("Initial objects:")
for obj in objects:
    print(f"  {obj}")

# Create a container with these objects
collection = PyMyStruct(objects)

# Iterate and modify in-place
print("\nModifying each object by multiplying its x value by 10:")
for i, item in enumerate(collection.items_py):
    original_value = item.x
    item.x = original_value * 10
    print(f"  Item {i}: {original_value} → {item.x}")
    assert item.x == original_value * 10, f"Item {i} should be updated to {original_value * 10}"

# Verify changes are reflected in original objects
print("\nVerifying changes are reflected in original objects:")
for i, obj in enumerate(objects):
    expected = (i + 1) * 10
    print(f"  Object {i}: {obj}")
    assert obj.x == expected, f"Original object {i} should be updated to {expected}"

# Verify changes are reflected when accessing container items again
print("\nVerifying changes are reflected when accessing container items again:")
for i, item in enumerate(collection.items_py):
    expected = (i + 1) * 10
    print(f"  Container item {i}: {item}")
    assert item.x == expected, f"Container item {i} should be updated to {expected}"

print("\n=== All assertions passed! Interior mutability is working as expected ===")