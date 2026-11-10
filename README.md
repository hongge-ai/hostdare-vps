# VPS Atlas

VPS Atlas 是一个静态 VPS 套餐发现与比较站。首页支持按国家和城市、CPU 型号、核心数、内存、带宽、月流量和付款周期筛选，最多可并排比较三个套餐。原有测评、教程和优惠文章仍保留在原有路径。

## 数据与维护

目前套餐数据来自原站 [HostDare 套餐快照](public/hostdare-plans/index.html)，核对日期为 2026-11-08（UTC+8）；当前仅包含 HostDare，并非实时报价。价格、库存、线路及配置可能变化，购买时请以商家页面为准。购买链接包含推广标识。

套餐数据保存在 `public/compare-assets/plans.json`。添加或更新套餐时请保留来源和核对时间，使用国家及城市两个字段；未知参数应标为未注明，不要推测。价格按原付款周期记录，首页的月均价格为周期总价除以周期月数，并非商家提供的月付价格。筛选付款周期时，只展示支持该周期的套餐，并使用该周期的价格计算。未筛选周期时，展示可选周期中月均最低的价格。

## 运行与部署

站点无需构建步骤。在仓库根目录运行 `python3 -m http.server 8000 --directory public`，然后访问 `http://localhost:8000/`。GitHub Actions 使用 `public` 目录部署到 GitHub Pages。

原站内容和历史路径保留在 `public` 下。共享样式位于 `public/compare-assets/`；修改旧页面时应保留其引入的 `legacy.css`。
