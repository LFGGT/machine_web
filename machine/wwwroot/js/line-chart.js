document.getElementById('lineChartButton').addEventListener('click', async () => {
    console.log('lineChart clicked');
    var excelData = document.getElementById("fileBox").dataset.excelData;
    lineChart(excelData);

});

async function lineChart(excelData) {
    
    var jsonData = JSON.parse(excelData);
    console.log(jsonData)
    var ctx = document.getElementById('lineChart').getContext('2d');
    var datasets = [
        {
            label: 'Vibration_X_RMS',
            borderColor: '#FFD306',
            data: jsonData.map(item => ({ x: item.timestamp, y: item.Vibration_X_RMS }))

        },
        {
            label: 'Vibration_Y_RMS',
            borderColor: '#2828FF',
            data: jsonData.map(item => ({ x: item.timestamp, y: item.Vibration_Y_RMS }))
        },
        {
            label: 'Vibration_Z_RMS',
            borderColor: '#00DB00',
            data: jsonData.map(item => ({ x: item.timestamp, y: item.Vibration_Z_RMS }))
        }

    ];

        
    
    var linechart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: datasets
        },
        options: {
        
        }
    });
}