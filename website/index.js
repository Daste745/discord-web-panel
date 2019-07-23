
(function () {
    const setColorsInRoles = () => {
        const roleColors = Array.from(document.getElementsByClassName("role-color"));
        for (let element of roleColors) {
            element.style.backgroundColor = element.innerText;
            element.innerText = "";
        }
    }
    const selectAllRoles = () => {
        if (!Sortable.utils.select) return;
        const elements = Array.from(document.getElementById("section-sortable").children);
        for (let element of elements) {
            Sortable.utils.select(element);
        }
    }

    const createSortables = () => {
        let sortables = new Array();
        sortables.push(Sortable.create(
            document.getElementById("section-sortable"), {
                multiDrag: true,
                preventOnFilter: true,
                selectedClass: "selected",
                animation: 150
            })
        );
    }
    document.addEventListener("DOMContentLoaded", (_event) => {
        createSortables();
        setColorsInRoles();
        document.getElementById("select-all-roles-button").addEventListener("click", selectAllRoles);
    });

}());
