import re
import time
from pathlib import Path

from py_dct_txt import DctTxtStore
from py_dct_txt.utils import normalize_to_ascii


def split_pos(s: str):
    match = re.match(r"^([a-zA-Z0-9 ]+\.)?(.+)$", s)
    if match:
        pos = match.group(1)
        pos = pos.strip() if pos else ""
        return (pos, match.group(2).strip())
    print(f"dismatch : {s}")


def get_value(s: str):
    if s and s[0] == "[" and "]" in s:
        ss = s[1:].split("]", 1)
        if len(ss) == 2:
            return ss[1]
    return s


def is_special(pos: str, s: str):
    if pos.strip():
        return False
    s = s.strip()
    if s.startswith("[网络]"):
        return False
    if s and s[0] == "[" and "]" in s:
        return True
    return False
    # if vv[0] == "[" and "]" in vv:
    #     vvv = vv[1:].split("]", 1)
    #     if len(vvv) == 2:
    #         v_set = set(vvv[1])
    #         if (
    #             len(v_set)
    #             and len(v_set & pos_exp_items_set) / len(v_set) > 0.65
    #         ):
    #             print(f'ignore {vv}')
    #             continue
    #     explain_items2.append(v)


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

    print(f"removing {path} ...")
    removed = 0
    remained = 0
    for key, word in keyd.items():
        explain = word.get("explain")
        if explain and explain.l:
            # if len(explain.l) < 2:
            #     continue
            res = []
            normal = set()
            # if key == "affective":
            #     __import__("pdb").set_trace()
            nl = []
            for s in explain.l:
                match = re.match(
                    r"(\(.*的.*(?:复数|过去|现在|形容|比较|最高|被动|缩写|形式).*\))\s*(.*(?:vi?t?|u?na?|a|adj|adv?|pl|mux|prep|pron|int|abbr|suff?|pref|det|art)\s?\..*)",
                    s,
                )
                if match:
                    nl.append((match.group(2) + " " + match.group(1)).strip())
                else:
                    nl.append(s)
            explain.l = nl
            # nl = []
            for s in explain.l:
                match = re.match(r"\s*(.*?)\s*((?:vi?t?|u?na?|a|adj|adv?|pl|mux|prep|pron|int|abbr|suff?|pref|det|art)\s?\.)(.*)", s)
                if match:
                    if len(match.group(1).strip())>0:
                    # nl.append(match.group(2).strip() + " " + match.group(1).strip() + " " + match.group(3).strip())
                        print(match.group(0))
                # else:
                    # nl.append(s)
            # explain.l = nl
            for s in explain.l:
                split_s = split_pos(s)
                assert split_s
                if not is_special(split_s[0], split_s[1]):
                    normal.update(
                        c for c in split_s[1] if c.isalpha() and not c.isascii()
                    )
            for s in explain.l:
                split_s = split_pos(s)
                assert split_s
                if not is_special(split_s[0], split_s[1]):
                    res.append(s)
                    continue

                v = split_s[1].strip()
                while v and v[0] == "[" and "]" in v:
                    v = v[1:].split("]", 1)[1].strip()
                special = set(c for c in v if c.isalpha() and not c.isascii())
                k = 0.6 - min(0.2, len(special) * 0.02)
                if len(special) and len(special & normal) / len(special) >= k:
                    removed += 1
                else:
                    remained += 1
                    res.append(s)
            word["explain"].l = res

    print(f"{removed=} , {remained=}")
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
