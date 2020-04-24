function del(){
    let str = "Are you sure you want to delete your page? You will not be able to restore it. All your entries will be deleted.";
    let b = confirm(str)
    if (b===true){
        location.href = 'delself'
    }
}