import json
import re
from typing import Dict, List, Any

def fuzzy_match_form_data(form_fields: Dict[str, Dict[str, Any]], form_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    将form_data中的content与form_fields中的label进行模糊匹配，并添加匹配到的键名
    """
    # 创建标签到键的映射，用于快速查找
    label_to_key_map = {form_item: key for key, form_item in form_fields.items()}
    result = []

    for item in form_data:
        # 提取content中的主要文本（去除冒号等后缀）
        clean_content = re.sub(r'[:：\s]+$', '', item['content'])
        matched_key = None

        # 精确匹配优先
        if clean_content in label_to_key_map:
            matched_key = label_to_key_map[clean_content]
        else:
            # 模糊匹配
            for key, form_item in form_fields.items():
                if clean_content in form_item or form_item in clean_content:
                    matched_key = key
                    break

        result.append({
            **item,
            'datakey': matched_key or '未匹配到'
        })

    return result

def main():
    # 示例数据（请替换为实际数据）
    form_fields = {
    "customerName": "客户名称",
    "customerPhone": "客户电话",
    "installationAddress": "安装地址",
    "unitModel": "机组型号",
    "controlProgramVersion": "控制程序版本",
    "touchscreenProgramVersion": "触摸屏程序版本",
    "expansionValveControllerVersion": "膨胀阀控制器版本",
    "productSn": "产品序列号",
    "powerSupply": "电源",
    "factoryTime": "出厂时间",
    "debugTime": "调试时间",
    "projectCode": "项目编码",
    "projectName": "项目名称",
    "debugModel": "调试机型",
    "unitAppearanceDamage": "机组外观是否有损坏",
    "partsDamage": "是否有零部件损坏",
    "insulationDamage": "是否存在保温破损",
    "other": "其它",
    "isSeparateWiring": "“强弱电是否分开布线",
    "isCabinetCleanedMicro": "微机控制柜内部是否清扫",
    "isCabinetCleanedStart": "启动柜内部是否清扫",
    "isWiringCompliant": "控制接线是否符合接线图",
    "controlPowerConnectionStatus": "控制电源配线连接状态",
    "relayStatus": "继电器状态",
    "contactorStatus": "接触器状态",
    "powerWiringStatus": "电源接线合规且无松动",
    "startCabinetGroundingStatus": "启动柜接地状态是否正常",
    "lowVoltageInsulationResistance": "低压机组点击绝缘电阻",
    "guidePageSwitchStatus": "导页手动开关零位至满位",
    "factoryStatus": "出厂状态",
    "airTightnessTestStatus": "不带氟出厂机组，气密性试验",
    "prePressureHoldingAirTightness": "保压前（气密性试验）",
    "postPressureHoldingAirTightness": "保压后（气密性试验）",
    "vacuumTestStatus": "不带氟出厂机组，真空试验",
    "prePressureHoldingVacuum": "保压前（真空试验）",
    "postPressureHoldingVacuum": "保压后（真空试验）",
    "refrigerantChargeAmount": "冷媒充注量（R134a）",
    "singlePointLeakRate": "单点漏率",
    "isImpurityInContainer": "管路清洗是否有杂质进入容器",
    "flowProtectionType": "用户流量保护装置类别",
    "coolingSideStatus": "冷却侧动作是否正常",
    "freezingSideStatus": "冷冻侧动作是否正常",
    "chilledWaterPumpForm": "冷冻水泵形式",
    "chilledWaterPumpFlow": "冷冻水泵流量(m³/h)",
    "chilledWaterPumpHead": "冷冻水泵扬程(m)",
    "coolingWaterPumpForm": "冷却水泵形式",
    "coolingWaterPumpFlow": "冷却水泵流量(m³/h)",
    "coolingWaterPumpHead": "冷却水泵扬程(m)",
    "coolingTowerForm": "冷却塔形式",
    "coolingTowerFlow": "冷却塔流量(m³/h)",
    "coolingTowerHead": "冷却塔扬程(m)",
    "chilledWaterPH": "冷冻水PH值",
    "chilledWaterConductivity": "冷冻水电导率(μS/cm)",
    "isChilledWaterClear": "冷冻水是否清澈",
    "coolingWaterPH": "冷却水PH值",
    "coolingWaterConductivity": "冷却水电导率(μS/cm)",
    "isCoolingWaterClear": "冷却水是否清澈",
    "evaporationPressureLowAlarm": "蒸发压力过低报警",
    "condensationPressureHighAlarm": "冷凝压力过高报警",
    "windingTemperatureHighAlarm": "点击绕组温度过高报警",
    "startupTimeExceedAlarm": "启动时间过长报警",
    "gatewayType": "网关类型",
    "networkStatus": "网络状态",
    "gatewayFixedVersion": "网关固定版本",
    "isSetParamsSameAsFactory": "设定参数与出厂参数是否一致",
    "specificParams": "请输入具体参数",
    "waterControl": "进出水控制",
    "coolingHeatingTargetTemp": "制冷/制热目标温度",
    "evaporatorActualControlTemp": "蒸发器实际控制温度",
    "exitPauseTempDiff": "退出暂停温差",
    "enterPauseTempDiff": "进入暂停温差",
    "capacityAdjustmentKeepTempDiff": "容量调节保持温差",
    "coolingTowerFanAdjustTempDiff": "冷却塔风机调节温差",
    "coolingTowerFan1SwitchTemp": "冷却塔风机1关闭/开启温度",
    "coolingTowerFan2SwitchTemp": "冷却塔风机2关闭/开启温度",
    "baudRate": "波特率",
    "stationAddress": "站号地址",
    "parityBit": "校验位",
    "exitPauseTemperatureDifference": "退出暂停温差",
    "enterPauseTemperatureDifference": "进入暂停温差",
    "controlMode": "控制模式",
    "operationMode": "运行模式",
    "ratedCurrent": "主机额定电流",
    "ratedFrequency": "额定频率",
    "currentTransmitterRange": "电流变送器范围",
    "pressureSensorUpperLimit": "压力传感器上限设置",
    "evaporatorTargetLiquidLevel": "蒸发器目标液位",
    "coolingFullLoadPower": "制冷满载功率",
    "iceStorageFullLoadPower": "蓄冰满载功率",
    "compressorShutdownInterval": "压缩机停机间隔",
    "startupInterval": "启动间隔",
    "quickStartSignalDelay": "快速启动备妥信号判断延时",
    "inverter1SoftwareVersion": "1#主控软件版本",
    "inverter2SoftwareVersion": "2#主控软件版本",
    "inverter3SoftwareVersion": "3#主控软件版本",
    "compressor1Version": "1#压缩机版本",
    "maglev1Version": "1#磁悬浮版本",
    "compressor2Version": "2#压缩机版本",
    "maglev2Version": "2#磁悬浮版本",
    "compressor3Version": "3#压缩机版本",
    "maglev3Version": "3#磁悬浮版本",
    "compressor1AZ": "1#机头 AZ (μm)",
    "compressor1FX": "1#机头 FX (μm)",
    "compressor1FY": "1#机头 FY (μm)",
    "compressor1RX": "1#机头 RX (μm)",
    "compressor1RY": "1#机头 RY (μm)",
    "compressor2AZ": "2#机头 AZ (μm)",
    "compressor2FX": "2#机头 FX (μm)",
    "compressor2FY": "2#机头 FY (μm)",
    "compressor2RX": "2#机头 RX (μm)",
    "compressor2RY": "2#机头 RY (μm)",
    "compressor3AZ": "3#机头 AZ (μm)",
    "compressor3FX": "3#机头 FX (μm)",
    "compressor3FY": "3#机头 FY (μm)",
    "compressor3RX": "3#机头 RX (μm)",
    "compressor3RY": "3#机头 RY (μm)",
    "logTime1": "记录时间1",
    "chilledWaterInletTemp1": "冷冻水入口温度",
    "chilledWaterOutletTemp1": "冷冻水出口温度",
    "coolingWaterInletTemp1": "冷却水入口温度",
    "coolingWaterOutletTemp1": "冷却水出口温度",
    "evaporatorEvaporationPressure1": "蒸发器蒸发压力",
    "evaporatorSaturationTemp1": "蒸发器饱和温度",
    "evaporatorTerminalTempDiff1": "蒸发器端温差",
    "condenserCondensationPressure1": "冷凝器冷凝压力",
    "condenserSaturationTemp1": "冷凝器饱和温度",
    "condenserTerminalTempDiff1": "冷凝器端温差",
    "guideVane1Opening1": "1#导叶开度",
    "guideVane2Opening1": "2#导叶开度",
    "guideVane3Opening1": "3#导叶开度",
    "currentPercentage1": "电流百分比",
    "logTime2": "记录时间2",
    "chilledWaterInletTemp2": "冷冻水入口温度",
    "chilledWaterOutletTemp2": "冷冻水出口温度",
    "coolingWaterInletTemp2": "冷却水入口温度",
    "coolingWaterOutletTemp2": "冷却水出口温度",
    "evaporatorEvaporationPressure2": "蒸发器蒸发压力",
    "evaporatorSaturationTemp2": "蒸发器饱和温度",
    "evaporatorTerminalTempDiff2": "蒸发器端温差",
    "condenserCondensationPressure2": "冷凝器冷凝压力",
    "condenserSaturationTemp2": "冷凝器饱和温度",
    "condenserTerminalTempDiff2": "冷凝器端温差",
    "guideVane1Opening2": "1#导叶开度",
    "guideVane2Opening2": "2#导叶开度",
    "guideVane3Opening2": "3#导叶开度",
    "currentPercentage2": "电流百分比",
    "logTime3": "记录时间3",
    "chilledWaterInletTemp3": "冷冻水入口温度",
    "chilledWaterOutletTemp3": "冷冻水出口温度",
    "coolingWaterInletTemp3": "冷却水入口温度",
    "coolingWaterOutletTemp3": "冷却水出口温度",
    "evaporatorEvaporationPressure3": "蒸发器蒸发压力",
    "evaporatorSaturationTemp3": "蒸发器饱和温度",
    "evaporatorTerminalTempDiff3": "蒸发器端温差",
    "condenserCondensationPressure3": "冷凝器冷凝压力",
    "condenserSaturationTemp3": "冷凝器饱和温度",
    "condenserTerminalTempDiff3": "冷凝器端温差",
    "guideVane1Opening3": "1#导叶开度",
    "guideVane2Opening3": "2#导叶开度",
    "guideVane3Opening3": "3#导叶开度",
    "currentPercentage3": "电流百分比",
    "logTime4": "记录时间4",
    "chilledWaterInletTemp4": "冷冻水入口温度",
    "chilledWaterOutletTemp4": "冷冻水出口温度",
    "coolingWaterInletTemp4": "冷却水入口温度",
    "coolingWaterOutletTemp4": "冷却水出口温度",
    "evaporatorEvaporationPressure4": "蒸发器蒸发压力",
    "evaporatorSaturationTemp4": "蒸发器饱和温度",
    "evaporatorTerminalTempDiff4": "蒸发器端温差",
    "condenserCondensationPressure4": "冷凝器冷凝压力",
    "condenserSaturationTemp4": "冷凝器饱和温度",
    "condenserTerminalTempDiff4": "冷凝器端温差",
    "guideVane1Opening4": "1#导叶开度",
    "guideVane2Opening4": "2#导叶开度",
    "guideVane3Opening4": "3#导叶开度",
    "currentPercentage4": "电流百分比",
    "logTime5": "记录时间5",
    "chilledWaterInletTemp5": "冷冻水入口温度",
    "chilledWaterOutletTemp5": "冷冻水出口温度",
    "coolingWaterInletTemp5": "冷却水入口温度",
    "coolingWaterOutletTemp5": "冷却水出口温度",
    "evaporatorEvaporationPressure5": "蒸发器蒸发压力",
    "evaporatorSaturationTemp5": "蒸发器饱和温度",
    "evaporatorTerminalTempDiff5": "蒸发器端温差",
    "condenserCondensationPressure5": "冷凝器冷凝压力",
    "condenserSaturationTemp5": "冷凝器饱和温度",
    "condenserTerminalTempDiff5": "冷凝器端温差",
    "guideVane1Opening5": "1#导叶开度",
    "guideVane2Opening5": "2#导叶开度",
    "guideVane3Opening5": "3#导叶开度",
    "currentPercentage5": "电流百分比",
    "logTime6": "记录时间6",
    "chilledWaterInletTemp6": "冷冻水入口温度",
    "chilledWaterOutletTemp6": "冷冻水出口温度",
    "coolingWaterInletTemp6": "冷却水入口温度",
    "coolingWaterOutletTemp6": "冷却水出口温度",
    "evaporatorEvaporationPressure6": "蒸发器蒸发压力",
    "evaporatorSaturationTemp6": "蒸发器饱和温度",
    "evaporatorTerminalTempDiff6": "蒸发器端温差",
    "condenserCondensationPressure6": "冷凝器冷凝压力",
    "condenserSaturationTemp6": "冷凝器饱和温度",
    "condenserTerminalTempDiff6": "冷凝器端温差",
    "guideVane1Opening6": "1#导叶开度",
    "guideVane2Opening6": "2#导叶开度",
    "guideVane3Opening6": "3#导叶开度",
    "currentPercentage6": "电流百分比",
    "customerTargetTemperature": "客户设定的目标温度",
    "userSideSupplyVoltagePhase1": "用户侧供电电压相1",
    "userSideSupplyVoltagePhase2": "用户侧供电电压相2",
    "userSideSupplyVoltagePhase3": "用户侧供电电压相3",
    "chilledWaterInletOutletPressureDifference": "冷冻水进出口压差",
    "coolingWaterInletOutletPressureDifference": "冷冻水进出口压差",
    "unitVibrationNoiseCheck": "运行状态下机组振动、噪音检查",
    "fluorideSideFilterTemperatureDifference": "氟侧系统过滤器前后温差",
    "userFeedback": "用户意见收集",
    "onSiteTrainingEffect": "现场培训效果",
    "problemsAndSolutions": "问题及处理结果",
    "preStartupCheckStatus": "客户开机前检查情况",
    "preStartupCheckDetails": "具体问题描述",
    "operationStatus": "运行状态下机组表现",
    "operationDetails": "具体问题描述",
    "otherMatters": "其它事项",
    "mideaServicePersonName": "美的服务人员姓名",
    "mideaServicePersonPhone": "美的服务人员电话",
    "mideaServiceSignatureDate": "签名日期",
    "mideaServiceSignature": "美的服务人员签名",
    "customerRepresentativeName": "客户代表人员姓名",
    "customerRepresentativePhone": "客户代表人员电话",
    "customerSignatureDate": "签名日期",
    "customerSignature": "客户代表签名"
  }

    form_data = [
        {
            "id": "92f57952-b1d7-4048-b178-63d9b686dd33",
            "content": "机组外观是否有损坏：",
            "result": "有"
        },
        {
            "id": "6b88976b-f6ae-44fa-9144-cb9cc77f7156",
            "content": "是否有零部件损坏：",
            "result": "有"
        },
        {
            "id": "f660a864-d071-4690-bb2b-714b3ae6beb1",
            "content": "是否存在保温破损：",
            "result": "有"
        },
        {
            "id": "cd198eed-3f9d-4023-8a9f-9970e6b97403",
            "content": "其他：",
            "result": ""
        },
        {
            "id": "ae3da50a-dd18-4e32-a6f1-c8fe2a5d722e",
            "content": "弱弱电是否分开布线：",
            "result": "是"
        },
        {
            "id": "eabd0140-71e0-4f58-8346-0927a2c29c79",
            "content": "输机线相序是否清扫：",
            "result": "是"
        },
        {
            "id": "3e3bc46d-46aa-4a21-bbe5-dfd382ecaaa5",
            "content": "启动控制回路是否清扫：",
            "result": "是"
        },
        {
            "id": "ea0edb6c-c5ea-46c7-b5ff-1965d0a1264c",
            "content": "控制接点是否符合接线图：",
            "result": "是"
        },
        {
            "id": "1cac0e27-83e9-48ea-bcbb-182ab23a6bf0",
            "content": "控制回路是否连接状态：",
            "result": "正常"
        },
        {
            "id": "5b29fe5d-221d-4fa1-a823-b3845d070308",
            "content": "继电器状态：",
            "result": "正常"
        },
        {
            "id": "e061b2dd-2c5d-4a29-9da4-45c9eab74168",
            "content": "接触器状态：",
            "result": "正常"
        },
        {
            "id": "356888f2-a1bc-4d09-862a-e6470df3f8a8",
            "content": "端子螺钉是否松动：",
            "result": "正常"
        },
        {
            "id": "ce96685e-142c-41d3-8fd1-833973c6e3b7",
            "content": "启动接线状态是否正常：",
            "result": "正常"
        },
        {
            "id": "6265d9e1-8293-48f0-b932-11a854b11353",
            "content": "压低机组电机绝缘电阻：",
            "result": "正常"
        },
        {
            "id": "47775e2b-7f75-4417-bbd2-43f5661b4c2e",
            "content": "导杆与动杆安装位置正确：",
            "result": "正常"
        },
        {
            "id": "2cfc166a-fc23-4a39-9fce-ac629db8ebbb",
            "content": "不带电机厂机组，气密性试验：保压前=MPa 保压后=MPa\n（充注试验压力1.15±0.05Mpa，保压24h）",
            "result": "正常"
        },
        {
            "id": "3dd37848-2417-48e3-b70c-dddf7df8eb70",
            "content": "不带电机厂机组，真空试验：保压前=MPa 保压后=MPa\n（充注试验压力1.15±0.05Mpa，保压24h）",
            "result": "正常"
        },
        {
            "id": "698ca9df-1aee-4be6-9875-33a976999cdc",
            "content": "冷媒种类（R134a）：",
            "result": "X kg"
        },
        {
            "id": "e1b396a4-28e1-45c6-96ae-080ee3eb972e",
            "content": "单机泄漏量：",
            "result": "X g/年（手持点检仪，<5g/年）"
        },
        {
            "id": "9b5e2c0b-bc4a-47b7-b027-679668aad70d",
            "content": "管路流量是否有杂质进入容器：",
            "result": "是"
        },
        {
            "id": "3165daa0-03cd-4c41-bdba-3759e0a4a815",
            "content": "用户流量保护装置类别：",
            "result": "靶流"
        },
        {
            "id": "0007f9fe-2a7b-4374-b7d0-3c5e43abb684",
            "content": "冷却侧泵动作是否正常：",
            "result": "正常"
        },
        {
            "id": "9eaf64b0-e982-4202-bd57-df7a3c941451",
            "content": "冷冻侧泵动作是否正常：",
            "result": "正常"
        },
        {
            "id": "c632ce80-97dc-4f2c-abec-ec509566b47a",
            "content": "水泵、冷却塔检查（流量大于机组额定流量）",
            "result": ""
        },
        {
            "id": "a213bc8a-d4b8-4318-8b4f-5286dba9d938",
            "content": "水质检查",
            "result": ""
        },
        {
            "id": "6242cd07-991a-46e6-bbed-051bd4cdfc79",
            "content": "紧急压力过低报警：",
            "result": "正常"
        },
        {
            "id": "96228907-bef2-4126-8c0f-99395edc5fb2",
            "content": "高冷压压力过高报警：",
            "result": "正常"
        },
        {
            "id": "af9a958f-1963-461f-8e30-8d5ac375f157",
            "content": "电机线组温度过高报警：",
            "result": "正常"
        },
        {
            "id": "2e4919df-bc72-45fd-ac78-da288d8c298a",
            "content": "启动时间过长报警：",
            "result": "正常"
        },
        {
            "id": "14cf819b-fa90-46db-b297-1a4ac992f38f",
            "content": "网络类型：",
            "result": "4G网络"
        },
        {
            "id": "328a5d3c-d555-48f9-9d40-6d8362d992c0",
            "content": "网络强度：",
            "result": "4G信号强"
        },
        {
            "id": "0a4af32b-9e4c-499a-b8bd-69fc8a97ebfb",
            "content": "设定参数与出厂参数是否一致：",
            "result": "是"
        },
        {
            "id": "7fc679c2-3d0b-4b46-ab13-14d75b4b576b",
            "content": "具体差异：",
            "result": "有"
        },
        {
            "id": "0ce24d16-7856-4c87-8d30-0c2a05929612",
            "content": "用户设定参数：",
            "result": ""
        },
        {
            "id": "c515cfae-a31d-46de-affe-16bcd287efea",
            "content": "冷却塔风机调节温差：",
            "result": "-"
        },
        {
            "id": "755146b8-611f-430a-8a22-4a4173756e4a",
            "content": "冷却塔风机组1关闭/开启温度：",
            "result": "-"
        },
        {
            "id": "67883ecd-3d49-4465-bd3c-9a5dd2940b26",
            "content": "冷却塔风机组2关闭/开启温度：",
            "result": "-"
        },
        {
            "id": "2e31dc10-8b07-4c04-acf7-678b9da6d2f1",
            "content": "制冷目标出水温度：",
            "result": "-"
        },
        {
            "id": "d10468f8-12b5-4feb-b42a-f75353485e2d",
            "content": "进水温度：",
            "result": "-"
        },
        {
            "id": "914477cd-1b63-454a-94ec-6be9e0d1aa86",
            "content": "蒸发器壳程控制温度：",
            "result": "-"
        },
        {
            "id": "3008b8b6-43e0-46d2-9bbb-a87be2d71fe5",
            "content": "退出传感温差：",
            "result": "-"
        },
        {
            "id": "186f5695-a461-4029-a99d-40f6940fa40b",
            "content": "进入管传感温差：",
            "result": "-"
        },
        {
            "id": "a9a60720-1c8c-4520-9d22-b762cfeb54b5",
            "content": "串口设置：",
            "result": ""
        },
        {
            "id": "c450bcb4-d8f3-4a5b-8422-70222699afb8",
            "content": "波特率：",
            "result": "9600"
        },
        {
            "id": "7bdd34d4-2778-4839-b088-e781b1a2c9eb",
            "content": "站号（地址）：",
            "result": "-"
        },
        {
            "id": "7699ef21-4d48-4fcf-b21b-a30fca548e30",
            "content": "校验位：",
            "result": "正常"
        },
        {
            "id": "c2410b73-8788-4c9a-b9df-7ec267d445aa",
            "content": "模式设置：",
            "result": ""
        },
        {
            "id": "524a95a4-a2ef-4c3e-9417-da1b6604fc76",
            "content": "控制模式：",
            "result": "就地"
        },
        {
            "id": "2c8d25f3-635f-4314-85c2-a888cd0b714c",
            "content": "运行模式：",
            "result": "制冷"
        },
        {
            "id": "7e9daf62-f017-473c-9d84-e6c0feed04f7",
            "content": "进出水控制：",
            "result": "进水控制"
        },
        {
            "id": "325f9c2d-d814-4fdb-9994-b36f524b8ead",
            "content": "常规设置：",
            "result": ""
        },
        {
            "id": "c0e92136-48a3-4090-82de-3d4fa0391d0c",
            "content": "主机额定电流：",
            "result": "-A"
        },
        {
            "id": "537ae8c3-fca9-4ce5-9148-d39bd28c3650",
            "content": "额定频率：",
            "result": "-HZ"
        },
        {
            "id": "6a80c52a-47d1-4b60-8a65-2fe28cce0b2d",
            "content": "电流变送器范围：",
            "result": "-A"
        },
        {
            "id": "26868341-4d7a-421d-ad6b-1ed5f811bcc2",
            "content": "当地最低大气压力：",
            "result": "-kPa"
        },
        {
            "id": "75b36383-ab93-4a71-901b-ea418c26b7cf",
            "content": "压力传感器上限设定：",
            "result": "-kPa"
        },
        {
            "id": "e81821e4-700b-468b-a68d-72548f455cd6",
            "content": "蒸发器水箱标准位：",
            "result": "-mm"
        },
        {
            "id": "3e4a29b4-04c9-44fe-951c-e47c23bf4249",
            "content": "满载功率制冰：",
            "result": "-kW"
        },
        {
            "id": "304b1f69-9bfc-4d3b-8dfc-7bc08f11217e",
            "content": "满载功率制冰：",
            "result": "-kW"
        },
        {
            "id": "d263fd00-adf4-4b98-ad16-9e0f616762da",
            "content": "压缩机机组顺序：",
            "result": "-"
        },
        {
            "id": "23f66b13-e4ed-42b6-859d-fe378a78ce29",
            "content": "压缩机启动间隔：",
            "result": "-"
        },
        {
            "id": "a7028168-fd94-4116-a719-17e104feef11",
            "content": "快速启动高复信号判断延时：",
            "result": "-"
        },
        {
            "id": "df4fb6fe-6752-469c-8b72-960144b9a3a7",
            "content": "实现参数：",
            "result": ""
        },
        {
            "id": "094a9ff0-6324-4ae6-b975-bc8fa3b87740",
            "content": "变频器频率：",
            "result": "- 波特率："
        },
        {
            "id": "a9bcd495-b1a5-46ea-8d4e-1faba8d841b7",
            "content": "读取起始地址：",
            "result": "- 写起始地址："
        },
        {
            "id": "c9294e96-98f4-4dc6-bd77-f78252465290",
            "content": "压缩机参数：",
            "result": ""
        },
        {
            "id": "417968fb-8a8a-4274-9e90-71e7b0548002",
            "content": "读取起始地址：",
            "result": "- 写起始地址："
        },
        {
            "id": "afeaf442-bc3b-48fe-a456-3125381bf057",
            "content": "磁悬浮参数：",
            "result": ""
        },
        {
            "id": "cae18d1b-65d2-4d64-ac52-3b34e865a66a",
            "content": "手动悬浮，位移参数在±10范围内：Displace: AZ____FX ____FY____ RX____RY",
            "result": ""
        }
    ]
    

    # 执行匹配
    matched_result = fuzzy_match_form_data(form_fields, form_data)

    # 保存结果到JSON文件
    with open('matched_result.json', 'w', encoding='utf-8') as f:
        json.dump(matched_result, f, ensure_ascii=False, indent=2)

    print("匹配完成，结果已保存到 matched_result.json")

if __name__ == "__main__":
    main()  