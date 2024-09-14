from qgis.core import *
from qgis.gui import *
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import QVariant
import requests
import json
from qgis.core import QgsCoordinateTransform, QgsProject, QgsCoordinateReferenceSystem
from qgis.gui import QgsMapCanvas

def get_wgs84_coordinates(event_pos, canvas: QgsMapCanvas):
    # 获取当前 CRS 和目标 CRS
    current_crs = canvas.mapSettings().destinationCrs()  # 当前画布的 CRS
    target_crs = QgsCoordinateReferenceSystem.fromEpsgId(4326)  # WGS 84
    
    # 获取画布上的坐标
    canvas_x = event_pos.x()
    canvas_y = event_pos.y()
    map_coords = canvas.getCoordinateTransform().toMapCoordinates(canvas_x, canvas_y)
    
    # 创建坐标转换工具
    transform = QgsCoordinateTransform(current_crs, target_crs, QgsProject.instance())
    
    # 转换坐标到目标 CRS
    wgs84_coords = transform.transform(map_coords)
    
    return wgs84_coords


class TileInfoPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.tool = MapClickTool(self.canvas)

    def initGui(self):
        self.action = QAction("Jilin1Info", self.iface.mainWindow())
        self.action.triggered.connect(self.activate)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Jilin1Info(2023)", self.action)

    def activate(self):
        self.canvas.setMapTool(self.tool)

    def unload(self):
        self.iface.removePluginMenu("&Jilin1Info(2023)", self.action)
        self.iface.removeToolBarIcon(self.action)

class MapClickTool(QgsMapTool):
    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapTool.__init__(self, self.canvas)

    def canvasReleaseEvent(self, event):
        # 获取点击的经纬度坐标
        point = get_wgs84_coordinates(event.pos(), self.canvas)
        lon = point.x()
        lat = point.y()
        
        # 固定zoom层级为18
        zoom = 18
        
        # 获取Tile信息
        tile_info = self.get_tile_info(zoom, lon, lat)
        
        # 如果Tile信息成功返回，创建点图层
        if tile_info:
            self.create_point_layer(zoom, lon, lat, tile_info)

    def get_tile_info(self, zoom, lon, lat):
        # 构建请求URL
        url = f"https://ovital.jl1mall.com/getTileInfo/{zoom}/{lon}/{lat}?mk=73ad26c4aa6957eef051ecc5a15308b4&tk=268f8056e6b07f974bb2dd2d229665bd"
        response = requests.get(url)
        
        # 检查响应是否成功
        if response.status_code == 200:
            json_response = response.json()
            # 如果返回的JSON中的'success'字段为True，返回数据
            if json_response.get('success'):
                return json_response  # 返回整个JSON对象
            else:
                return None
        else:
            return None

    def create_point_layer(self, zoom, lon, lat, response):
        # 提取返回的data字段
        data = response.get('data')
        
        if not data:
            return  # 如果data字段为空，则不进行任何操作

        # 创建一个内存点图层
        layer = QgsVectorLayer("Point?crs=EPSG:4326", f"Tile Info - {data}", "memory")
        provider = layer.dataProvider()

        # 添加字段
        provider.addAttributes([
            QgsField("zoom", QVariant.Int),        # 缩放层级
            QgsField("longitude", QVariant.Double),# 经度
            QgsField("latitude", QVariant.Double), # 纬度
            QgsField("date", QVariant.String)      # 日期信息
        ])
        layer.updateFields()

        # 创建一个点
        point = QgsPointXY(lon, lat)
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPointXY(point))
        
        # 设置属性，包含zoom、经度、纬度和从API返回的data
        attributes = [zoom, lon, lat, data]
        feature.setAttributes(attributes)
        
        # 将特征添加到图层中
        provider.addFeature(feature)
        layer.updateExtents()

        # 将图层添加到QGIS项目中
        QgsProject.instance().addMapLayer(layer)
