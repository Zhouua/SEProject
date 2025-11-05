# 区块链非原子套利交易识别
## 项目背景
本项目以 Uniswap V3 和 Binance 之间的 USDT/ETH 交易对为研究对象，通过对两边的价格数据进行分析，尝试识别其中可能存在的非原子套利行为
## Quick Start
本项目前端使用vue3，后端使用python fastapi，数据库使用PostgreSQL

### 获取代码

```bash
git clone https://github.com/Zhouua/SEProject.git
```

### 前端

```python
cd frontend
npm install
npm start dev
```



### 后端

```python
pip install ...
```



## 项目需求
实现一个Web应用，完成如下两个核心功能:
1. 展示 2025 年 9 月 1 日至 9 月 30 日期间，Ethereum上Uniswap V3（USDT/ETH池）与
Binance（USDT/ETH 交易对）的历史成交数据，并对两者价格变化进行可视化对比。
2. 对 Uniswap V3与Binance之间的USDT/ETH交易数据进行分析，探索并实现识别非原子套
利行为的方法，可结合启发式规则、统计分析或其他可行手段，计算潜在获利金额（以
USDT 为单位）。
## 数据来源
1. 对Uniswap V3上其中一个USDT/ETH池进行分析
- 以太坊合约地址： 0x11b815efB8f581194ae79006d24E0d814B7697F6
- 可通过如下链接查看：
https://goto.etherscan.com/address/0x11b815efb8f581194ae79006d24e0d814b7697f6
2. 获取交易数据的API参考文档
  https://dune.com/home
  https://thegraph.com/docs/zh/
  https://github.com/binance/binance-spot-api-docs
  https://docs.etherscan.io/

3. 相关文献：

  Heimbach L, Pahari V, Schertenleib E. Non-atomic arbitrage in decentralized
  finance[C]//2024 IEEE Symposium on Security and Privacy (SP). IEEE, 2024: 3866-3884.

  Wu F, Sui D, Thiery T, et al. Measuring CEX-DEX Extracted Value and Searcher Profitability:
  The Darkest of the MEV Dark Forest[J]. arXiv preprint arXiv:2507.13023, 2025.
## 相关算法
1. 启发式规则
2. 统计分析
3. xxx
### 参考文献
https://ieeexplore.ieee.org/abstract/document/10646836

https://arxiv.org/abs/2406.02172

https://arxiv.org/abs/2410.10797

https://www.researchgate.net/publication/388494799_Cross-Chain_Arbitrage_The_Next_Frontier_of_MEV_in_Decentralized_Finance

https://link.springer.com/article/10.1007/s11117-021-00848-z

xxx

## 代码提交规范

### 分支管理

1. **主分支保护**
   - `main` 分支为受保护分支，不允许直接提交
   - `develop` 分支为开发分支，用于集成各个功能分支

2. **分支命名规范**
   - 功能分支：`feature/<功能名称>`，例如 `feature/user-login`
   - 修复分支：`fix/<问题描述>`，例如 `fix/login-bug`
   - 优化分支：`optimize/<优化内容>`，例如 `optimize/query-performance`
   - 热修复分支：`hotfix/<紧急问题>`，例如 `hotfix/critical-security`

### 提交流程

1. **拉取最新代码**
   ```bash
   git checkout main
   git pull origin main
   ```

2. **创建并切换到新分支**
   ```bash
   git checkout -b feature/<功能名称>
   ```

3. **开发并提交代码**
   ```bash
   git add .
   git commit -m "<提交信息>"
   ```

4. **推送到远程仓库**
   ```bash
   git push origin feature/<功能名称>
   ```

5. **创建 Pull Request**
   - 在 GitHub 上创建 PR，指定审核人员
   - 填写 PR 描述，说明改动内容和目的
   - 等待代码审核通过后合并

6. **合并前的准备**
   ```bash
   # 切换到主分支并拉取最新代码
   git checkout main
   git pull origin main
   
   # 切换回功能分支并合并主分支
   git checkout feature/<功能名称>
   git merge main
   
   # 解决冲突（如果有）
   # 测试确保功能正常
   git push origin feature/<功能名称>
   ```

### Commit Message 规范

采用约定式提交（Conventional Commits）格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type 类型：**
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档修改
- `style`: 代码格式调整（不影响代码逻辑）
- `refactor`: 代码重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动
- `build`: 构建系统或外部依赖的变动
- `ci`: CI 配置文件和脚本的变动

**示例：**
```bash
git commit -m "feat(frontend): 添加用户登录界面"
git commit -m "fix(backend): 修复套利计算逻辑错误"
git commit -m "docs(readme): 更新项目文档"
git commit -m "refactor(api): 重构数据获取接口"
```

### 版本标签

在达到重要里程碑时，使用 Git Tag 进行标记：

```bash
# 创建标签
git tag -a v1.0.0 -m "发布版本 1.0.0"

# 推送标签到远程
git push origin v1.0.0

# 推送所有标签
git push origin --tags
```

**版本号规范（语义化版本）：**
- `v0.1.0`: MVP 版本
- `v1.0.0`: 第一个正式版本
- `v1.1.0`: 新增功能（次版本号）
- `v1.1.1`: Bug 修复（修订号）
- `v2.0.0`: 重大更新（主版本号）

### 注意事项

- ⚠️ 提交前务必在本地测试，确保代码可运行
- ⚠️ 不要提交敏感信息（API密钥、密码等）
- ⚠️ 大文件和编译产物不要提交到仓库（配置好 `.gitignore`）
- ⚠️ 及时同步主分支代码，避免产生大量冲突

## 人员分工
- 前端：[@Zhouua](https://github.com/Zhouua), [@WBLBDB-DB](https://github.com/WBLBDB-DB)
- 后端：[@f0reverFr33](https://github.com/f0reverFr33)
- 算法：[@oi35](https://github.com/oi35)
- 测试：[@MKL537999](https://github.com/MKL537999)
