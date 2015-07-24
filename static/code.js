$(function () {
    //Get the info to load the graph
    nodes = [];
    edges = [];
    $.ajax({url: "/api/v1/history/all/course-v1:edX+test105+2015_Q2"})
        .done(function (data) {
            $.each(data, function (key, value) {
                if (key.toLowerCase() == 'root') {
                    return true;
                }
                $.ajax({url: ""})
                nodes.push({data: {id: key, name: key}});
                console.log("key: " + key + " -- values: " + value)
                if (value.length > 0) {
                    $.each(value, function (index, val) {
                        edges.push({data: {id: "e" + val, source: key, target: val}});
                    });
                }
            });
            reloadGraph(nodes, edges);
        });
});

// Hide the info pane initially
function retrieveStructureInfo(structure_id) {
    $.ajax("/api/v1/block_counts_by_structure/" + structure_id).
        done(function (data) {
            $("#block-counts").text(JSON.stringify(data, null, 2));
        });
};

