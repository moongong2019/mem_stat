#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：moon time:2019/3/19
# coding=utf-8
import os
import time
import csv
import matplotlib.pyplot as plt


# 追加写入CSV文件
def add_write_data_into_CSV(stat_list, file_name):
    # python3 need newline
    with open(file_name, "a+", newline='') as csvfile:
        csvWriter = csv.writer(csvfile)
        for data in stat_list:
            csvWriter.writerow(data)
        pass
    pass

array_total = []
array_java = []
array_native = []
array_code = []
array_graphic = []
array_private_other = []
array_system = []
array_stack = []


def analysis_lines(input_lines, csv_filename):
    total = 0
    java = 0
    native = 0
    code = 0
    graphic = 0
    private_other = 0
    system = 0
    stack = 0
    for line in input_lines:
        if isinstance(line, str):
            if 'TOTAL:' in line:
                total = int(line.split(':')[1].strip(' ').split(' ')[0])
            elif 'Java Heap:' in line:
                java = int(line.split(':')[1].split('\\n')[0])
                # print (java)
            elif 'Native Heap:' in line:
                native = int(line.split(':')[1].split('\\n')[0])
                # print (native)
            elif 'Code:' in line:
                code = int(line.split(':')[1].split('\\n')[0])
                # print (code)
            elif 'Graphics:' in line:
                graphic = int(line.split(':')[1].split('\\n')[0])
                # print (graphic)
            elif 'Private Other:' in line:
                private_other = int(line.split(':')[1].split('\\n')[0])
                # print (private_other)
            elif 'System:' in line:
                system = int(line.split(':')[1].split('\\n')[0])
                # print (system)
            elif 'Stack:' in line:
                stack = int(line.split(':')[1].split('\\n')[0])
                # print (stack)
            pass
        pass
    ans = [[total,java, native, code, stack, graphic, private_other, system]]
    add_write_data_into_CSV(ans, csv_filename)
    array_total.append(total)
    array_java.append(java)
    array_native.append(native)
    array_code.append(code)
    array_graphic.append(graphic)
    array_private_other.append(private_other)
    array_system.append(system)
    array_stack.append(stack)
    pass


def init_csv(csv_filename):
    # 如果文件存在则删除
    if os.path.exists(csv_filename):
        os.remove(csv_filename)
        print('remove file= {} '.format(csv_filename))
    str = [['TOTAL','Java Heap', 'Native Heap', 'Code', 'Stack', 'Graphics', 'Private Other', 'System']]
    add_write_data_into_CSV(str, csv_filename)
    pass


def draw_stackplot(times):
    x = range(1, times + 1)
    plt.title("mem stat")
    plt.plot(x,array_total,label ='total pss',color="red")
    plt.plot(x,array_java, label='java heap', color="yellow")
    plt.plot(x,array_native, label='native heap', color="green")
    plt.ylabel('memory usage (KB)')
    plt.xlabel('times')
    # 显示图例（即显示labels的效果）
    plt.legend(loc='upper left')
    # 显示图形
    plt.show()
    plt.savefig('mem.png')
    pass

def get_device_no():
    r = os.popen('adb devices')
    info = r.readlines()
    device_list = []
    for line in info:
        line = line.strip('\r\n')
        if len(line)>2 and '\tdevice' in line:
            device_list.append(line.split('\t')[0])
    print('Device list: %s'%str(device_list))
    return device_list


if __name__ == '__main__':
    pkg = 'com.tencent.mm:tools'  # 包名
    times = 60  # 运行次数
    sleep_time = 0.8  # 运行间隔
    csv_filename = 'mem_info.csv'
    # 指定设备
    device_list = get_device_no()
    device_name = device_list[0]
    exec_str = 'adb shell ' if device_name is None else 'adb -s '+device_name+' shell '
    init_csv(csv_filename)
    exec_str += 'dumpsys meminfo {} | grep -E "TOTAL:|Native Heap:|Graphics:|Java Heap:|Code:|Stack:|Private Other:|System:"'.format(
        pkg)
    #print(exec_str)
    for i in range(0, times):
        temp_string = os.popen(exec_str).readlines()
        print (temp_string)
        analysis_lines(temp_string, csv_filename)
        time.sleep(sleep_time)
    draw_stackplot(times)
    pass