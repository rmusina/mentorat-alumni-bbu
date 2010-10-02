next_id = 1

function remove_field(id, pid)
{
    document.getElementById(pid).removeChild(document.getElementById(id));
}

function addRemoveButton(div, text, parent_id)
{
    button = document.createElement("button");
    button.setAttribute("type", "button");
    button.appendChild(document.createTextNode(text));
    button.setAttribute("onclick", "remove_field('" + div.getAttribute("id") + "', '" + parent_id + "')");
    div.appendChild(button);
}

/*
 * <div>
 * <h3>Text field</h3>
 * <input type="hidden" name="field<id>-type" value="text"/>
 * <label for="field<id>-name">Field name:</label> <input type="text" name="field<id>-name"/>
 * <input type="checkbox" name="field<id>-required" value="Yes" checked /><label for="field<id>-required">Required</label>
 * </div>
 */
function add_textfield(holder_name, head_text, fname, req, rm_text)
{
    names = "field-" + next_id + "-";

    div = document.createElement("div");
    div.setAttribute("class", "ctrlHolder");
    div.setAttribute("id", names + "holder");
    head = document.createElement("h3");
    head.appendChild(document.createTextNode(head_text));
    div.appendChild(head);

    field_type = document.createElement("input");
    field_type.setAttribute("type", "hidden");
    field_type.setAttribute("name", names + "type");
    field_type.setAttribute("value", "text");
    div.appendChild(field_type);

    label_name = document.createElement("label");
    label_name.setAttribute("for", names + "name");
    label_name.appendChild(document.createTextNode(fname + "*\n"));
    field_name = document.createElement("input");
    field_name.setAttribute("type", "text");
    field_name.setAttribute("name", names +  "name");
    field_name.setAttribute("class", "textinput");
    div.appendChild(label_name);
    div.appendChild(field_name);

    div.appendChild(document.createElement("br"));

    label_req = document.createElement("label");
    label_req.setAttribute("for", names + "required");
    label_req.appendChild(document.createTextNode(req));
    field_req = document.createElement("input");
    field_req.setAttribute("type", "checkbox");
    field_req.setAttribute("name", names + "required");
    field_req.setAttribute("value", "yes");
    field_req.setAttribute("checked", "");
    field_req.setAttribute("class", "checkboxinput");
    div.appendChild(field_req);   
    div.appendChild(label_req);

    addRemoveButton(div, rm_text, holder_name);

    document.getElementById(holder_name).appendChild(div);    
    ++ next_id;
}

/*
 * <div>
 * <h3>Boolean field</h3>
 * <input type="hidden" name="field<id>-type" value="bool"/>
 * <label for="field<id>-name">Field name:</label> <input type="text" name="field<id>-name"/>
 * </div>
 */
function add_booleanfield(holder_name, head_text, fname, rm_text)
{
    names = "field-" + next_id + "-";

    div = document.createElement("div");
    div.setAttribute("class", "ctrlHolder");
    div.setAttribute("id", names + "holder");
    head = document.createElement("h3");
    head.appendChild(document.createTextNode(head_text));
    div.appendChild(head);

    field_type = document.createElement("input");
    field_type.setAttribute("type", "hidden");
    field_type.setAttribute("name", names + "type");
    field_type.setAttribute("value", "bool");
    div.appendChild(field_type);

    label_name = document.createElement("label");
    label_name.setAttribute("for", names + "name");
    label_name.appendChild(document.createTextNode(fname + "*\n"));
    field_name = document.createElement("input");
    field_name.setAttribute("type", "text");
    field_name.setAttribute("name", names +  "name");
    field_name.setAttribute("class", "textinput");
    div.appendChild(label_name);
    div.appendChild(field_name);

    div.appendChild(document.createElement("br"));

    addRemoveButton(div, rm_text, holder_name);

    document.getElementById(holder_name).appendChild(div);
    ++ next_id;
}

function add_choice(pid, name, choice_name, rm_choice)
{
    var div = document.createElement("div");
    div.setAttribute("class", "ctrlHolder");
    var val = parseInt(document.getElementById(name + "counter").getAttribute("value"));
    document.getElementById(name + "counter").setAttribute("value", val + 1);
    var id = name + val;
    div.setAttribute("id", id + "-holder");
    
    var label = document.createElement("label");
    label.setAttribute("for", id);
    label.appendChild(document.createTextNode(choice_name + '*'));
    var input = document.createElement("input");
    input.setAttribute("type", "text");
    input.setAttribute("name", id);
    input.setAttribute("class", "textinput");

    div.appendChild(label);
    div.appendChild(input);

    addRemoveButton(div, rm_choice, pid);

    document.getElementById(pid).appendChild(div);
}

function add_choicediv(to, name, choice_text, add_text, choice_name, rm_choice)
{
    var div = document.createElement("div");
    div.setAttribute("id", name+"holder");
    div.setAttribute("style", "position: relative; left:30px");
    div.setAttribute("class", "ctrlHolder");

    head = document.createElement("h4");
    head.appendChild(document.createTextNode(choice_text));
    div.appendChild(head);

    hidden = document.createElement("input");
    hidden.setAttribute("type", "hidden");
    hidden.setAttribute("id", name + "counter");
    hidden.setAttribute("value", "0");
    div.appendChild(hidden);

    button = document.createElement("button");
    button.setAttribute("type", "button");
    button.appendChild(document.createTextNode(add_text));
    button.setAttribute("onclick", "add_choice('" + div.getAttribute("id") + "', '" + name + "', '" + choice_name + "', '" + rm_choice + "')");

    div.appendChild(button);

    to.appendChild(div);
    to.appendChild(button);
}

/*
 * <div>
 * <h3>Choice field</h3>
 * <input type="hidden" name="field<id>-type" value="bool"/>
 * <label for="field<id>-name">Field name:</label> <input type="text" name="field<id>-name"/>
 * <input type="checkbox" name="field<id>-multichoice" value="Yes" checked /><label for="field<id>-required">Multichoice</label>
 * <input type="checkbox" name="field<id>-required" value="Yes" checked /><label for="field<id>-required">Required</label>
 * </div>
 */
function add_choicefield(holder_name, head_text, fname, multi, req, choice_text, add_text, rm_text, choice_name, rm_choice)
{
    names = "field-" + next_id + "-";

    div = document.createElement("div");
    div.setAttribute("class", "ctrlHolder");
    div.setAttribute("id", names + "holder");
    head = document.createElement("h3");
    head.appendChild(document.createTextNode(head_text));
    div.appendChild(head);

    field_type = document.createElement("input");
    field_type.setAttribute("type", "hidden");
    field_type.setAttribute("name", names + "type");
    field_type.setAttribute("value", "choice");
    div.appendChild(field_type);

    label_name = document.createElement("label");
    label_name.setAttribute("for", names + "name");
    label_name.appendChild(document.createTextNode(fname + "*\n"));
    field_name = document.createElement("input");
    field_name.setAttribute("type", "text");
    field_name.setAttribute("name", names +  "name");
    field_name.setAttribute("class", "textinput");
    div.appendChild(label_name);
    div.appendChild(field_name);

    div.appendChild(document.createElement("br"));

    label_multi = document.createElement("label");
    label_multi.setAttribute("for", names + "multichoice");
    label_multi.appendChild(document.createTextNode(multi));
    field_multi = document.createElement("input");
    field_multi.setAttribute("type", "checkbox");
    field_multi.setAttribute("name", names + "multichoice");
    field_multi.setAttribute("value", "yes");
    field_multi.setAttribute("class", "checkboxinput");
    div.appendChild(field_multi);   
    div.appendChild(label_multi);

    label_req = document.createElement("label");
    label_req.setAttribute("for", names + "required");
    label_req.appendChild(document.createTextNode(req));
    field_req = document.createElement("input");
    field_req.setAttribute("type", "checkbox");
    field_req.setAttribute("name", names + "required");
    field_req.setAttribute("value", "yes");
    field_req.setAttribute("checked", "");
    field_req.setAttribute("class", "checkboxinput");
    div.appendChild(field_req);   
    div.appendChild(label_req);

    add_choicediv(div, names + 'choices-', choice_text, add_text, choice_name, rm_choice);
    addRemoveButton(div, rm_text, holder_name);

    document.getElementById(holder_name).appendChild(div);
    ++ next_id;
}
