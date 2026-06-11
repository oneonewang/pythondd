"""Ex01 测试。"""
import time

from .ex01_gil_and_threading import (
    ThreadLocalStorage,
    counter_unsafe,
    counter_with_lock,
    parallel_speedup,
    run_io_tasks,
    run_serial,
)


class TestRunIoTasks:
    def test_results_match(self) -> None:
        tasks = [(0.01, "a"), (0.01, "b"), (0.01, "c")]
        assert sorted(run_io_tasks(tasks)) == ["a", "b", "c"]

    def test_actually_parallel(self) -> None:
        tasks = [(0.05, i) for i in range(4)]
        start = time.perf_counter()
        run_io_tasks(tasks, max_workers=4)
        elapsed = time.perf_counter() - start
        # 4 个 0.05s 并发应该 < 0.15s
        assert elapsed < 0.15


class TestRunSerial:
    def test_results_match(self) -> None:
        tasks = [(0.01, "a"), (0.01, "b")]
        assert sorted(run_serial(tasks)) == ["a", "b"]


class TestParallelSpeedup:
    def test_speedup(self) -> None:
        tasks = [(0.05, i) for i in range(4)]
        speedup = parallel_speedup(tasks, max_workers=4)
        assert speedup > 2.0           # 至少 2x


class TestCounter:
    def test_unsafe_loses_increments(self) -> None:
        n = 5
        incs = 1000
        result = counter_unsafe(n, incs)
        # 不一定每次都丢，但极大概率
        assert result < n * incs

    def test_with_lock_correct(self) -> None:
        n = 5
        incs = 1000
        assert counter_with_lock(n, incs) == n * incs


class TestThreadLocalStorage:
    def test_each_thread_sees_own_value(self) -> None:
        from concurrent.futures import ThreadPoolExecutor

        storage = ThreadLocalStorage()

        def worker(value: int) -> int:
            storage.set(value)
            return storage.get()

        with ThreadPoolExecutor(max_workers=4) as ex:
            futures = [ex.submit(worker, i) for i in range(4)]

        # 每个 worker 看到的都是自己设置的值
        assert sorted(f.result() for f in futures) == [0, 1, 2, 3]
