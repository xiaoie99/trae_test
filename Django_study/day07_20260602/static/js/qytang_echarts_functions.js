function echarts_compound(chartid, labelname, legends, labels, datas){
    let myChart = echarts.init(document.getElementById(chartid));
    myChart.setOption({
        title : {
            text:labelname,
            x:'center',
            textStyle:{
                color: 'red',
                fontSize: 20
            }
        },
        legend: {
            bottom: 0,
            data:legends
        },
        tooltip: {
            trigger: 'axis'
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            name: '时间',
            data: labels,
        },
        yAxis: {
            type: 'value',
            name: '利用率(单位%)',
            axisLabel: {
                formatter: '{value} %'
            },
            min: 0,
            max: 100
        },
        series: datas
    })
}
function echarts_bar(chartid, labelname, labels, datas, color){
    let myChart = echarts.init(document.getElementById(chartid));
    myChart.setOption({
        title : {
            text:labelname,
            x:'center',
            textStyle:{
                color: 'red',
                fontSize: 20
            }
        },
        tooltip: {
            trigger: 'axis'
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            name: '时间',
            data: labels
        },
        yAxis: {
            type: 'value',
            name: '利用率'
        },
        series: [{
            name: 'Line 1',
            data: datas,
            smooth:true,
            type: 'bar',
            color: color
        }]
    })
}
function ajax_render_echart(url, chartid) {
    $.getJSON(url,function(data) {
        echarts_compound(chartid, data.labelname, data.legends, data.labels, data.datas)
    });
}
function echarts_pie(chartid, labelname, labels, datas){
    let myChart = echarts.init(document.getElementById(chartid));
    myChart.setOption({
        title: {
            text: labelname,
            left: 'center',
            top: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: labels
        },
        series: [{
            name: labelname,
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '30',
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: datas
        }]
    })
}
function ajax_render_pie(url, chartid) {
    $.getJSON(url, function(data) {
        echarts_pie(chartid, data.labelname, data.labels, data.datas);
    });
}
