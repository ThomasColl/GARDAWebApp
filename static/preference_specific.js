function adjust_action_box() {
    var mylist = document.getElementById("resource");

    if(mylist.options[mylist.selectedIndex].value == "items") {
        var sel = document.getElementById('action');
        var opt = document.createElement('option');

    	opt.appendChild( document.createTextNode("adjust") );
    	opt.value = "adjust";
        sel.appendChild(opt);
    }
    else if(mylist.options[mylist.selectedIndex].value == "policies") {
        var sel = document.getElementById('action');
        var opt = document.createElement('option');

    	opt.appendChild( document.createTextNode("add") );
    	opt.value = "add";
        sel.appendChild(opt);
        var sel = document.getElementById('action');
        var opt = document.createElement('option');
        opt.appendChild( document.createTextNode("edit") );
    	opt.value = "edit";
        sel.appendChild(opt);
        var sel = document.getElementById('action');
        var opt = document.createElement('option');
        opt.appendChild( document.createTextNode("delete") );
    	opt.value = "delete";
        sel.appendChild(opt);

    }
    else if(mylist.options[mylist.selectedIndex].value == "analytics") {
        var sel = document.getElementById('action');
        var opt = document.createElement('option');

    	opt.appendChild( document.createTextNode("request") );
    	opt.value = "request";
        sel.appendChild(opt);
    }
}