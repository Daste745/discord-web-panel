(function () {
    const setColorsInRoles = () => {
        const roleColors = Array.from(document.getElementsByClassName("role-color"));
        for (let element of roleColors) {
            element.style.backgroundColor = element.innerText;
            element.innerText = "";
        }
    };

    const selectAllRoles = () => {
        if (!Sortable.utils.select) return;
        const elements = Array.from(document.getElementById("section-sortable").children);
        for (let element of elements) {
            Sortable.utils.select(element);
        }
    };

    const createSortables = () => {
        let sortables = [];
        sortables.push(Sortable.create(
            document.getElementById("section-sortable"), {
                multiDrag: true,
                preventOnFilter: true,
                selectedClass: "selected",
                animation: 150
            })
        );
    };

    const selectGuild = (event) => {
        for (let element of document.querySelectorAll("#server-list > label")) {
            element.classList.remove("selected")
        }
        event.target.parentElement.classList.add("selected")
    };

    const redirectToBotInvite = () => {
        window.open(
            "https://discordapp.com/oauth2/authorize?client_id=603111310770831360&scope=bot&permissions=268438528",
            "_blank"
        )
    };

    document.addEventListener("DOMContentLoaded", (_event) => {
        createSortables();
        setColorsInRoles();
        Array.from(document.querySelectorAll("#server-list > label > input"))
            .forEach((x) => x.addEventListener("click", selectGuild));
        document.getElementById("select-all-roles-button").addEventListener("click", selectAllRoles);
        document.getElementById("bot-invite-button").addEventListener("click", redirectToBotInvite);
    });

}());
