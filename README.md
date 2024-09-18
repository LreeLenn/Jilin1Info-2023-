# Jilin1Info 插件简介

**Jilin1Info** 是一个 QGIS Desktop 插件，由 [@lreept](undefined/lreept) 开发，现已通过 QGIS Plugin 发布。该插件可以实现 **2023 年全国 50cm 吉林一号影像** 的拍摄日期查询，用户可通过鼠标点击生成带有拍摄日期标注的临时图层（Point）。

<div align="center">
  <img src="https://cdn.nlark.com/yuque/0/2024/png/21957921/1726629143267-15e9f770-e1f5-421a-84cd-c05d0ca24105.png" alt="白云机场 吉林一号拍摄于 2023/01/29" width="600"/>
  <p><i>白云机场 吉林一号拍摄于 2023/01/29</i></p>
</div>

---

## 1. Jilin1Info 下载安装

你可以通过 QGIS 的插件管理器在线搜索并安装 **Jilin1Info** 插件。请注意，需要先 **开启实验性插件** 检索功能，才能找到此插件。

<div align="center">
  <img src="https://cdn.nlark.com/yuque/0/2024/png/21957921/1726629464635-81f8504a-f4b2-43d2-8c68-8042c5e131d1.png" alt="Jilin1Info(2023) 实验性插件" width="600"/>
  <p><i>Jilin1Info(2023) 实验性插件</i></p>
</div>

---

## 2. 插件功能说明

**Jilin1Info** 插件的核心功能是允许用户点击地图，生成拍摄日期标注的临时点图层，并且可以根据用户需求更改图层数据。

用户可以通过修改位于：

`%AppData%\QGIS\QGIS3\profiles\default\python\plugins\Jilin1Info-2023-\main.py`

的 `main.py` 文件，来更换影像图层和个人申请的图源 API KEY。例如：

- 如果你需要检索 **2022 年吉林一号影像** 拍摄日期，可以找到 `main.py` 中的 `mk=` 代码部分，将图层 ID 进行替换。

修改示例：
- **2023 年图层 ID**：`73ad26c4aa6957eef051ecc5a15308b4`
- **2022 年图层 ID**：`841e61e1f539abcc328bca96294e8e50`

修改完成后，重启 QGIS 即可生效。

---

## 3. 图层 ID 讨论

如果你有其他年份的图层 ID，欢迎在评论区讨论分享。

<div align="center">
  <img src="https://cdn.nlark.com/yuque/0/2024/png/21957921/1726630398816-9c07b559-3bf9-41bc-a993-1b7d8f43da13.png" alt="插件效果示例" width="600"/>
  <p><i>插件效果示例</i></p>
</div>

---

通过这个插件，用户可以快速查询吉林一号影像的拍摄日期，方便进行遥感数据分析。欢迎大家一起探讨不同年份的图层 ID。
