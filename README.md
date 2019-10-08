![示例](example.png)

## 安装

请自行安装 `python3-pip` 。

### 直接安装

方便，但是不会经常维护，如果碰到问题请使用源码安装获得最新版本。

```
pip3 install ioretest --user
```

### 从源码安装

直接安装最新的稳定版本。

```bash
git clone https://github.com/kewth/retest
cd retest
pip3 install .
```

## 使用

请自行查看帮助：

```bash
retest -h
```

或者

```bash
retest -l
```

## 说明

- 单人评测脚本。
- 专为偏爱终端的 OIer 设计，方便在改题的时候随时重测自己的程序。
- 同样适用于出题时，用自己造的数据测试标程或部分分程序的正确性。

## 功能

- 支持 AC, WA, RE, TLE, MLE, CE 评测状态。
- 支持 spj 比较
- 支持对拍
- 支持插件扩展
- 每个点 AC 后会给出用时。
- 评测后会生成目录 retest_dir ，内有评测详细信息。

## 本地化

由于每个人使用习惯不相同， retest 不会去刻意迎合某个习惯。  
但是想让 retest 在自己的习惯下更好用，也是很容易做到的。  
比如写个 retest.yaml 生成器之类的小工具，或者使用 python 编写扩展插件得到更好的效果，甚至可以用 retest 做后端自己写接口。

如果你有自己的小工具或者插件，不妨写在 extra 目录下或者 plugin 目录下，提交 pull request 。

## 常见问题

Q: 为什么 retest 测第 3 个点 WA 但是自己测的时候 AC ？  
A1: 第三个点 3.in 在实际数据文件夹中可能并不是 3.in ，事实上 3.in 指的是 retest_dir/3.in 。  
A2: 程序里有 freopen 但未指定 input/output

Q: 为什么改 retest_dir 里面的数据的时候原数据也出了问题。  
A: retest_dir 内的数据实际上都是符号链接。

Q: 为什么 retest 报错并崩溃？  
A: 写了 input/output 但没打 freopen 。

