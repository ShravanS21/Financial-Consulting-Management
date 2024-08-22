function adminvalidation()
{
    var admin_name=document.getElementById("admin_name").value;
    var password=document.getElementById("password").value;

    if(admin_name=="")
    {
        alert("Please enter Admin name");
        return false;
    }    
    
    if(password=="")
    {
        alert("Please enter Password");
        return false;
    }  
    return true;
}