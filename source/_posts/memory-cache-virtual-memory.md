---
title: 'Memory Systems: From SRAM Caches to TLBs'
date: 2026-05-03 14:20:00
categories:
  - article
tags:
  - computer systems
  - memory
  - cache
  - virtual memory
  - operating systems
math: true
---

Memory is not one uniform resource. A modern system combines several layers with different capacities, latencies, and addressing rules. This note connects the pieces: SRAM and DRAM, CPU caches, segmentation, paging, multi-level page tables, and the translation lookaside buffer (TLB).

## SRAM and DRAM

Static random-access memory (SRAM) is faster than dynamic random-access memory (DRAM), but it is also more expensive and less dense. That trade-off makes SRAM a good fit for small CPU caches such as L1, L2, and L3, while DRAM provides the larger main-memory pool.

The cache hierarchy works because programs tend to reuse recently accessed data and access nearby addresses. A small, fast layer can therefore hide much of the latency of a larger, slower layer.

## Cache organization

Most loads and stores pass through the cache hierarchy before reaching main memory. It is useful to keep instruction and data caches separate: code and data usually have different access patterns, and caching decoded instructions can avoid repeating front-end work.

### Processors, cores, and threads

A physical processor is a CPU package. A processor can contain multiple cores, and a core can expose multiple hardware threads. Different cores have separate execution resources, while hardware threads on one core share those resources and are scheduled by the operating system.

The number of logical CPUs can be estimated as

$$
\text{processors} \times \text{cores per processor} \times \text{threads per core}.
$$

Cache sharing often follows the same hierarchy. Cores generally have private L1 caches, may share an L2 cache, and may share a larger L3 cache within a processor. Separate processors do not necessarily share any cache directly.

### Address decomposition

A cache does not store a complete memory address in every line. It divides an address into an offset, an index, and a tag:

- The offset selects a byte within a cache line.
- The index selects a set.
- The tag identifies which memory region is currently stored in that set.

For a 32-bit address and a cache with 64-byte lines, 256 sets, and four lines per set:

1. A 64-byte line needs $\log_2 64 = 6$ offset bits.
2. 256 sets need $\log_2 256 = 8$ index bits.
3. The remaining $32 - 6 - 8 = 18$ bits form the tag.

In a four-way set-associative cache, the index chooses one set and the tag is compared with the four tags in that set. This gives more placement flexibility than a direct-mapped cache without the cost of comparing every line in the cache.

### Cache coherence

When multiple cores cache the same writable memory, they need a coherence protocol. A common write-invalidate design lets one core obtain ownership of a line for writing and causes other cached copies to become invalid. The next reader must then obtain the updated value. The exact protocol is hardware-specific, but the goal is the same: all cores must observe a coherent order of writes.

## Segmentation

Segmentation divides a process address space into logical regions. Each segment has a base and a bound (or limit), and the hardware checks that a logical offset stays within the segment before forming a physical address.

The heap commonly grows from lower addresses toward higher addresses, while the stack grows in the opposite direction. For example, if a heap begins at virtual address 4 KiB and a program accesses offset 4200, the offset inside the segment is

$$
4200 - 4096 = 104.
$$

With a base of 34 KiB, the resulting physical address is the base plus that checked offset.

An implementation can identify a segment explicitly, for example with selector bits, or implicitly from the pointer used to form the address. Segmentation can suffer from external fragmentation, so the operating system may need to compact or otherwise manage free regions carefully.

The allocator also needs to remember how large an allocation is when the caller later invokes `free(ptr)`. A common approach is to place a small header immediately before the user-visible payload. The header stores the size and allocator metadata, so the allocator can recover the chunk boundaries from the pointer alone.

## Paging

Paging replaces variable-sized logical segments with fixed-size pages. A process's virtual address space is split into pages, and physical memory is split into same-sized frames. The operating system maps virtual pages to physical frames through a page table.

For a page size of $2^p$ bytes, a virtual address can be written as

$$
\text{virtual address} = (\text{VPN},\ \text{offset}),
$$

where the offset is the lower $p$ bits. The page table translates the virtual page number (VPN) into a physical frame number (PFN). The offset is then copied unchanged:

$$
\text{physical address} = (\text{PFN},\ \text{offset}).
$$

Page tables are normally per-process. The CPU keeps a pointer to the current process's page-table root, so the same virtual address can map to different physical frames in different processes.

### Multi-level page tables

A single, flat page table can be large even when a process uses only a small portion of its address space. A multi-level page table splits the virtual address into several indexes and one offset. Each index selects an entry in the next-level directory until the last level identifies the physical frame.

For example, a virtual address divided into four indexes and one offset uses a four-level page table. The extra levels add page-table walks on a miss, but they let the operating system allocate lower-level tables only for regions that are actually in use.

As the number of levels increases, a page-table walk becomes more expensive. That is why address translation is normally cached.

### A large-page example

On a 32-bit machine using 4 MiB pages, the lower 22 bits are the page offset because $2^{22}=4$ MiB. The upper 10 bits select one of the 1024 entries in the page directory. The selected entry supplies the physical page's base, which is combined with the 22-bit offset.

This is different from the more common 4 KiB two-level layout, where the address is split into a 10-bit page-directory index, a 10-bit page-table index, and a 12-bit offset.

## TLBs

The translation lookaside buffer is a small cache of recent VPN-to-PFN translations. On a TLB hit, the CPU can combine the cached PFN with the original offset immediately. On a miss, hardware or the operating system performs a page-table walk and then usually inserts the result into the TLB.

Without address-space tags, changing processes requires invalidating translations that belong to the old page table. Modern systems can use tags such as ASIDs or PCIDs to keep translations from different address spaces distinct and reduce the amount of flushing required during a context switch.

## Putting it together

Caches optimize access to physical data. Paging translates virtual pages into physical frames, and the TLB caches those translations so that the translation step does not become the new bottleneck. Segmentation explains an older logical-address model, while paging provides the fixed-size mapping used by most modern operating systems.

The common theme is indirection with locality: keep the frequently used metadata and data close to the CPU, and use compact indexes to find the larger backing store only when necessary.

## Further reading

- [CPU and Memory](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf)
