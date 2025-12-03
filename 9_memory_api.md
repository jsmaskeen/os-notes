Types of meory:
stack- allocations and deallocations are managed implicitly. So its called automatic memory.
heap- alloc and dealloc is handaled explicitly by the programmer.
`int *x = (int *) malloc(sizeof(int));`

here pointer to x is alloced on stack and x is on heap.
sizeof() is an operator not a function call. It is a compile time operator.

casting a malloc doesnt accomplish anything its just semantics.

free(p) frees a pointer p, however the memory manager must know how much to free.

forgetting to free memory -> memory leak

freeing memory before using it -> dangling pointer.

repeatedly freeing memory: double free, result is undefined.

