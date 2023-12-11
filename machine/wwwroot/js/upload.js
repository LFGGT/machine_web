
document.getElementById('uploadButton').addEventListener('click', async () => {
     
    console.log('uploadFileToApi');
    var excelData = document.getElementById("fileBox").dataset.excelData;
    
    if (excelData && excelData.length > 0) {
        console.log(excelData);
        
        await uploadFileToApi(excelData).catch(error => {
            console.error(`Error in uploadFileToApi: ${error.message}`);

        });
    } else {
        console.log('no exceldata')
        await uploadFileToApi(excelData).catch(error => {
            console.error(`Error in uploadFileToApi: ${error.message}`);

        });
    }

});



async function uploadFileToApi(excelData) {
    try {
        const formData = new FormData();
        formData.append('excelData', excelData);
        formData.append('excel', 'database');

        for (const pair of formData.entries()) {
            console.log(pair[0], pair[1]);
        }
        const response = await fetch('http://localhost:5000/DAS_OCSVM', {
            method: 'POST',
            body: formData,
        });
        //創建formData放置資料並上傳後台
            if (response.ok) {
                const result = await response.json();
                console.log(result);
                //後端回傳資訊
                if (result.image) {
                    console.log('find')
                    var imageElement = new Image();
                    imageElement.src = 'data:image/png;base64,' + result.image;
                    document.getElementById('outputmachine').appendChild(imageElement);
                    console.log(imageElement.src)
                    alert('success');
                } else {
                    alert('Error: Image data not found in the response');
                }
            } else {
                alert('error');
        }
    } catch (error) {
        console.error(`Error uploading file: ${error.message}`);
    }
}

