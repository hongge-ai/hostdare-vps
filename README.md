# VPS Atlas

VPS Atlas 是面向中文用户的静态 VPS 套餐发现与比较站。首页支持跨商家筛选地区、商家、预算、标称线路和配置，并可并排比较三个套餐。商家目录与原有测评、教程和优惠文章保留在原有路径。

## 数据与价格口径

首页 `public/compare-assets/catalog.json` 是历史快照，不是实时报价或库存。目前收录 HostDare、RackNerd 和 BandwagonHost 的 2026-11-08 快照，以及 Raksmart 的 2026-11-11 活动默认配置快照（均为 UTC+8）。Raksmart 的裸机云及物理服务器不进入 VPS 比较。DMIT 历史文章中的套餐和系列对应关系尚待核验，因此暂未收录。

每条记录包括稳定的商家命名空间 ID、商家、套餐名、机房、结构化资源、存储、带宽、流量、商家标称线路、付款周期及标价、续费与活动资格、库存、购买链接、来源和核验日期。来源指向记录所依据的本站历史快照，快照内含商家来源。未知信息使用 `null` 或 `未知`；不可从地区、名称或其他套餐推测线路、库存、续费或实际应付金额。跨机房套餐的名称可能含线路，但不同机房实际线路可能不同。

价格为美元，显示对应周期的历史标价以及该周期标价除以月数的月均参考；默认使用月均最低的已记录周期，筛选周期时只使用该周期。预算筛选按同一月均参考计算，不能说明商家提供月付。税费、优惠资格、续费和实际应付金额以商家结账页为准。所有库存均为未知；本站部分购买链接含推广标识，可能带来收益。

Raksmart 仅记录快照中默认配置及对应周期的价格，不将可选付款周期推断为已知价格；活动资格、续费快照和附加条件会显示在卡片及对比中。具体促销可能已结束。原始记录位于 `public/raksmart-vps/plans.json`。

## 维护和新增商家

`python3 scripts/build-catalog.py` 从原 HostDare 快照、RackNerd / BandwagonHost 归档页面及 Raksmart 原始快照生成首页目录。该脚本不联网，不会更新核验日期，也不会验证当前价格或库存。更新源数据并逐项核验后，才能修改对应日期；添加商家时应记录官方或可靠的可追溯来源、时间、币种、真实付款周期与优惠条件，并使用不会跨商家重复的稳定 ID。不要将历史标价标作当前应付金额。

记录结构示例：

```json
{
  "id": "provider:stable-id", "provider": "服务商", "name": "套餐名称",
  "country": null, "city": null, "locations": null,
  "cpu_model": null, "cores": null, "memory_gb": null, "storage": null,
  "bandwidth": null, "traffic": null, "network": "未注明", "system": null,
  "currency": "USD", "prices": [{"period": "年付", "amount": 49.99}],
  "renewal": "未知", "eligibility": "未知", "stock": "未知", "terms": "未知",
  "verified_at": "2026-11-08", "source_url": "provider-snapshot/", "url": "https://example.com/"
}
```

## 运行与部署

站点无需构建步骤。生成目录后，在仓库根目录运行 `python3 -m http.server 8000 --directory public`，然后访问 `http://localhost:8000/`。GitHub Actions 使用 `public` 目录部署到 GitHub Pages。

各页面共用 `public/compare-assets/site.css` 和 `site.js`，统一导航与页脚；旧文章保留原有页面和样式。新增页面时请沿用共用导航，使用相对于页面的资源链接，并保留来源、核验时间及推广说明。
