# -*- coding: utf-8 -*-
import gc
from dataclasses import dataclass

import torch

# from src_log.LoggerFactory import LoggerFactory
# logger1 = LoggerFactory.getLogger(__name__)

class FalseLogger:
    def info(self, *args, **kwargs):
        return print(*args, **kwargs)


logger1 = FalseLogger()


@dataclass
class MemoryStats:
    allocated: float  # in GB
    reserved: float  # in GB
    peak_allocated: float  # in GB
    peak_reserved: float  # in GB

    def __str__(self) -> str:
        return (
            f"[GPU-LEAK ?] Allocated: {self.allocated:.2f}GB "
            f"(Peak: {self.peak_allocated:.2f}GB) | "
            f"Reserved: {self.reserved:.2f}GB "
            f"(Peak: {self.peak_reserved:.2f}GB)"
        )


def bytes_to_gb(bytes_val: int) -> float:
    return bytes_val / (1024**3)


def get_gpu_memory_stats() -> MemoryStats | None:
    """Get current GPU memory statistics in GB."""
    if not torch.cuda.is_available():
        return None

    return MemoryStats(
        allocated=bytes_to_gb(torch.cuda.memory_allocated()),
        reserved=bytes_to_gb(torch.cuda.memory_reserved()),
        peak_allocated=bytes_to_gb(torch.cuda.max_memory_allocated()),
        peak_reserved=bytes_to_gb(torch.cuda.max_memory_reserved()),
    )


def log_gpu_memory(context: str = "") -> None:
    """Log current GPU memory usage with optional context."""
    stats = get_gpu_memory_stats()
    if stats:
        logger1.info(f"GPU Memory Usage {context}: {stats}")
    return stats


def measure_model_memory_impact(func):
    """Decorator to measure GPU memory impact of model loading/usage."""

    def wrapper(*args, **kwargs):
        # Clear any existing cached memory
        gc.collect()
        torch.cuda.empty_cache()

        # Measure before
        before_stats = get_gpu_memory_stats()
        if before_stats:
            logger1.info(f"GPU Memory before {func.__name__}: {before_stats}")

        # Run the function
        result = func(*args, **kwargs)

        # Measure after
        after_stats = get_gpu_memory_stats()
        if after_stats and before_stats:
            memory_impact = MemoryStats(
                allocated=after_stats.allocated - before_stats.allocated,
                reserved=after_stats.reserved - before_stats.reserved,
                peak_allocated=after_stats.peak_allocated - before_stats.peak_allocated,
                peak_reserved=after_stats.peak_reserved - before_stats.peak_reserved,
            )
            logger1.info(f"GPU Memory impact of {func.__name__}: {memory_impact}")

        return result

    return wrapper
