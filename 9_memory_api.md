# Memory API


## 1. Types of Memory
In C programming, there are two primary types of memory allocation:

### Stack Memory

* **Management (in C):** Allocations and deallocations are managed implicitly by the compiler.
* **Terminology:** Often referred to as **automatic memory**.
* **Note:** In other languages (e.g., C++), stack allocation is still managed by the compiler, but heap allocation can also be managed by the compiler or standard library (e.g., using `std::vector`).

### Heap Memory

* **Management (in C):** Allocation and deallocation are handled explicitly by the programmer.
* **Note:** In languages like C++, heap allocation can be managed by the compiler or standard library (e.g., containers such as `std::vector` automatically manage heap memory).

## 2. Allocation: `malloc()`

To allocate memory on the heap, we use `malloc()`.

```c
int *x = (int *) malloc(sizeof(int));
```

**Memory Layout:**

In the line of code above:

  * The pointer variable `x` itself is allocated on the **stack**.
  * The actual integer memory it points to is allocated on the **heap**.

**Details:**

  * **`sizeof()` Operator:** This is a **compile-time operator**, not a function call. It determines the size of the type at compile time.
  * **Casting:** Casting the result of `malloc` (e.g., `(int *)`) does not accomplish anything functional; it is purely semantics (and often unnecessary in modern C).

## 3. Deallocation: `free()`

To release heap memory, we use `free()`.

  * **Syntax:** `free(p)` frees the memory pointed to by `p`.
  * **Mechanism:** The memory manager tracks the size of the allocation internally, so it knows exactly how much memory to free.

## 4. Common Errors

Managing heap memory manually introduces several potential bugs:

1.  **Memory Leak:** Occurs when the programmer forgets to free memory.
2.  **Dangling Pointer:** This is a pointer that continues to reference a memory location after that memory has been deallocated (freed). Accessing or dereferencing a dangling pointer can result in undefined behavior, including crashes, data corruption, or security vulnerabilities, because the memory may now be used by other parts of the program or the operating system.
3.  **Double Free:** Occurs when `free()` is called repeatedly on the same pointer. The result of this operation is **undefined**.