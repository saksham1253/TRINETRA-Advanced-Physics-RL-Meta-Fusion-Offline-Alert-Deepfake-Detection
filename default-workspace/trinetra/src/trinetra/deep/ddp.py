"""trinetra.deep.ddp — DistributedDataParallel launcher for Kaggle T4 x2 (max throughput path).

DataParallel (trinetra.deep.train) is the simple, reliable default. DDP is faster (one process per GPU, no
Python-GIL scatter/gather bottleneck) and is the recommended path for long runs. Use it from a plain `.py`
script (NOT after CUDA is already initialized in the notebook):

    from trinetra.deep.ddp import launch_ddp, is_main, ddp_sampler
    def worker(rank, world_size, args):
        setup done for you; build model -> DistributedDataParallel, loader with ddp_sampler(...), train.
    launch_ddp(worker, args)

Each rank trains on a disjoint shard; gradients are all-reduced automatically. Save/eval only on rank 0.
"""
from __future__ import annotations

import os

import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler


def ddp_setup(rank: int, world_size: int, backend: str = "nccl"):
    os.environ.setdefault("MASTER_ADDR", "127.0.0.1")
    os.environ.setdefault("MASTER_PORT", "29500")
    dist.init_process_group(backend, rank=rank, world_size=world_size)
    torch.cuda.set_device(rank)


def ddp_cleanup():
    if dist.is_initialized():
        dist.destroy_process_group()


def is_main() -> bool:
    return (not dist.is_initialized()) or dist.get_rank() == 0


def wrap_ddp(model, rank: int):
    return DDP(model.to(rank), device_ids=[rank], find_unused_parameters=False)


def ddp_sampler(dataset, shuffle: bool = True) -> DistributedSampler:
    return DistributedSampler(dataset, shuffle=shuffle)


def ddp_loader(dataset, batch_size: int, shuffle: bool = True, num_workers: int = 4) -> DataLoader:
    """Per-rank DataLoader with a DistributedSampler (each rank sees a disjoint shard)."""
    sampler = ddp_sampler(dataset, shuffle)
    return DataLoader(dataset, batch_size=batch_size, sampler=sampler, num_workers=num_workers,
                      pin_memory=True, persistent_workers=num_workers > 0, drop_last=shuffle)


def launch_ddp(worker, args, world_size: int | None = None):
    """Spawn one process per GPU. `worker(rank, world_size, args)` must call ddp_setup/ddp_cleanup itself,
    or wrap it with `ddp_worker` below which does setup/cleanup for you."""
    world_size = world_size or torch.cuda.device_count()
    if world_size < 2:
        # single device: just run inline on rank 0
        worker(0, max(world_size, 1), args)
        return
    mp.spawn(worker, args=(world_size, args), nprocs=world_size, join=True)


def ddp_worker(fn):
    """Decorator: wraps a `fn(rank, world_size, args)` with ddp_setup/ddp_cleanup and an all-reduce barrier."""
    def wrapped(rank, world_size, args):
        ddp_setup(rank, world_size)
        try:
            return fn(rank, world_size, args)
        finally:
            if dist.is_initialized():
                dist.barrier()
            ddp_cleanup()
    return wrapped
