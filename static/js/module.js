const tabGroup = document.querySelector(".tab-group");
const tabButtons = document.querySelectorAll(".tab-button");
const tabContents = document.querySelectorAll(`.tab`);
let module_completion = document.querySelector(".module-completion");
const green = "#32d373";


function selectTab(tabButton) {
    let id = tabButton.id;
    let tabContent = document.querySelector(`[for=${id}]`);

    for (let otherButton of tabButtons) {
        otherButton.classList.remove("tab-selected");
    }
    for (let content of tabContents) {
        content.style.display = "none";
    }

    tabButton.classList.add("tab-selected");
    tabContent.style.display = "block";
}


function initTabGroups() {
    if (tabGroup && tabButtons.length > 0) {
        selectTab(tabButtons[0]);
    }
    for (let button of tabButtons) {

        button.addEventListener("click", () => {
            selectTab(button);
        })
    }
}


function set_percent_done() {
    if (module_completion == null) {
        return;
    }

    const percent = Math.min(
        Math.round(
            ((window.pageYOffset + window.innerHeight) / document.body.scrollHeight) * 100
        ),
        100
    )

    if (percent == 100) {
        module_completion.style.background = "";
        module_completion.innerHTML = "Module Completed";
        module_completion.classList.add("module-complete");
        module_completion = null;
    }
    /*
    else if (module_completion) {
        module_completion.innerHTML = `${percent}% complete`;
        const progress = `linear-gradient(to right, #32d373 ${percent}%, white ${percent}%)`;
        module_completion.style.background = progress;
    }
    */
}

/*
window.addEventListener("scroll", set_percent_done);
window.addEventListener("load", set_percent_done);
*/


initTabGroups();
