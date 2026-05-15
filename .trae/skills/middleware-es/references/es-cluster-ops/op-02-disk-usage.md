# 操作 2：查看节点磁盘使用率

| 属性 | 说明 |
|------|------|
| 操作类型 | 查看节点磁盘使用率 |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令模板 | `paas-cli es disk-usage --project {project_id} --env {env}` |

## 额外参数

无需额外参数。

## 命令示例

```bash
paas-cli es disk-usage --project j036x0 --env DEV
```

## 返回信息

- 各节点磁盘使用率
- 磁盘水位线状态（正常 / 接近水位线 / 超过水位线）
- 磁盘总量和可用空间

## 注意事项

- 这是只读操作，可直接执行
- 当节点磁盘使用率超过 85% 时需要注意，超过 90% 可能触发只读模式
- 磁盘水位线阈值：
  - `cluster.routing.allocation.disk.watermark.low`：默认 85%，不分配新分片
  - `cluster.routing.allocation.disk.watermark.high`：默认 90%，开始迁移分片
  - `cluster.routing.allocation.disk.watermark.flood_stage`：默认 95%，索引设为只读
