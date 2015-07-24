$(function () {
    nodes = [];
    edges = [];
    $.ajax({url: "/api/v1/history/all/" + course_name})
        .done(function (data) {
            history_nodes = data['nodes'];
            $.each(history_nodes, function (key, value) {
                node_data = {data: {id: key, name: key}}
                special_nodes = ['root', 'current'];
                for (var i = 0; i < special_nodes.length; i++) {
                    var special_node = special_nodes[i];
                    if (key === data[special_node][0]) {
                        node_data.data[special_node] = true;
                    }
                }
                nodes.push(node_data);
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

function retrieveStructureInfo(structure_id) {
    $.ajax("/api/v1/block_counts_by_structure/" + structure_id).
        done(function (data) {
            $("#block-counts").text(JSON.stringify(data, null, 2));
        });
};

