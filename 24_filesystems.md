- Disk is divided into blocks, say from 0 to N-1
- A range is defined for the dta region. 
- THen we need to store the metadafa of each file with info as: size of while, which datablocks comprise the file, owner, access rights,access, and modify times. etc.
- We have to stoer the inode table that holds the array of on disk inodes.
- num of inodes = max number of files we can have.
- We need to track which inode or data regions are free, so we need a data bitmap and inode bitmap.
- The 0th block we have is the superblock. Contains info about the filesystem like how many inodes are there, how many datablocks are there, where the inode table begins, etc. It also hasa  magic number to identify the type of filesystem this is.
- SO while mounting, the OS will read the superblock first and then attach the bolume to file system tree.
- `stat/fstat <path> system call` tells what all info the filesystem has stored for that file.
- inode fullform is indexed node. Each ahs a number caled inumber.
- Given an inumber we can easliy get the address of the inode. 
- We can do `inode_tbl_start_addr + inodenumber*sizeof(inode)` to get the inode. But disks are blokc addressible.
- So to get the sector where inode is located, we do:
    - `blk = (inumber * sizeof(inode_t)) / blockSize;`
    - `sector = ((blk * blockSize) + inodeStartAddr) / sectorSize; = (inumber * sizeof(inode_t) + inodeStartAddr)/sectorSize;`
    - sectorSize is usaually 512B.
- inode in its datablock entires, has direct pointer, which point to the datablock containing the data.

Multi Level Index

- It also has an indirect pointer, which points to a datablock which contains addresses of datablocks of additional data.
- It can also have a double indirect pointer.
- Eg: datablock size 4KB, 4 byte pointers, so number of addresses we can store in the datablock = 4KB/4B = 1024.
- With 12 direct, 1 indirect adn 1 doubly indirect, we can have, $(12 + 1024 + 1024^2)*4$ KB of storage.
- why this approach ? cause most files are small

Another way is to use extents:
- extent is a disk pointer + length (in blocks)
- idea is rather than storing all the pointers for a contigous chunk, store extents. 
- but it is difficult to find a contigous free ondisk space. Hence should store multiple extents.
- these are less flexible but more compact.
- pointers are more flexible but require storing lot of metadata.
- extent are better if we can find contiguos space.

Directories:
- These are also files [special files]. they also have thir own inode number
- Store a list of (filename,name_len,inodenum) tuples.
- COntains 2 spcl entries, `.` (current dir) and `..` (parent dir).
- Deleting a file can cause holes in this list, hence the deleted files are given an inode number of 0.

Creating a file:
- Filesystem will ahve to first find a free inode, then mark it in the inode bitmap.
- Then if we write data, it will ahve to allocate blocks (so find frree bolcks using datablock bitmap)
- there are preallocation policies too like, heuristics while allocation datablocks, may try to allocate ateast 8 contiguos blocks.
