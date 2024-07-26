function performLocalAction(action) {
    let data = {};
    if (action === 'create_file' || action === 'create_folder' || action === 'install_software') {
        let name = prompt(`Enter ${action.replace('_', ' ')} name:`);
        if (!name) {
            alert('Name cannot be empty.');
            return;
        }
        if (action === 'create_file') data['file_name'] = name;
        if (action === 'create_folder') data['folder_name'] = name;
        if (action === 'install_software') data['software_name'] = name;
    }
    $.post(`/local/${action}`, data, function(response) {
        $('#result').html(`<div class="alert alert-${response.status === 'success' ? 'success' : 'danger'}">${response.message}</div>`);
    });
}

function performRemoteAction(action) {  
    let data = {};
    let ip = $('#ip').val();
    if (!ip) {
        alert('Remote IP cannot be empty.');
        return;
    }
    data['ip'] = ip;
    if (action === 'create_file' || action === 'create_folder' || action === 'install_software') {
        let name = prompt(`Enter ${action.replace('_', ' ')} name:`);
        if (!name) {
            alert('Name cannot be empty.');
            return;
        }
        if (action === 'create_file') data['file_name'] = name;
        if (action === 'create_folder') data['folder_name'] = name;
        if (action === 'install_software') data['software_name'] = name;
    }
    $.post(`/remote/${action}`, data, function(response) {
        $('#result').html(`<div class="alert alert-${response.status === 'success' ? 'success' : 'danger'}">${response.message}</div>`);
    });
}
