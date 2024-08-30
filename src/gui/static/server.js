mostrarAlertaServer = () => {}
const fetchDefault = (endpoint, init, method, resolve = mostrarAlertaServer, reject = mostrarAlertaServer) => {
    fetch(`http://127.0.0.1:5000/${endpoint}`, {
        'method': method,
        'headers': {
            'Content-Type': 'application/json',
        },
        body: init,
    })
    .then(async (res) => {
        return res.json();
    })
    .then(data => {
        if (data.message != null) {
            reject(data)
        }
        else {
            resolve(data);
        }
    })
    .catch(err => { 
        reject(err);
    });
}

const fetchGet = (endpoint, resolve = mostrarAlertaServer, reject = mostrarAlertaServer) => {
    fetch(`http://127.0.0.1:5000/${endpoint}`, {
        'method': "GET",
        'headers': {
            'Content-Type': 'application/json',
        }
    })
    .then(async (res) => {
        return res.json();
    })
    .then(data => {
        if (data.message != null) {
            reject(data)
        }
        else {
            resolve(data);
        } 
    })
    .catch(err => { 
        reject(err);
    });
}

const fetchDelete = (endpoint, resolve = mostrarAlertaServer, reject = mostrarAlertaServer) => {
    fetch(`/api/v1${endpoint}`, {
        'method': "DELETE",
    })
    .then(async (res) => {
        return res.json();
    })
    .then(data => {
        resolve(data);
    })
    .catch(err => { 
        reject(err);
    });
}


const fetchForm = (endpoint, init, method, resolve  , reject)=>{
    fetch(`/api/v1${endpoint}`, {
        'method': method, 
        'headers': {
            // 'Content-Type': 'application/json',
        }, 
        body: init
    })
    .then(async (res) => {
        switch(res.status){
            case 200:
                return res.json()
            break ;
            default: 
                return {status: res.status, text: await res.text()}                
            break 
        }
    })
    .then(data=>{
        resolve(data)
    })
    .catch(err=>{
        err
        reject({msg: 'No disponible' , status: 500})
    })
}