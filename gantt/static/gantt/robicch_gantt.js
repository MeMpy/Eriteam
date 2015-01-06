function loadGanttFromServer(project_id) {

    var prof = new Profiler("loadServerSide");
    prof.reset();

    $.getJSON("/gantt/robicch/api/project/" + project_id + "/", function (response) {
        //console.debug(response);
        if (response.ok) {
            prof.stop();

            ge.loadProject(response.project);
            ge.checkpoint(); //empty the undo stack

            if (typeof(callback) == "function") {
                callback(response);
            }
        } else {
            jsonErrorHandling(response);
        }

    });
}

function saveGanttOnServer(project_id) {
    if (!ge.canWrite)
        return;


    var prj = ge.saveProject();

    delete prj.resources;
    delete prj.roles;

    var prof = new Profiler("saveServerSide");
    prof.reset();

    if (ge.deletedTaskIds.length > 0) {
        if (!confirm("TASK_THAT_WILL_BE_REMOVED\n" + ge.deletedTaskIds.length)) {
            return;
        }
    }

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax("/gantt/robicch/api/project/" + project_id, {
        dataType: "json",
        data: {project: JSON.stringify(prj)},
        type: "PUT",

        success: function (response) {
            if (response.ok) {
                prof.stop();
                if (response.project) {
                    ge.loadProject(response.project); //must reload as "tmp_" ids are now the good ones
                } else {
                    ge.reset();
                }
            } else {
                var errMsg = "Errors saving project\n";
                if (response.message) {
                    errMsg = errMsg + response.message + "\n";
                }

                if (response.errorMessages.length) {
                    errMsg += response.errorMessages.join("\n");
                }

                alert(errMsg);
            }
        }

    });


}