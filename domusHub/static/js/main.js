
function start(){
    console.log('DomusHub Initialized')
}

function toggleDiv(){
    const div = document.getElementById('sideBar')
    if (div.style.display === 'none' || div.style.display === ''){
        div.style.display = 'flex';
    }else{
        div.style.display = 'none';
    }
}

