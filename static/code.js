$(function () {
    // Hide the info pane initially eles.one()
    $("#info-pane").hide();

    //Get the info to load the graph
    nodes = [];
    edges = [];
    $.ajax({url: "http://localhost:5000/api/v1/history/all/course-v1:edX+test105+2015_Q2"})
        .done(function (data) {
            $.each(data, function (key, value) {
                if (key.toLowerCase() == 'root') {
                    return true;
                }

                nodes.push({data: {id: key, name: key}});
                console.log("key: " + key + " -- values: " + value)
                if (value.length > 0) {
                    $.each(value, function (index, val) {
                        edges.push({data: {id: "e" + val, source: key, target: val}});
                    });
                }
            });

            // Create and set up the graph.
            $('#cy').cytoscape({
                style: cytoscape.stylesheet()
                    .selector('node')
                    .css({
                        'content': 'data(name)',
                        'text-valign': 'center'
                    })
                    .selector('edge')
                    .css({
                        'target-arrow-shape': 'triangle'
                    }),

                elements: {nodes: nodes, edges: edges},

                layout: {
                    name: 'dagre',
                    rankDir: 'TB'
                },
                ready: function () {
                    window.cy = this;
                    cy.elements().unselectify();
                    cy.on('tap', function (e) {
                        var node = e.cyTarget;
                        $("#info-pane").text(node.data('name'));
                        $("#info-pane").show();

                    });
                }
            });
        });


});
