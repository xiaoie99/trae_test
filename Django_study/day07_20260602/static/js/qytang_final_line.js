function formatNumber (n) {
            n = n.toString()
            return n[1] ? n : '0' + n;
        }
        function formatTime (number, format) {
            let time = new Date(number)
            let y = time.getFullYear()
            let M = formatNumber(time.getMonth() + 1)
            let D = formatNumber(time.getDate())
            let h = formatNumber(time.getHours())
            let m = formatNumber(time.getMinutes())
            let s = formatNumber(time.getSeconds())
            return format.replace('Y', y).replace('M', M).replace('D', D).replace('h', h).replace('m', m).replace('s', s)
        }
        function formatAxisTime(value) {
            let time = new Date(value);
            return formatNumber(time.getHours()) + ':' + formatNumber(time.getMinutes()) + ' ' + formatNumber(time.getMonth() + 1) + '-' + formatNumber(time.getDate());
        }
function echart_final_line_if_speed(chartid, labelname, lengends, datas, starttime) {
            let chart = echarts.init(document.getElementById(chartid));
            let option = {
                            title: {
                                text: labelname
                            },
                            tooltip: {
                                formatter: function (params) {
                                    let res='<div>时间：'+formatTime((params[0].data)[0], 'Y-M-D h:m:s')+'</div>'
                                    res+='<i class="fa fa-circle" style="color:'+params[0].color+'"></i> '+params[0].seriesName.replace(/Av.*/, '')+': '+(params[0].data)[1]+' kbps'+'<br/>'
                                    res+='<i class="fa fa-circle" style="color:'+params[1].color+'"></i> '+params[1].seriesName.replace(/Av.*/, '')+': '+(params[1].data)[1]+' kbps'+'<br/>'
                                    return res;},
                                trigger: 'axis',
                                axisPointer: {
                                    type: 'cross'
                                }
                            },
                            legend: {
                                left: '5%',
                                bottom: '7%',
                                data: lengends
                            },
                            grid: {
                                left: 'left',
                                y2: 100,
                                containLabel: true
                            },
                            toolbox: {
                                right: '10%',
                                feature: {
                                    saveAsImage: {}
                                }
                            },
                            xAxis: {
                                splitNumber: 10,
                                type: 'time',
                                boundaryGap: false,
                                axisLabel: {
                                    formatter: function (value) {
                                        return formatAxisTime(value);
                                    }
                                }
                            },
                            dataZoom: [{
                                type: 'slider',
                                start: 85,
                                end: 100,
                                bottom: 35,
                                height: 22
                            }, {
                                type: 'inside',
                                start: 85,
                                end: 100
                            }],
                            yAxis: {
                                type: 'value',
                                axisLabel: {
                                    formatter: '{value} kbps'
                                }
                            },
                            series: datas
            };
            chart.setOption(option);
        }
function echart_final_line_cpu_usage(chartid, labelname, lengends, datas, starttime) {
            let chart = echarts.init(document.getElementById(chartid));
            let option = {
                            title: {
                                text: labelname
                            },
                            tooltip: {
                                formatter: function (params) {
                                    console.log(params)
                                    let res='<div>时间：'+formatTime((params[0].data)[0], 'Y-M-D h:m:s')+'</div>'
                                    res+='<i class="fa fa-circle" style="color:'+params[0].color+'"></i> '+params[0].seriesName.replace(/Av.*/, '')+': '+(params[0].data)[1]+' %'+'<br/>'
                                    return res;},
                                trigger: 'axis',
                                axisPointer: {
                                    type: 'cross'
                                }
                            },
                            legend: {
                                left: '5%',
                                bottom: '7%',
                                data: lengends
                            },
                            grid: {
                                left: 'left',
                                y2: 100,
                                containLabel: true
                            },
                            toolbox: {
                                right: '10%',
                                feature: {
                                    saveAsImage: {}
                                }
                            },
                            xAxis: {
                                splitNumber: 16,
                                type: 'time',
                                boundaryGap: false,
                            },
                            dataZoom: [{
                                startValue: starttime
                            }, {
                                type: 'inside'
                            }],
                            yAxis: {
                                type: 'value',
                                axisLabel: {
                                    formatter: '{value} %'
                                }
                            },
                            series: datas
            };
            chart.setOption(option);
        }
function get_json_render_echart_line_if_speed(url, chartid) {
            $.getJSON(url,function(data) {
                                            echart_final_line_if_speed(chartid, data.labelname, data.legends, data.datas, data.starttime)
                                          });
            }
function get_json_render_echart_line_cpu_usage(url, chartid) {
            $.getJSON(url,function(data) {
                                            echart_final_line_cpu_usage(chartid, data.labelname, data.legends, data.datas, data.starttime)
                                          });
            }
