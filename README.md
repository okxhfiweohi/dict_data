# dict_data

数据仓库

欢迎任何数据修正/修订的 pr !

## 数据格式

```plain
/* 可以有注释 */
/* := => >> <> 标记不同数据类型 */

/* explain 含义 */
/* || 分隔, string[] */
word := 解释1 || 解释2 || ...

/* 音标、重定向 */
word2 => str /* string */

/* collins 星级、词频 */
word3 >> 3 /* integer or any value type */

/* 其他复杂数据： 词性比例 */
/* yaml-like (flow style) */
like <> V: {rk: 208, frq: 198134}, N: {rk: 5907, frq: 4143}
```

更多信息参考: [py_dct_txt](https://github.com/okxhfiweohi/py_dct_txt.git)

## 数据分组

- `phonetic` : 音标
- `collins` : 柯林斯星级 (0 - 5)
- `explain` : 简明释义( [词性](./misc/pos.md#pos-normal-abbr) )
- `pos` : 词性占比 （参考 [claws7](./misc/pos.md#claws7-abbr) ,rk=rank, frq=frequency）
- `exchange` : 词形变换 ([类型](./misc/other.md#exchange-forms))
- `bnc` : bnc 词频排名
- `freq` : 当代语料库排名
- `lgk_id` : 兰极客 id 记录（不包含数据） (w=word, p=photos)
- `redirect` : 其他词条重定向

## 标签

- cet4
- cet6
- gre
- high_school : 高中
- middle_school : 初中
- npee
- oxford_3000 : 牛津核心三千词
- postgraduated_exam : 考研
- primary_school : 小学
- tem8
- toefl

## 致谢

诚挚感谢以下开源项目, 站在前人的肩膀上，整理出了本仓库的数据:

- [skywind3000/ECDICT](https://github.com/skywind3000/ECDICT) :
  音标、简明释义及占比 [等](#数据分组) 内容的数据来源
- [mahavivo/english-wordlists](https://github.com/mahavivo/english-wordlists.git) : 几乎所有 [标签](#标签) 的数据来源
