import time
from pathlib import Path

from py_dct_txt import DctTxtStore
from py_dct_txt.utils import normalize_to_ascii


class Timer:
    def __init__(self) -> None:
        self.time_start = None
        pass

    def start(self):
        self.time_start = time.time()

    def print(self, s="used {:.3f}s"):
        t = 0 if self.time_start is None else time.time() - self.time_start
        print(s.format(t))


def format(path: Path):
    tmr = Timer()
    print(f"looading {path} ...")
    tmr.start()
    store = DctTxtStore()
    keyd = store.load(path)
    tmr.print()

    print(f"formatting {path} ...")
    tmr.start()
    keyd = {
        k: v
        for k, v in sorted(
            keyd.items(),
            key=lambda v: (normalize_to_ascii(v[0]).lower(), v[0].lower(), v[0]),
        )
    }
    tmr.print()

    print("saving ...")
    tmr.start()
    store.save(keyd, path)
    tmr.print()

    print("cleaning ...")
    tmr.start()
    store.clean()
    store.clean_empty_folder(path)
    tmr.print()


tmr = Timer()
tmr.start()
format(Path("./data"))
tmr.print("all used {:.3f}s")


print("done!")
