
function mouseOver(id, value)
{
    full = document.getElementById('star-full').src;
    empty = document.getElementById('star-empty').src;
    extra = '-star-';
    var max = 4;

    for(var i=1;i<=value;++i)
    {
        document.getElementById(id + extra + i).src = full;
    }

    for(var i=value+1;i<=max;++i)
    {
        document.getElementById(id + extra + i).src = empty;
    }
}

function mouseOut(id)
{
    full = document.getElementById('star-full').src;
    empty = document.getElementById('star-empty').src;
    extra = '-star-';
    var value = parseInt(document.getElementById(id).value)
    var max = 4;

    for(var i=1;i<=value;++i)
    {
        document.getElementById(id + extra + i).src = full;
    }

    for(var i=value+1;i<=max;++i)
    {
        document.getElementById(id + extra + i).src = empty;
    }
}

function click(id, value)
{
    document.getElementById(id).value = value;
}

function addLoadEvent(func) {
    var oldonload = window.onload;
    if(typeof window.onload != 'function'){
        window.onload = func;
    }
    else{
        window.onload = function(){
            if(oldonload){
                oldonload();
            }
            func();
        }
    }
}
