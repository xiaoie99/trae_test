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
