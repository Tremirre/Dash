function show_hidden_panel() {
    const hidden_panel = document.getElementById("hidden-panel");
    const button = document.getElementById("table-panel-button");
    const container = document.getElementById("table-container");
    if (hidden_panel == null || button == null || container == null) {
        return;
    }
    var new_text = ">";
    var new_width = "0px";
    var new_opacity = 0;
    if (button.textContent == ">") {
        new_text = "<";
        new_width = "600px";
        new_opacity = 1;
    }
    hidden_panel.style.width = new_width;
    button.textContent = new_text;
    button.style.left = new_width;
    container.style.opacity = new_opacity;
}