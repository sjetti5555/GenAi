document.addEventListener("DOMContentLoaded", function () {
    const timeFilter = document.getElementById("time_filter");
    const customTimeGroup = document.getElementById("custom_time_group");

    if (timeFilter && customTimeGroup) {
        timeFilter.addEventListener("change", function () {
            if (this.value === "custom") {
                customTimeGroup.style.display = "block";
            } else {
                customTimeGroup.style.display = "none";
            }
        });
    }
});
